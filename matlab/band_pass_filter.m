function [b,a] = band_pass_filter(fc1, fc2, fs)
    % fc1: lower cut-off frequency
    % fc2: upper cut-off frequency
    % fs: sampling frequency
    % b: numerator coefficients of the filter
    % a: denominator coefficients of the filter

    fc = sqrt(fc1*fc2);
    Q = fc/(fc2 - fc1);
    % Q = 1/Q;
    K = calculateK(fc, fs);

    b0 = K/Q / (1 + K/Q + K^2);
    b1 = 0;
    b2 = -b0;

    a0 = 1;
    a1 = 2*(K^2 - 1) / (1 + K/Q + K^2);
    a2 = (1 - K/Q + K^2) / (1 + K/Q + K^2);

    b = [b0 b1 b2];
    a = [a0 a1 a2];

end
