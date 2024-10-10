% Script for Indoor localization
% Author: Aravind Potluri <aravindswami135@gmail.com>
% File: IndoLocate.m

% Set up
clear;
clc;
load('matlabData/data.mat', '-ascii');

% Initialize parameters
ch_num = 56;
d = 0.05;
BW = 80;
FREQ = 2^26 / 277022;
FREQ = FREQ * 1e6;

% Extract all SN
SN = unique(sort(data(:, 1)));

% Guess cores, nsss, and items per spectrum
cores = unique(sort(data(:, 2)));
nsss = unique(sort(data(:, 3)));
tonesmin = unique(sort(data(:, 4)));

% Ensure all CSI data has the same type (same num of cores/nss/bandwidths)
coreno = length(cores);
nssno = length(nsss);
itemperspectrum = length(tonesmin);

% Define itemsn as the expected number of items per SN
itemsn = coreno * nssno * itemperspectrum;

% Estimate the number of packets to preallocate memory
max_packets = length(SN);

% Preallocate for txtsdata and alldata
txtsdata = zeros(max_packets, 2); % Assuming two columns: txts and txseqno
alldata(max_packets) = struct('tones', [], 'phytype', [], 'rxts', [], ...
    'rxtsslow', [], 'rxseqno', [], 'txts', [], 'sn', [], 'ts', [], ...
    'srcmac', [], 'powers', [], 'phy0', [], 'core', []); 

