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

% Ensure all CSI data has the same type (same number of cores/nss/bandwidths)
coreno = length(cores);
nssno = length(nsss);
itemperspectrum = length(tonesmin);

% Define itemsn as the expected number of items per SN
itemsn = coreno * nssno * itemperspectrum;

% Estimate the number of packets to preallocate memory
max_packets = length(SN);

% Preallocate for txtsdata and alldata
txtsdata = zeros(max_packets, 2); % Assuming two columns: txts and txseqno
alldata(max_packets) = struct('tones', [], 'phytype', [], 'rxts', [], 'rxtsslow', [], 'rxseqno', [], 'txts', [], 'sn', [], 'ts', [], 'srcmac', [], 'powers', [], 'phy0', [], 'core', []); 

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

            datasub = datasn(datasn(:, 2) == core & datasn(:, 3) == nss, :);

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

%% Actual angle calculation

num_packets = length(alldata);
subcarriers = get_subcarriers(ch_num);

% Preallocate AoA and timestamps
AoA_31 = zeros(1, num_packets); % Left - Middle
AoA_14 = zeros(1, num_packets); % Middle - Right
AoA_34 = zeros(1, num_packets); % Left - Right
timestamps = zeros(1, num_packets);

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

    % Extract timestamp for the current element
    timestamps(i) = alldata(i).ts;
end

% Plot AoA over time for each antenna pair
figure('Name', 'IndoLocate');
hold on; % Hold on to overlay multiple plots
plot(timestamps, AoA_31, '-o', 'DisplayName', 'AoA 3-1 (Left-Middle)');
plot(timestamps, AoA_14, '-s', 'DisplayName', 'AoA 1-4 (Middle-Right)');
plot(timestamps, AoA_34, '-d', 'DisplayName', 'AoA 3-4 (Left-Right)');

% Set axis labels, title, and legend
xlabel('Relative Time (s)');
ylabel('Angle of Arrival (AoA) (degrees)');
title('Angle of Arrival over Time');
ylim([-180 180]);
yticks(-15:20:15);
grid on;
set(gca, 'YGrid', 'on', 'YMinorGrid', 'off');
legend show;
hold off;
