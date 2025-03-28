Se realizó una práctica de laboratorio para lograr medir y explicar una señal EMG y observar a su vez la fatiga del músculo, para llevar a cabo esto, inicialmente se realizó la preparación del sujeto de prueba, este se posicionó en una silla para colocarle los electrodos de superficie (es decir que solo se pegan en la piel) en el músculo  Flexor superficial de los dedos que se adhieren bien a la piel por el gel conductor que posee el electrodo, para lograr adquierir la señal de emg y la respectiva fatiga,  se implementó una tarjeta conocida como DAQ, pero a la vez fue necesario descargar un programa de Controlador NI-DAQmx para que el computador la reconociera y se logrará hacer una correcta toma de la señal.

En dado caso de querer descargarlo, se pueden dirigir a la paginal de national instruments (NI) para instalar esto, luego para ejecutar esto en el pythonn(sino se tiene descargado se puede descargar y en nuestro caso en particular estamos usando anaconda y más especificamente spyder), se debe abrir en el terminal, pip install nidaqmx, con el fin de instalar esto en el python y que lo reconozca, posterior a esto, se conecta la tarjeta DAQ al computador y se abre automaticamente el NI MAX, que reconoce esta como un device, con esto claro se procede hacer el código en python que se explicará detalladamente a continuación:



sección del código;
CODIGO de la adquisición de la señal, este código lo pueden copiar y compilar en python, ya que fue con el que adquirimos la señal no obstante para que funcione optimamente tienen que realizar el circuito como se evidenciará más adelante.

import nidaqmx      == esto es una libreria de python que es para interactuar con dispositivos como la DAQ, permitiendo leer datos de los dispositivos conectados  a la DAQ (el sensor emg) 


import pandas as pd     === esta librería sirve para manipular datos cienctificos, se usa para almacenar, procesar y analizar los datos adquiridos.


import numpy as np  ====     es una libreria para cálculo matemático y manipulación de arreglos numéricos, se implementa para manejar muchos datos  (todas las cantidades de muestras de una contracción) de manera eficiente.


import matplotlib.pyplot as plt   === es una librería ára visualizar datos por medios de gráficas, que permite graficar la señal EMG y analizarla de manera visual.


from scipy.signal import find_peaks    ====  se usa para encontrar picos en una señal, identificando momentos donde en la señal emg se alcanzan los valores máximos, es decir las contracciones musculares


def adquirir_datos(fs, cantidad):   == se define una función que toma dos parámetros fs, que es la frecuencia de muestreo en Hz, es decir cuantas muestras por segundo se capturarán y la cantidad que es el número total de muestras a adquirir.


    with nidaqmx.Task() as task: == aqui se crea una tarea DAQ, que es basicamente una configuración deadquisiión de datos de la tarjeta DAQ.
    
        task.ai_channels.add_ai_voltage_chan("Dev4/ai0", min_val=0, max_val=4) ==aquí dice que esta parte "Dev4/ai0" indica que la señal leerpa del canal analogico 0 (en la DAQ hay un puerto que se llama ai0), en cuanto a min_val=0, max_val=4
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

if _name_ == "_main_":
    main()import nidaqmx
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

if _name_ == "_main_":
    main()


A su vez, se conectaron los electrodos al sensor emg, que permitirá captar bien la señal muscular, teniendo claro que el músculo que elegimos, en la parte del antebrazo, el flexor superficial, se realiza un cálculo de la frecuencia de muestreo para realizar la captura de la señal.