packet = 1;
for snjj = 1:length(SN)
    clear framecsi;

    sn = SN(snjj);
    datasn = data(data(:, 1) == sn, :);

    % Check if we have the complete data set for this SN
    if size(datasn, 1) ~= itemsn
        warning('Missing data for SN %d', sn);
        continue;
    end

    error = 0;
    ts = min(datasn(:, 13));
    rxts = min(datasn(:, 14));
    rxtsslow = min(datasn(:, 15));
    rxseqno = min(datasn(:, 16));
    txts = min(datasn(:, 17));
    txseqno = min(datasn(:, 18));
    powers = datasn(:, 19:22);

    if any(any(diff(powers, [], 1) ~= 0))
        warning('Powers not constant over profiles of the same frame');
        continue;
    end
    
    phy0 = datasn(:, 23);
    if any(diff(phy0, [], 1) ~= 0)
        warning('phy0 not constant over profiles of the same frame');
        continue;
    end

    % Store txts and txseqno in preallocated txtsdata
    txtsdata(packet, :) = [txts, txseqno];

    % Process data, give error if missing
    for corejj = 1:length(cores)
        core = cores(corejj);
        for nsskk = 1:length(nsss)
            nss = nsss(nsskk);

            datasub = datasn(datasn(:,2) == core & datasn(:,3) == nss,:);

            if size(datasub, 1) < itemperspectrum
                warning('Incomplete data for SN %d', sn);
                error = 1;
                break;
            end

            tonemin = min(datasub(:, 4));
            tonemax = max(datasub(:, 5));

            phytype = unique(datasub(:, 6));
            if length(phytype) > 1
                warning('Multiple phytype for SN %d', sn);
                error = 1;
                break;
            end

            macaddr = datasub(7:12);
            datasub = datasub(:, 28:2:end) + 1i * datasub(:, 29:2:end);
            N = size(datasub, 2);

            if itemperspectrum > 1
                warning('itemperspectrum > 1 unsupported');
                error = 1;
                break;
            end

            els = numel(datasub);
            datasub = reshape(datasub.', 1, els);

            framecsi.core{core + 1}.nss{nss + 1}.data = datasub;

        end
        if error == 1
            break;
        end
    end

    if error == 1
        continue;
    end

    % Store framecsi data in the preallocated alldata
    framecsi.tones = [tonemin, tonemax];
    framecsi.phytype = phytype;
    framecsi.rxts = int64(rxts);
    framecsi.rxtsslow = rxtsslow;
    framecsi.rxseqno = rxseqno;
    framecsi.txts = int64(txts);
    framecsi.sn = sn;
    framecsi.ts = ts;
    framecsi.srcmac = sprintf('%02X%02X%02X%02X%02X%02X', macaddr);
    framecsi.powers = powers(1, :);
    framecsi.phy0 = phy0(1, :);

    alldata(packet) = framecsi;
    packet = packet + 1;
end

% Trim the preallocated arrays to the actual number of packets
txtsdata = txtsdata(1:packet-1, :);
alldata = alldata(1:packet-1);

fprintf('Found CSI for %d packets\n\n', packet-1);

% Actual angle calculation

num_packets = length(alldata);
subcarriers = get_subcarriers(ch_num);

% Preallocate AoA and timestamps
AoA_31 = zeros(1, num_packets); % Left - Middle
AoA_14 = zeros(1, num_packets); % Middle - Right
AoA_34 = zeros(1, num_packets); % Left - Right
target_loc = zeros(2, num_packets); % Location of target
timestamps = zeros(1, num_packets);

% Antenna positions
ap_31 = [-d/2, 0]; % Left-Middle antennas
ap_14 = [+d/2, 0]; % Middle-Right antenna
ap_34 = [0, 0];    % Right-Middle antenna

% Loop through each element in alldata
for i = 1:num_packets
    % Extract phase angles for antenna 
    phi_1 = alldata(i).core{1}.nss{1}.data; % Core 1 (Middle)
    phi_2 = alldata(i).core{2}.nss{1}.data; % Core 2 (Internal)
    phi_3 = alldata(i).core{3}.nss{1}.data; % Core 3 (Left)
    phi_4 = alldata(i).core{4}.nss{1}.data; % Core 4 (Right)

    % Calculate AoA for the current alldata element for each pair
    AoA_31(i) = extract_angle(phi_3, phi_1, subcarriers, d); % Left-Middle
    AoA_14(i) = extract_angle(phi_1, phi_4, subcarriers, d); % Middle-Right
    AoA_34(i) = extract_angle(phi_3, phi_4, subcarriers, d); % Left-Right

    % Estimate the client position using triangulation
    Q = [
        tan(AoA_31(i)), -1;
        tan(AoA_14(i)), -1;
        tan(AoA_34(i)), -1;
    ];
    
    f = [
        ap_31(1)*tan(AoA_31(i)) - ap_31(2);
        ap_14(1)*tan(AoA_14(i)) - ap_14(2);
        ap_34(1)*tan(AoA_34(i)) - ap_34(2)
    ];

    target_loc(:, i) = (Q' * Q) \ (Q' * f);

    % Extract timestamp for the current element
    timestamps(i) = alldata(i).ts;
end

%% Plot AoA over time for each antenna pair

% figure('Name', 'AoA');
% hold on; % Hold on to overlay multiple plots
% plot(timestamps, rad2deg(AoA_31), '-o', 'DisplayName', 'AoA 3-1 (Left-Middle)');
% plot(timestamps, rad2deg(AoA_14), '-s', 'DisplayName', 'AoA 1-4 (Middle-Right)');
% plot(timestamps, rad2deg(AoA_34), '-d', 'DisplayName', 'AoA 3-4 (Left-Right)');
% xlabel('Relative Time (s)');
% ylabel('Angle of Arrival (AoA) (degrees)');
% title('Angle of Arrival over Time');
% ylim([-180 180]);
% yticks(-180:45:180);
% grid on;
% set(gca, 'YGrid', 'on', 'YMinorGrid', 'off');
% legend show;
% hold off;

%% Plot 2D Location with time

x_coords = target_loc(1, :);
y_coords = target_loc(2, :);
time_diffs = diff(timestamps);

fig = figure('Name', '2D Location Animation', 'Position', ...
    [100, 100, 800, 600]);
hold on;
xlabel('X Coordinate');
ylabel('Y Coordinate');
title('2D Location over time');
xlim([min(x_coords) - 0.1, max(x_coords) + 0.1]);
ylim([min(y_coords) - 0.01, max(y_coords) + 0.1]);
grid on;

plot(ap_31(1), ap_31(2), 'rs', 'MarkerSize', 5, 'MarkerFaceColor', ...
    'r', 'DisplayName', 'AP 31 (Left)');
plot(ap_14(1), ap_14(2), 'gs', 'MarkerSize', 5, 'MarkerFaceColor', ...
    'g', 'DisplayName', 'AP 14 (Middle)');
plot(ap_34(1), ap_34(2), 'bs', 'MarkerSize', 5, 'MarkerFaceColor', ...
    'b', 'DisplayName', 'AP 34 (Right)');

text(ap_31(1), ap_31(2), 'AP 31', 'VerticalAlignment', 'top', ...
    'HorizontalAlignment', 'center');
text(ap_14(1), ap_14(2), 'AP 14', 'VerticalAlignment', 'top', ...
    'HorizontalAlignment', 'center');
text(ap_34(1), ap_34(2), 'AP 34', 'VerticalAlignment', 'top', ...
    'HorizontalAlignment', 'center');

h = plot(x_coords(1), y_coords(1), 'bo', 'MarkerSize', 8, ...
    'MarkerFaceColor', 'b', 'DisplayName', 'Client');

setappdata(fig, 'x_coords', x_coords);
setappdata(fig, 'y_coords', y_coords);
setappdata(fig, 'time_diffs', time_diffs);
setappdata(fig, 'num_packets', num_packets);
setappdata(fig, 'h_client', h);

uicontrol('Style', 'pushbutton', 'String', 'Play', ...
    'Position', [20, 10, 60, 30], 'Callback', @PlayCallback);
uicontrol('Style', 'pushbutton', 'String', 'Stop', ...
    'Position', [100, 10, 60, 30], 'Callback', @StopCallback);
uicontrol('Style', 'pushbutton', 'String', 'Exit', ...
    'Position', [180, 10, 60, 30], 'Callback', @exitCallback);

setappdata(gcf, 'stopAnimation', false);

function PlayCallback(~, ~)
    disp('Playing Animation ..');
    % Retrieve data from appdata
    h = getappdata(gcf, 'h_client');
    x_coords = getappdata(gcf, 'x_coords');
    y_coords = getappdata(gcf, 'y_coords');
    time_diffs = getappdata(gcf, 'time_diffs');
    num_packets = getappdata(gcf, 'num_packets');
    
    playButton = gco;
    set(playButton, 'Enable', 'off');
    
    % Reset stop condition
    setappdata(gcf, 'stopAnimation', false); 

    % Loop through each point and update the plot using time intervals
    for i = 1:num_packets - 1
        % Check if the stop condition is true
        if getappdata(gcf, 'stopAnimation')
            break;
        end

        % Update the x and y data of the plot
        set(h, 'XData', x_coords(i), 'YData', y_coords(i));

        % Optional: Plot the trajectory by adding a trace
        % plot(x_coords(1:i), y_coords(1:i), 'b-', 'LineWidth', 0.5);
        
        % Pause based on the actual time difference between points
        pause(time_diffs(i)); 
    end

    set(playButton, 'Enable', 'on'); % Enable the Play button again
end

function StopCallback(~, ~)
    setappdata(gcf, 'stopAnimation', true); % Set stop condition to true
end

function exitCallback(~, ~)
    disp('Exiting...');
    close(gcf);
end
