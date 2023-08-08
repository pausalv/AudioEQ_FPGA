function [b,a] = peak_filter1(fc,Q,G,fs)
%PEAK_FILTER Summary of this function goes here
%   Detailed explanation goes here
    wc = 2*pi*fc/fs;
    alpha = sin(wc)/(2*Q);
    g = 10^(G/40);

    b0 = 1 + alpha*g;
    b1 = -2*cos(wc);
    b2 = 1 - alpha*g;

    a0 = 1 + alpha/g;
    a1 = -2*cos(wc);
    a2 = 1 - alpha/g;

    b = [b0 b1 b2]/a0;
    a = [a0 a1 a2]/a0;

end