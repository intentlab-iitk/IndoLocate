function [AoA] = extract_angle(csi1, csi2, lambdas, d)  
    % extract_angle csi1, csi2: CSI Info corresponding Antenna ...
    % lambdas: Is a subcarrier wave length vector
    % d: Distance between antennas
    % Returns the Angle of Arrival(radians) for a given CSI info from two antennas
    
    num_subcarriers = length(lambdas);
    
    % Validate that both core1_CSI and core2_CSI
    if length(csi1) ~= length(csi2) || length(csi1) ~= num_subcarriers
        error('Mismatch in length of subcarriers or CSI Matrices');
    end
    
    % Calculate the phase difference for each subcarrier
    delta_phase = angle(csi1) - angle(csi2);

    % Estimate AoA in radians using the vector of subcarrier wavelengths
    aoa_radians = real(asin((lambdas .* delta_phase) / (2 * pi * d)));

    % Convert AoA from radians to degrees
    AoA = mean(aoa_radians);
end
