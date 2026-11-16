function [pks, locs, w_fwhm] = find_resonance_peaks(y, x)
% FIND_RESONANCE_PEAKS - Robust Peak and FWHM Detector (Toolbox-Independent)
%
% Syntax:
%   [pks, locs, w_fwhm] = find_resonance_peaks(y, x)
%
% Inputs:
%   y - Signal vector (e.g. transmission coefficient T(E))
%   x - Coordinate vector (e.g. energy E)
%
% Outputs:
%   pks    - Array of peak values
%   locs   - Array of peak locations along x
%   w_fwhm - Full-Width at Half-Maximum (FWHM / linewidth Gamma) for each peak
%
% Works natively in base MATLAB without requiring the Signal Processing Toolbox.

    pks = [];
    locs = [];
    w_fwhm = [];

    N = length(y);
    if N < 3
        return;
    end

    dx = abs(x(2) - x(1));

    % Detect local maxima
    for i = 2:(N-1)
        if y(i) > y(i-1) && y(i) >= y(i+1) && y(i) > 0.02
            % Refine peak position using 3-point parabolic interpolation
            denom = (y(i-1) - 2*y(i) + y(i+1));
            if abs(denom) > 1e-12
                delta = 0.5 * (y(i-1) - y(i+1)) / denom;
                x_peak = x(i) + delta * dx;
                y_peak = y(i) - 0.25 * (y(i-1) - y(i+1)) * delta;
            else
                x_peak = x(i);
                y_peak = y(i);
            end

            pks(end+1) = max(0, min(1, y_peak)); %#ok<AGROW>
            locs(end+1) = x_peak; %#ok<AGROW>

            % Estimate FWHM (Full-Width at Half-Maximum)
            half_max = y(i) * 0.5;

            % Search left
            left_idx = i;
            while left_idx > 1 && y(left_idx) > half_max
                left_idx = left_idx - 1;
            end
            if left_idx < i && (y(left_idx+1) - y(left_idx)) ~= 0
                x_left = x(left_idx) + (half_max - y(left_idx)) / (y(left_idx+1) - y(left_idx)) * (x(left_idx+1) - x(left_idx));
            else
                x_left = x(max(1, left_idx));
            end

            % Search right
            right_idx = i;
            while right_idx < N && y(right_idx) > half_max
                right_idx = right_idx + 1;
            end
            if right_idx > i && (y(right_idx) - y(right_idx-1)) ~= 0
                x_right = x(right_idx-1) + (half_max - y(right_idx-1)) / (y(right_idx) - y(right_idx-1)) * (x(right_idx) - x(right_idx-1));
            else
                x_right = x(min(N, right_idx));
            end

            width = max(dx, x_right - x_left);
            w_fwhm(end+1) = width; %#ok<AGROW>
        end
    end
end
