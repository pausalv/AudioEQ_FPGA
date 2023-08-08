function drawFreqZ(b,a,n,fs,fig)
    [h,f] = freqz(b,a,n,fs);
    figure(fig)
    clf
    subplot(211)
    semilogx(f,20*log10(abs(h)))
    xlim([20 20e3])
    grid
    xlabel('Frecuencia [Hz]')
    ylabel('Amplitud [dB]')
    title('Respuesta en frecuencia')
    subplot(212)
    semilogx(f,unwrap(angle(h)))
    xlim([20 20e3])
    grid
    xlabel('Frecuencia [Hz]')
    ylabel('Fase [rad]')
end