function [b,a] = low_pass_filter(fc, fs)
    % fc: cut-off frequency
    % fs: sampling frequency
    % b: numerator coefficients
    % a: denominator coefficients
    
    K = calculateK(fc, fs);

    b0 = K^2 /(1 + sqrt(2)*K + K^2);
    b1 = 2*K^2 /(1 + sqrt(2)*K + K^2);
    b2 = b0;

    a0 = 1;
    a1 = 2*(K^2 - 1) /(1 + sqrt(2)*K + K^2);
    a2 = (1 - sqrt(2)*K + K^2) /(1 + sqrt(2)*K + K^2);

    b = [b0 b1 b2];
    a = [a0 a1 a2];
end
