fs = 48e3;

fc = 1e3;

fc1 = 100;
fc2 = 10e3;

Q = 0.5;
G = 10;

% [b,a] = low_pass_filter(fc,fs);
% [b,a] = high_pass_filter(fc,fs);
% [b,a] = band_pass_filter(fc1,fc2,fs);
[b1,a1] = peak_filter(fc,Q,-G,fs);
[b2,a2] = peak_filter1(fc,Q,-G,fs);

dibujarFreqZ(b1,a1,4096,fs,3);
dibujarFreqZ(b2,a2,4096,fs,4);
% ylim([0 10])