![WhatsApp Image 2025-03-27 at 11 48 14](https://github.com/user-attachments/assets/670f57d2-f976-427d-a5ca-7744fa0e4679)


2. Para continuar, el sujero ya estando conectado se le pidió realizar primero el movimiento de apretar una pelota antiestres para llegar a la contracción con mayor facilidad, entonces se le pidió que realizará la contracción del músculo mencionado y se registra la señal por medio el código de python.


<img width="609" alt="Figure 2025-03-27 111639" src="https://github.com/user-attachments/assets/b6fc20c2-1ca5-49aa-bca3-ce419dd2c262" />

Imagen 1. Señal emg del músculo

En esta gráfica se evidencia como quedó la captura de la señal emg, del músculo mencionado previamente, que muestra  la actividad del músculo, donde se incluye la contracción, relajación y fatiga,  en esta imagen en particular, observamos que que hay cambios grandes en la amplitud de la señal, es decir que hay niveles de actividad muscular, asimismo, para llevar a cabo un análisis más claro, identificaremos las fases por las que pasa la gráfica;
 
  En primer lugar, la fase de contracción donde se observan segmentos que la amplitud aumenta de manera signifcativa, representando la activación de las fibras musculares en rerspuesta a la contraciión que se esta haciendo de manera voluntaria, y se observa en algunos puntos más intensidad y duración, lo que indica que al ser voluntaria estos dos factores dependen de la persona que esta haciendo la contracción.
 
  En segundo lugar, la fase de relajación, no se observa completamente, debido a que se presentaron movimientos involuntarios donde se movió el brazo por estar repitiendo la señal distintas veces, ya que al inicio no nos salia, tuvimos que repetirla para llegar a la gráfica que se muestra, entonces repetir esta captura en más de una ocasión genera que la persona se canse y se le presenten leves temblores en el brazo producto del cansancio, asimismo, tuvimos que cambiar de persona en 3 ocasiones ya que el músculo no se encontraba, este cambio se realizó inicialmente con electrodos nuevos, pero al realizar distintas pruebas ya no teniamos más electrodos, por esto al final ya se perdió un poco el pegante, es decir que no se aherian bien a la piel y eto genera inconvenientes en la señal tomada, por otro lado, al tener un sensor emg, los cables no se encontraban lo suficientemente largos, y se necesitaba un poco de espacio para realizaar la contracción, entonces el roce con los cbales generaba una interferencia, recreando una posible actividad cuando en verdad era relajación, y por último, otro factor de afectación en la señal, fue que el músculo pudo no alcanzar la relajación total entre contracciones por la fatiga, esto demuestra que la señal podria no haber descendido completamente en el reposo 
 

 


3. Poaterior a esto, se aplica un filtro a la señal pasa alta, con el fin de eliminar componentes de baja frecuencia (ruido que se asocie al movimiento), y asu vez se implementó un filtro pasa baja para quitar frecuencias altas como el ruidp electromagnético.



   aqui con filtro
4. Es necesario mencionar, que para captar un pedazo de la señal que resultara analizable, se implementó una ventana, para observar determinado pedazo de la señal. y se le realizará un análisis espectral implementando la transformada de fourier para obtener el espectro de frecuencas en intervalos determinados de la señal EMG.




5. Luego a todo esto, se observará como cambia el espectro se la señal en cada ventana mientras más se acerque  a la fatiga muscular, para evaluar la disminución de la frecuencia mediana en cada ventana como indicador de la fatiga, por último se implementa una prueba de hipótesis para verificar si el cambio en la mediana tiene un valor significativo en la estadistíca.



La mediana se calcula con la formmula
senal filtrada pasa alto y pasa bajo
<img width="617" alt="Figure 2025-03-27 191053 (1)" src="https://github.com/user-attachments/assets/76f5872d-b4a2-4559-a0e5-9c26f504154b" />


ventanas por contracciones (17) con su respectivo espectro 

<img width="569" alt="Figure 2025-03-27 191053 (2)" src="https://github.com/user-attachments/assets/8e27e4c9-142e-4eb3-993a-43c2ff532b90" />

<img width="569" alt="Figure 2025-03-27 191053 (3)" src="https://github.com/user-attachments/assets/851216c1-e66e-40e5-a4f1-4ca716f5a00d" />


<img width="569" alt="Figure 2025-03-27 191053 (4)" src="https://github.com/user-attachments/assets/f7086e05-d30b-4c12-b835-801cff2b9e67" />


<img width="569" alt="Figure 2025-03-27 191053 (5)" src="https://github.com/user-attachments/assets/d1a9986a-98a0-44e6-812a-342e8c6a43b4" />

<img width="569" alt="Figure 2025-03-27 191053 (6)" src="https://github.com/user-attachments/assets/8cfaf68f-4938-48f3-a734-95340fb8d91a" />

<img width="569" alt="Figure 2025-03-27 191053 (7)" src="https://github.com/user-attachments/assets/cbe3ac83-92c9-4d24-9c2e-03c3df24f3c3" />

<img width="569" alt="Figure 2025-03-27 191053 (8)" src="https://github.com/user-attachments/assets/6780977f-f3f9-4eb9-947f-1312d52bea22" />

<img width="569" alt="Figure 2025-03-27 191053 (9)" src="https://github.com/user-attachments/assets/4fff6596-9acc-4cd4-a97f-7e8fb88dde97" />


<img width="569" alt="Figure 2025-03-27 191053 (10)" src="https://github.com/user-attachments/assets/8a3989d2-c624-4dca-9f11-19c9eec87d5a" />

<img width="569" alt="Figure 2025-03-27 191053 (11)" src="https://github.com/user-attachments/assets/dae943bb-e27f-4aa9-8d70-00caf78e6924" />

<img width="569" alt="Figure 2025-03-27 191053 (12)" src="https://github.com/user-attachments/assets/6ce3c6ea-c6c9-445e-b51f-8e3c8347be5e" />

<img width="569" alt="Figure 2025-03-27 191053 (13)" src="https://github.com/user-attachments/assets/43253198-5f5a-4dc9-a066-dcd5050947c0" />

<img width="569" alt="Figure 2025-03-27 191053 (14)" src="https://github.com/user-attachments/assets/ca08fc91-c744-4499-8cbe-d6c80d3a867d" />

<img width="569" alt="Figure 2025-03-27 191053 (15)" src="https://github.com/user-attachments/assets/6ed15224-8351-49e2-8e2b-bd28fd41b725" />

<img width="569" alt="Figure 2025-03-27 191053 (16)" src="https://github.com/user-attachments/assets/b3305a7a-38c4-4e38-a7ac-c6f8c0609a74" />

<img width="569" alt="Figure 2025-03-27 191053 (17)" src="https://github.com/user-attachments/assets/488dc30e-229d-43a9-8527-ef94cf6cdaa6" />

<img width="569" alt="Figure 2025-03-27 191053 (18)" src="https://github.com/user-attachments/assets/5d8aeb1a-cf51-41f7-93b7-e773de954ff7" />

calculos estadisticos por ventana y test de hipotesis 

<img width="735" alt="Captura de pantalla 2025-03-27 a la(s) 7 17 36 p m" src="https://github.com/user-attachments/assets/a8292e93-f78e-4ff8-b9df-3baff28326d0" />

<img width="730" alt="Captura de pantalla 2025-03-27 a la(s) 7 18 02 p m" src="https://github.com/user-attachments/assets/1020933d-0686-419f-8e0f-5e4e2006a16d" />


<img width="734" alt="Captura de pantalla 2025-03-27 a la(s) 7 18 14 p m" src="https://github.com/user-attachments/assets/8fbea60d-c114-4a6e-b679-340ece349e57" />

<img width="722" alt="Captura de pantalla 2025-03-27 a la(s) 7 18 27 p m" src="https://github.com/user-attachments/assets/914243fe-b87a-41a6-84af-231ad0d3e4b5" />

<img width="735" alt="Captura de pantalla 2025-03-27 a la(s) 7 18 58 p m" src="https://github.com/user-attachments/assets/7a1bbd23-3cdc-432e-80b3-1145aff319a5" />

















