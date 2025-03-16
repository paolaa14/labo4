Se realizó una práctica de laboratorio para lograr medir y explicar una señal EMG, para llevar a cabo esto, 





Para correr el codigo y que funcione correctamente se deben descargar ciertas cosas, inicialmente en la consola de spyder se deben descargar librerías de la siguiente manera; pip install numpy matplotlib wfdb scipy, estas son para;

- import numpy as np: es para que permita correr cálculos númericos y arrays en caso de     tenerlos.
- import matplotlib.pyplot as plt :grafica señales de audio y transformaciones, como 
  espectros de frecuencia.
- import scipy.io.wavfile as wavfile ; lee archivos en formato WAV, Con wavfile.read() se   cargan archivos WAV y se obtiene su frecuencia de muestreo y los datos. -from         
  scipy.fftpack import fft; Importa la Transformada Rápida de Fourier (FFT), que se usa     para convertir una señal del dominio del tiempo al dominio de la frecuencia.
  from sklearn.decomposition import FastICA; implementa el Análisis de Componentes 
