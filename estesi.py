import nidaqmx
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def adquirir_datos(fs, cantidad):
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev4/ai0", min_val=0, max_val=4)
        task.timing.cfg_samp_clk_timing(fs, sample_mode=nidaqmx.constants.AcquisitionType.FINITE, samps_per_chan=cantidad)
        return [v for _ in range(6) for v in task.read(cantidad)]

def main():
    try:
        fs, cantidad = 250, 2500
        data = adquirir_datos(fs, cantidad)
        nombre = input("Nombre del archivo: ")
        np.save(f"{nombre}.npy", data)
        pd.DataFrame(data).to_csv(f"{nombre}.csv", index=False)
        peaks, _ = find_peaks(data, distance=fs//5, height=0.2)
        if len(peaks) > 1:
            print(f"Frecuencia estimada: {round((60 * fs) / np.mean(np.diff(peaks)), 2)} BPM")
        plt.plot(data); plt.plot(peaks, np.array(data)[peaks], 'rx'); plt.show()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
