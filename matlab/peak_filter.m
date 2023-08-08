function [b,a] = peak_filter(fc,Q,G,fs)
%PEAK_FILTER Summary of this function goes here
%   Detailed explanation goes here

    K = calculateK(fc, fs);
    V0 = 10^(G/20);

    b0 = (1 + K*V0/Q + K^2) / (1 + K/Q + K^2);
    b1 = 2 * (K^2 - 1) / (1 + K/Q + K^2);
    b2 = (1 - K*V0/Q + K^2) / (1 + K/Q + K^2);

    a0 = 1;
    a1 = 2 * (K^2 - 1) / (1 + K/Q + K^2);
    a2 = (1 - K/Q + K^2) / (1 + K/Q + K^2);

    b = [b0 b1 b2];
    a = [a0 a1 a2];

end