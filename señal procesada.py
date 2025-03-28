import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, find_peaks
from scipy.signal.windows import hann 
from scipy.fft import fft, fftfreq
from scipy.stats import median_abs_deviation, ttest_1samp

# Cargar el archivo NPY
archivo_npy = "emg_Andre.npy"
data = np.load(archivo_npy).flatten()  # Asegurar que sea 1D

#  Graficar la señal original
plt.figure(figsize=(10, 4))
plt.plot(data, linestyle="-", color='b')
plt.xlabel("Tiempo (muestras)")
plt.ylabel("Amplitud EMG")
plt.title("Señal EMG original")
plt.grid()
plt.show()

#  Aplicar filtros pasa alto y pasa bajo
def butter_bandpass(lowcut, highcut, fs, order=4):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a

fs = 1000  # Frecuencia de muestreo estimada (ajústala si es necesario)
lowcut = 20  # Frecuencia de corte inferior (pasa alto)
highcut = 450  # Frecuencia de corte superior (pasa bajo)

b, a = butter_bandpass(lowcut, highcut, fs)
filtered_data = filtfilt(b, a, data)

#  Graficar la señal filtrada
plt.figure(figsize=(10,4))
plt.plot(filtered_data, linestyle="-", color='g')
plt.xlabel("Tiempo (muestras)")
plt.ylabel("Amplitud EMG")
plt.title("Señal EMG con filtro pasa alto y pasa bajo")
plt.grid()
plt.show()

#  Encontrar picos (contracciones) con ajuste de umbral
target_peaks = 17  # Se buscan exactamente 17 contracciones
umbral_min = 0.2  # Reducir el umbral para captar picos más pequeños
distance_min = 500  # Reducir la distancia mínima entre picos

peaks, _ = find_peaks(np.abs(filtered_data), height=umbral_min, distance=distance_min)

# Si se detectan más de 17 picos, tomamos los primeros 17
if len(peaks) > target_peaks:
    peaks = peaks[:target_peaks]

#  Extraer y aplicar ventana de Hanning a las 17 contracciones
window_size = 2000  # Ajuste del tamaño de la ventana
segments = []
windowed_segments = []
fft_segments = []
freqs_list = []
freq_means = []

print("\nResultados de Análisis de Frecuencia:\n")
for i, peak in enumerate(peaks):  # Tomar solo las 17 contracciones encontradas
    start = max(0, peak - window_size // 2)
    end = min(len(filtered_data), peak + window_size // 2)
    segment = filtered_data[start:end]

    # Aplicar ventana de Hanning a cada contracción
    if len(segment) > 1:  # Asegurar que hay suficientes datos para aplicar la ventana
        window = hann(len(segment))
        windowed_segment = segment * window
        segments.append(segment)
        windowed_segments.append(windowed_segment)

        #  Aplicar Transformada de Fourier (FFT)
        N = len(segment)
        fft_values = np.abs(fft(windowed_segment))[:N // 2]  # Magnitud de la FFT
        freqs = fftfreq(N, 1/fs)[:N // 2]  # Frecuencias correspondientes
        fft_segments.append(fft_values)
        freqs_list.append(freqs)

        #  Calcular estadísticas del espectro considerando la magnitud
        freq_dominant = freqs[np.argmax(fft_values)]
        freq_median = np.median(np.repeat(freqs, fft_values.astype(int)))  # Mediana ponderada
        freq_mean = np.sum(freqs * fft_values) / np.sum(fft_values)  # Media ponderada
        freq_std = np.sqrt(np.sum(((freqs - freq_mean) ** 2) * fft_values) / np.sum(fft_values))  # Desviación estándar ponderada
        freq_means.append(freq_mean)
        
        print(f"Estadísticas espectrales del Segmento {i+1}:")
        print(f"  Frecuencia Dominante: {freq_dominant:.2f} Hz")
        print(f"  Frecuencia Mediana: {freq_median:.2f} Hz")
        print(f"  Frecuencia Media: {freq_mean:.2f} Hz")
        print(f"  Desviación Estándar de la Frecuencia: {freq_std:.2f} Hz\n")

#  Graficar cada contracción y su respectiva FFT
for i, (segment, fft_values, freqs) in enumerate(zip(segments, fft_segments, freqs_list)):
    fig, axs = plt.subplots(2, 1, figsize=(8, 6))
    
    # Gráfico de la señal en el tiempo
    axs[0].plot(segment, linestyle="-", color='r')
    axs[0].set_xlabel("Tiempo (muestras)")
    axs[0].set_ylabel("Amplitud EMG")
    axs[0].set_title(f"Contracción {i+1} ")
    axs[0].grid()
    
    # Gráfico de la FFT
    axs[1].plot(freqs, fft_values, linestyle="-", color='b')
    axs[1].set_xlabel("Frecuencia (Hz)")
    axs[1].set_ylabel("Magnitud")
    axs[1].set_title(f"Espectro de frecuencia de la contracción {i+1}")
    axs[1].grid()
    
    plt.tight_layout()
    plt.show()

#  Prueba de hipótesis sobre la media más alta y más baja
if freq_means:
    ref_value = 50  # Valor de referencia
    min_max_freqs = [min(freq_means), max(freq_means)]  # Solo usar la mínima y máxima frecuencia
    
    # Test de hipótesis
    t_stat, p_value = ttest_1samp(min_max_freqs, ref_value)
    print("\nPrueba de Hipótesis sobre la Media de Frecuencia:")
    print(f"  Frecuencia mínima considerada: {min_max_freqs[0]:.2f} Hz")
    print(f"  Frecuencia máxima considerada: {min_max_freqs[1]:.2f} Hz")
    print(f"  Estadístico t: {t_stat:.4f}")
    print(f"  Valor p: {p_value:.4f}")
    
    # Evaluación del resultado
    if p_value < 0.05:
        print("➡ Se rechaza la hipótesis nula (H0). Hay evidencia significativa de que la media no es 50 Hz.")
    else:
        print("✅ No se rechaza la hipótesis nula (H0). No hay suficiente evidencia para afirmar que la media es diferente de 50 Hz.")
else:
    print("No se encontraron segmentos válidos para el análisis de hipótesis.")
