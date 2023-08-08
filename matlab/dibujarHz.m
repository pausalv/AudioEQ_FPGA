fs = 48e3;

fc = 1e3;

Q = 0.5;
G = 10;

[b,a] = peak_filter(fc,Q,G,fs);

n = 1000;
f = linspace(0,fs/2,n);
s = 1j*2*pi*f;
z = exp(s/fs);

z_v = [ones(size(z)); z.^-1; z.^-2];
% z_v = [z.^2; z; ones(size(z))];


b_z = b'.*z_v;
num = sum(b_z);

a_z = a'.*z_v;
den = sum(a_z);

Hs = num ./ den;

figure(10)
semilogx(f,20*log10(abs(Hs)))