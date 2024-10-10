function [lambdas] = get_subcarriers(channel_num, subcarrier_spacing, num_subcarriers)
% Returns a vector of subcarriers wavelength.
    % Constants
    c = 299792458;  % Speed of light in m/s (higher precision)

    % Set default values for optional parameters if not provided
    if nargin < 2
        % Default subcarrier spacing in Hz (312.5 kHz)
        subcarrier_spacing = 312.5e3; 
    end
    
    if nargin < 3
        % Default number of subcarriers
        num_subcarriers = 128; 
    end

    % Central frequency mapping for Wi-Fi channels (5 GHz band)
    channel_info = [
        struct('channel', 36, 'frequency', 5180e6);
        struct('channel', 40, 'frequency', 5200e6);
        struct('channel', 44, 'frequency', 5220e6);
        struct('channel', 48, 'frequency', 5240e6);
        struct('channel', 52, 'frequency', 5260e6);
        struct('channel', 56, 'frequency', 5280e6);
        struct('channel', 60, 'frequency', 5300e6);
        struct('channel', 64, 'frequency', 5320e6)
    ];

    % Validate channel number and retrieve corresponding channel info
    idx = find([channel_info.channel] == channel_num, 1);
    if isempty(idx)
        error('Unsupported channel number');
    end
    
    center_frequency = channel_info(idx).frequency;
    
    % Generate the list of subcarriers around the central frequency
    subcarriers_frequency = center_frequency + ((1:num_subcarriers) - (num_subcarriers / 2 + 0.5)) * subcarrier_spacing;
    lambdas = c ./ subcarriers_frequency; % Calculate wavelengths
end
