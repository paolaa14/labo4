Se realizó una práctica de laboratorio para lograr medir y explicar una señal EMG y observar a su vez la fatiga del músculo, pero es necesario comprender unos conceptos muy importantes; 
 - En electromiografía (EMG), los conceptos de respuesta rápida y respuesta lenta se refieren a la velocidad de activación y reclutamiento de las fibras musculares durante una contracción. Estas respuestas están directamente relacionadas con los dos tipos principales de fibras musculares: las de contracción rápida (tipo II) y las de contracción lenta (tipo I).
 - Las fibras musculares tipo II, también conocidas como fibras de contracción rápida, son responsables de movimientos explosivos y de alta intensidad. Estas fibras se activan de manera casi inmediata cuando el cuerpo requiere generar una gran cantidad de fuerza en poco tiempo y las características en la EMG son ; generar señales de alta amplitud, se activan en corta duración, y se fatigan rapidamente por la dependencia del metabplismo anaeróbico para producir enegía.
 - Las fibras musculares tipo I, o fibras de contracción lenta, están diseñadas para mantener una activación prolongada con menor generación de fuerza. Son esenciales para actividades que requieren resistencia y estabilidad, como el mantenimiento de la postura o el ejercicio aeróbico prolongado y las características en la EMG son; generar señales de menor frecuencia y amplitud comparandolas con las fibras rápidas, resisten más a la fatiga y se pueden mantener activas durante más tiempo y su obtención de energía es principalmente por medio del metabolismo aeróbico.

 

Para llevar a cabo esto, inicialmente se realizó la preparación del sujeto de prueba, este se posicionó en una silla para colocarle los electrodos de superficie (es decir que solo se pegan en la piel) en el músculo  Flexor superficial de los dedos que se adhieren bien a la piel por el gel conductor que posee el electrodo, para lograr adquierir la señal de emg y la respectiva fatiga,  se implementó una tarjeta conocida como DAQ, pero a la vez fue necesario descargar un programa de Controlador NI-DAQmx para que el computador la reconociera y se logrará hacer una correcta toma de la señal.

En dado caso de querer descargarlo, se pueden dirigir a la paginal de national instruments (NI) para instalar esto, luego para ejecutar esto en el pythonn(sino se tiene descargado se puede descargar y en nuestro caso en particular estamos usando anaconda y más especificamente spyder), se debe abrir en el terminal, pip install nidaqmx, con el fin de instalar esto en el python y que lo reconozca, posterior a esto, se conecta la tarjeta DAQ al computador y se abre automaticamente el NI MAX, que reconoce esta como un device, con esto claro se procede hacer el código en python que se explicará detalladamente a continuación:



sección del código;
CODIGO de la adquisición de la señal, este código lo pueden copiar y compilar en python, ya que fue con el que adquirimos la señal no obstante para que funcione optimamente tienen que realizar el circuito como se evidenciará más adelante.

import nidaqmx  # Interactúa con dispositivos DAQ para leer datos del sensor EMG
import pandas as pd  # Manipulación de datos científicos, almacenamiento y análisis
import numpy as np  # Cálculos matemáticos y manipulación de arreglos numéricos
import matplotlib.pyplot as plt  # Visualización de datos mediante gráficas
from scipy.signal import find_peaks  # Detección de picos en una señal EMG


def adquirir_datos(fs, cantidad):
    """
    Adquiere datos de la DAQ con la frecuencia de muestreo y cantidad de muestras especificadas.
    :param fs: Frecuencia de muestreo (Hz)
    :param cantidad: Número total de muestras a adquirir
    :return: Lista con los datos adquiridos
    """
    with nidaqmx.Task() as task:
        # Configuración del canal de entrada analógica
        task.ai_channels.add_ai_voltage_chan("Dev4/ai0", min_val=0, max_val=4)
        
        # Configuración del reloj de muestreo
        task.timing.cfg_samp_clk_timing(
            fs,
            sample_mode=nidaqmx.constants.AcquisitionType.FINITE,
            samps_per_chan=cantidad
        )
        
        # Leer datos y expandir cada muestra 6 veces
        return [v for _ in range(6) for v in task.read(cantidad)]


def main():
    """
    Función principal para adquirir, procesar y guardar los datos de la señal EMG.
    """
    try:
        fs, cantidad = 250, 2500  # Frecuencia de muestreo (250 Hz) y cantidad total de muestras (2500)
        data = adquirir_datos(fs, cantidad)  # Adquisición de datos desde la DAQ
        
        # Guardado de datos
        nombre = input("Nombre del archivo: ")
        np.save(f"{nombre}.npy", data)  # Guarda en formato binario Numpy (.npy)
        pd.DataFrame(data).to_csv(f"{nombre}.csv", index=False)  # Guarda en formato CSV
        
        # Detección de picos en la señal EMG
        peaks, _ = find_peaks(data, distance=fs//5, height=0.2)
        
        # Cálculo de frecuencia en BPM si hay más de un pico
        if len(peaks) > 1:
            frecuencia_bpm = round((60 * fs) / np.mean(np.diff(peaks)), 2)
            print(f"Frecuencia estimada: {frecuencia_bpm} BPM")
        
        # Visualización de la señal y los picos detectados
        plt.plot(data)
        plt.plot(peaks, np.array(data)[peaks], 'rx')
        plt.show()
        
    except Exception as e:
        print(f"Error: {e}")  # Manejo de errores


if __name__ == "__main__":
    main()  # Ejecutar la función principal si el script se ejecuta directamente




A su vez, se conectaron los electrodos al sensor emg, que permitirá captar bien la señal muscular, teniendo claro que el músculo que elegimos, en la parte del antebrazo, el flexor superficial, se realiza un cálculo de la frecuencia de muestreo para realizar la captura de la señal.



![WhatsApp Image 2025-03-27 at 11 48 14](https://github.com/user-attachments/assets/670f57d2-f976-427d-a5ca-7744fa0e4679)

Imagen 1. Cómo se colocaron los electrodos en el paciente 


2. Para continuar, el sujero ya estando conectado se le pidió realizar primero el movimiento de apretar una pelota antiestres para llegar a la contracción con mayor facilidad, entonces se le pidió que realizará la contracción del músculo mencionado y se registra la señal por medio el código de python.


<img width="609" alt="Figure 2025-03-27 111639" src="https://github.com/user-attachments/assets/b6fc20c2-1ca5-49aa-bca3-ce419dd2c262" />

Imagen 2. Señal emg del músculo

Antes de iniciar con el análisis de la gráfica es necesario mencionar que esta gráfica contiene detalles especificos sobre la frecuencia de muestreo(250 Hz), tiempo de grabación (40 SEGUNDOS, eso también se puede elegir pero según la explicación de las fibras rápidas, determinamos que en este tiempo se capturaban las contracciones necesarias para llegar a la fatiga), longitud de la señal (40.000), número de contracciones  (17 contracciones) y el músculo medido (el músculo  Flexor superficial de los dedos).

En esta gráfica se evidencia como quedó la captura de la señal emg, del músculo mencionado previamente, que muestra  la actividad del músculo, donde se incluye la contracción, relajación y fatiga,  en esta imagen en particular, observamos que que hay cambios grandes en la amplitud de la señal, es decir que hay niveles de actividad muscular, asimismo, para llevar a cabo un análisis más claro, identificaremos las fases por las que pasa la gráfica;
 
  En primer lugar, la fase de contracción donde se observan segmentos que la amplitud aumenta de manera signifcativa, representando la activación de las fibras musculares en rerspuesta a la contraciión que se esta haciendo de manera voluntaria, y se observa en algunos puntos más intensidad y duración, lo que indica que al ser voluntaria estos dos factores dependen de la persona que esta haciendo la contracción.
 
  En segundo lugar, la fase de relajación, no se observa completamente, debido a que se presentaron movimientos involuntarios donde se movió el brazo.
 
Por último, la fase de fatiga es la parte final de la señal que parece mantener cierta actividad sin volver completamente al reposo, y durante esta fase la actividad electrica del músculo cambia y pueden aparecer frecuencias más bajas por la reducción en la capacidad de generar fuerza.




3. Posterior a esto, se aplica un filtro a la señal pasa alta, con el fin de eliminar componentes de baja frecuencia (ruido que se asocie al movimiento), y a su vez se implementó un filtro pasa baja para quitar frecuencias altas como el ruido electromagnético.


Imagen 3. señal filtrada pasa alto y pasa bajo


<img width="617" alt="Figure 2025-03-27 191053 (1)" src="https://github.com/user-attachments/assets/76f5872d-b4a2-4559-a0e5-9c26f504154b" />



![WhatsApp Image 2025-03-27 at 23 14 35](https://github.com/user-attachments/assets/53952ef3-e2c8-46e9-b54a-9f0c087bf4a7)


El filtro fue diseñado considerando los parámetros estudiados en clase, asegurando una correcta eliminación de ruido y preservación de la señal de interés. Se establecieron frecuencias de corte de 20 Hz (pasa alto) y 450 Hz (pasa bajo), con una frecuencia de muestreo de 1000 Hz. Se aplicó una ventana de Hanning para minimizar el efecto de Gibbs, y el orden del filtro fue calculado en función del ancho de la banda de transición. La ecuación de la respuesta al impulso  ℎ(𝑛) se fundamenta en la función sinc, ajustada con la ventana de Hanning.
   
4. Es necesario mencionar, que para captar un pedazo de la señal que resultara analizable, se implementó una ventana, para observar determinado pedazo de la señal. y se le realizará un análisis espectral implementando la transformada de fourier para obtener el espectro de frecuencas en intervalos determinados de la señal EMG.


En el procesamiento de la señal EMG, se aplica una ventana de Hanning a cada segmento seleccionado. La elección de este tipo de ventana se debe a su capacidad para reducir las discontinuidades en los extremos de los segmentos, minimizando el efecto de fuga espectral en la Transformada de Fourier. La ventana de Hanning es una función suave, definida matemáticamente como:

w(n)=0.5(1−cos(2πn/ N−1))
donde 𝑁 es la longitud del segmento y  𝑛 representa las muestras dentro del segmento.

En este código, el tamaño de la ventana se define en 2000 muestras, lo que permite capturar adecuadamente la estructura de las contracciones musculares sin perder información significativa. Antes de aplicar la ventana, la señal original de cada segmento presenta transiciones bruscas en los extremos. Sin embargo, tras la convolución con la ventana de Hanning, la señal se atenúa progresivamente en los bordes, reduciendo artefactos no deseados en el análisis espectral.

Para visualizar el impacto de la ventana, se pueden graficar tanto la señal original del segmento como la señal tras la aplicación de la ventana. Esto permite comparar cómo cambia la amplitud y la forma de la señal después de la convolución. La superposición de ambas señales ayuda a evidenciar la reducción de efectos no deseados en la estimación del espectro de frecuencias.


ventanas por contracciones (17) con su respectivo espectro 

Imagen 4. CONTRACCIÓN Y ESPECTRO 1.

<img width="569" alt="Figure 2025-03-27 191053 (2)" src="https://github.com/user-attachments/assets/8e27e4c9-142e-4eb3-993a-43c2ff532b90" />

- En esta gráfica se evidencia , en el eje horizontal se representa el tiempo en muestras, mientras que en el eje vertical se muestra la amplitud de la señal EMG.
Inicialmente, la señal tiene una amplitud muy baja (cercana a 0), lo que indica un estado de reposo o baja actividad muscular. A partir de aproximadamente la muestra 500, la amplitud de la señal aumenta y presenta oscilaciones más pronunciadas, lo que sugiere la activación del músculo y una contracción sostenida.
- La señal es de naturaleza oscilatoria y caótica, lo cual es típico en registros EMG debido a la combinación de múltiples unidades motoras activándose simultáneamente.
Gráfica inferior: Espectro de frecuencia de la señal EMG. En el eje horizontal se representa la frecuencia en Hz, mientras que en el eje vertical se muestra la magnitud de la señal en el dominio de la frecuencia.

Para la parte del espectro;
- Se observa que la mayor concentración de energía se encuentra en frecuencias bajas, aproximadamente entre 0 y 100 Hz. Esto es característico de señales EMG, donde la mayor parte del contenido útil suele estar por debajo de los 150 Hz.
A partir de los 100 Hz, la magnitud de la señal decrece rápidamente, lo que indica que hay poca energía en frecuencias más altas. No se observan picos muy marcados en altas frecuencias, lo cual sugiere que no hay interferencias de alta frecuencia o ruido significativo en la señal.


Imagen 5. CONTRACCIÓN Y ESPECTRO 2.

<img width="569" alt="Figure 2025-03-27 191053 (3)" src="https://github.com/user-attachments/assets/851216c1-e66e-40e5-a4f1-4ca716f5a00d" />

- En esta gráfica, al inicio, la señal presenta oscilaciones de alta amplitud, lo que sugiere una fuerte activación muscular, mientras que hacia el final de la señal, la amplitud disminuye, lo que indica la relajación progresiva del músculo.
- Alrededor de la muestra 1000, hay una caída abrupta, posiblemente un artefacto o una transición brusca en la contracción.

 Para la parte del espectro;
- La mayor concentración de energía se encuentra en las frecuencias bajas, principalmente por debajo de los 100 Hz, hay una disminución progresiva en la magnitud conforme aumenta la frecuencia. Esto es característico de las señales EMG, ya que la mayor parte de la información relevante se encuentra en el rango de 20 a 150 Hz, dependiendo del tipo de músculo y la intensidad de la contracción.
- La presencia de ruido o actividad de alta frecuencia parece ser mínima, lo cual sugiere que la señal ha sido correctamente filtrada.


Imagen 6.CONTRACCIÓN Y ESPECTRO 3.

<img width="569" alt="Figure 2025-03-27 191053 (4)" src="https://github.com/user-attachments/assets/f7086e05-d30b-4c12-b835-801cff2b9e67" />


- En esta gráfica, en las primeras 500 muestras, la señal es prácticamente nula, lo que sugiere que el músculo estaba en reposo antes de la contracción. A partir de aproximadamente la muestra 750, se observa un aumento progresivo en la actividad EMG, con oscilaciones de mayor amplitud. La fase de contracción parece ser más prolongada y consistente en comparación con la "Contracción 2", lo que sugiere una activación muscular más sostenida. A diferencia de la "Contracción 2", aquí no se observa una caída abrupta en la señal.

 Para la parte del espectro;
- Se observa un pico predominante por debajo de los 50 Hz, lo que es característico de una señal EMG limpia y sin ruido de alta frecuencia. La mayor concentración de energía se encuentra entre 20 y 100 Hz, lo que es típico en señales EMG de contracciones musculares voluntarias. En comparación con la "Contracción 2", la magnitud máxima es un poco mayor, lo que puede indicar una contracción más intensa o sostenida.No hay presencia significativa de frecuencias altas, lo que sugiere que la señal está bien filtrada y sin artefactos eléctricos.


Imagen 7. CONTRACCIÓN Y ESPECTRO 4.

<img width="569" alt="Figure 2025-03-27 191053 (5)" src="https://github.com/user-attachments/assets/d1a9986a-98a0-44e6-812a-342e8c6a43b4" />

- En esta gráfica, se observa actividad muscular desde el inicio (aproximadamente en la muestra 100), lo que sugiere que la contracción comenzó antes que en las gráficas anteriores. La amplitud de la señal es relativamente constante y con una gran densidad de picos a lo largo del tiempo, indicando una contracción mantenida.
En comparación con las contracciones anteriores, esta presenta una actividad más continua y sin pausas evidentes.

Para la parte del espectro;
- Se observa un pico predominante en la región de 0 a 50 Hz, lo cual es característico de señales EMG. La concentración de energía entre 20 y 100 Hz sigue el mismo patrón que las contracciones anteriores. La magnitud del pico máximo es menor que en la "Contracción 3", pero sigue dentro del rango típico para una contracción voluntaria. No se observan picos en altas frecuencias, lo que indica que la señal está bien filtrada y libre de ruido.
  

Imagen 8. CONTRACCIÓN Y ESPECTRO 5.

<img width="569" alt="Figure 2025-03-27 191053 (6)" src="https://github.com/user-attachments/assets/8cfaf68f-4938-48f3-a734-95340fb8d91a" />

- En esta gráfica, la contracción comienza cerca de la muestra 100 y se mantiene hasta aproximadamente la muestra 1500.Se observa una disminución progresiva en la actividad después de la muestra 1300, lo que podría indicar fatiga muscular o el final voluntario de la contracción. Comparado con las contracciones anteriores, esta presenta una reducción más evidente en la amplitud en la fase final.

 Para la parte del espectro;
- Se observa un pico predominante en la región de 0 a 50 Hz, lo cual es típico en señales EMG. La distribución de energía es similar a la de la "Contracción 4", pero la magnitud de los picos es mayor, indicando posiblemente una mayor intensidad en la actividad muscular. Se mantiene una concentración de energía entre 20 y 100 Hz, sin componentes significativas en frecuencias más altas.

  

Imagen 9. CONTRACCIÓN Y ESPECTRO 6.

<img width="569" alt="Figure 2025-03-27 191053 (7)" src="https://github.com/user-attachments/assets/cbe3ac83-92c9-4d24-9c2e-03c3df24f3c3" />

- En esta gráfica, se observa una actividad intensa en los primeros 800-1000 puntos, con variaciones rápidas y una amplitud mayor. Posteriormente, la señal se estabiliza y muestra un comportamiento con menor amplitud, lo que sugiere relajación muscular tras la contracción.

Para la parte del espectro; 
- Representa la Transformada de Fourier de la señal EMG, es decir, cómo se distribuyen sus componentes en frecuencia. El eje X muestra la frecuencia en Hz, mientras que el eje Y representa la magnitud de cada frecuencia.
- Se observa que la mayor parte de la energía de la señal está concentrada en el rango de 0 a 100 Hz, con picos más marcados entre 0 y 50 Hz. Después de 100 Hz, la magnitud de la señal cae abruptamente, indicando que la mayor parte de la información relevante está en las frecuencias bajas e intermedias.



Imagen 10. CONTRACCIÓN Y ESPECTRO 7.

<img width="569" alt="Figure 2025-03-27 191053 (8)" src="https://github.com/user-attachments/assets/6780977f-f3f9-4eb9-947f-1312d52bea22" />

-Esta gráfica, se observa un periodo inicial de baja actividad (hasta ~600 muestras), seguido de una contracción activa que aumenta en intensidad y persiste hasta el final de la muestra.Comparado con la contracción 6, esta señal parece más sostenida y con una amplitud ligeramente mayor en la segunda mitad del registro.

Para la parte del espectro;
- Muestra la Transformada de Fourier de la señal EMG, representando las frecuencias predominantes. La mayor parte de la energía se encuentra en el rango de 0 a 100 Hz, con picos más pronunciados entre 0 y 50 Hz.
- Se observa una magnitud de frecuencia más elevada (~50) en comparación con la contracción 6 (~30), lo que indica una mayor intensidad en las componentes de alta frecuencia. A partir de los 100 Hz, la magnitud disminuye rápidamente, indicando que las frecuencias dominantes están en el rango bajo e intermedio.


Imagen 11. CONTRACCIÓN Y ESPECTRO 8.

<img width="569" alt="Figure 2025-03-27 191053 (9)" src="https://github.com/user-attachments/assets/4fff6596-9acc-4cd4-a97f-7e8fb88dde97" />

En esta gráfica, se observa una fase inicial con baja actividad (~0 a 200 muestras), seguida de una fase de contracción activa (~200 a 1200 muestras), y una fase de relajación (~1200 en adelante). En comparación con las contracciones anteriores, esta señal parece más irregular en su amplitud, con picos más altos (~1.0) en ciertos momentos. Después de la muestra 1200, la señal disminuye rápidamente en amplitud, indicando el final de la contracción.

Para la parte de espectro;
Se observa que la mayor parte de la energía está concentrada entre 0 y 100 Hz, con un pico fuerte alrededor de 50-60 Hz. En comparación con las contracciones anteriores, la magnitud máxima del espectro es más alta (~60), lo que sugiere una mayor intensidad en estas frecuencias. A partir de 100 Hz, la magnitud disminuye rápidamente, mostrando una menor contribución de las frecuencias altas.



Imagen 12. CONTRACCIÓN Y ESPECTRO 9.

<img width="569" alt="Figure 2025-03-27 191053 (10)" src="https://github.com/user-attachments/assets/8a3989d2-c624-4dca-9f11-19c9eec87d5a" />

- En esta gráfica, se observa una fase inicial de reposo (~0 a 900 muestras) sin actividad significativa. A partir de la muestra 900, comienza la contracción, con un incremento gradual en la amplitud. La fase de contracción se extiende hasta el final de la señal (~2000 muestras), con oscilaciones de amplitud que llegan hasta ±1.0. En comparación con la contracción 8, esta señal tiene una activación más tardía pero parece más sostenida.

Para la parte de espectro; 
- La mayor parte de la energía está concentrada entre 0 y 100 Hz, con picos importantes cerca de 50 Hz. La magnitud máxima del espectro es ~50, similar a la contracción 7, pero menor que la contracción 8 (~60). A partir de 100 Hz, la magnitud disminuye rápidamente, con valores casi nulos más allá de 200 Hz.


Imagen 13. CONTRACCIÓN Y ESPECTRO 10.

<img width="569" alt="Figure 2025-03-27 191053 (11)" src="https://github.com/user-attachments/assets/dae943bb-e27f-4aa9-8d70-00caf78e6924" />

En esta gráfica, se muestra la actividad comienza alrededor de las 200 muestras, con un incremento progresivo de la amplitud. La fase de contracción más intensa ocurre entre 400 y 1200 muestras, con picos que alcanzan aproximadamente ±1.0.
Después de las 1200 muestras, la amplitud comienza a disminuir gradualmente hasta estabilizarse cerca de las 1750 muestras.Comparada con las contracciones anteriores, esta parece más simétrica en su activación y relajación.

Para la parte de espectro;
La mayor parte de la energía está concentrada entre 0 y 100 Hz, con picos significativos en torno a 50-60 Hz.La magnitud máxima en este espectro es ~70, la más alta hasta ahora en comparación con las contracciones previas. A partir de 100 Hz, la magnitud disminuye progresivamente, manteniendo valores bajos después de 200 Hz.


Imagen 14. CONTRACCIÓN Y ESPECTRO 11.

<img width="569" alt="Figure 2025-03-27 191053 (12)" src="https://github.com/user-attachments/assets/6ce3c6ea-c6c9-445e-b51f-8e3c8347be5e" />

- En esta gráfica, se observa la señal comienza con oscilaciones de baja amplitud cercanas a 0, lo que sugiere un estado de reposo inicial del músculo.
Aproximadamente desde la muestra 100, la señal empieza a aumentar su amplitud, indicando el inicio de la contracción muscular.
El pico máximo de amplitud ocurre alrededor de la muestra 500, con valores que oscilan entre -1 y 1, reflejando una contracción fuerte y sostenida.
Hacia la muestra 1000, la amplitud comienza a decrecer progresivamente hasta estabilizarse nuevamente en valores cercanos a 0, lo que indica la relajación del músculo. La forma de la señal sugiere una contracción rápida con una disminución controlada, lo que podría estar relacionado con una fatiga moderada del músculo.


Para la parte del espetro;
-Se observa una mayor concentración de energía en las frecuencias bajas, principalmente entre 0 y 100 Hz, lo cual es característico de señales EMG en contracciones musculares normales. El pico dominante está alrededor de los 50 Hz, lo que indica que la mayor actividad eléctrica del músculo ocurre en esa frecuencia. A partir de los 100 Hz, la energía del espectro decae rápidamente, con valores casi nulos después de los 200 Hz, lo que es esperable en señales EMG donde las altas frecuencias suelen estar más asociadas a ruido que a información útil.



Imagen 15. CONTRACCIÓN Y ESPECTRO 12.

<img width="569" alt="Figure 2025-03-27 191053 (13)" src="https://github.com/user-attachments/assets/43253198-5f5a-4dc9-a066-dcd5050947c0" />


- En esta gráfica, la señal comienza en reposo, con valores cercanos a 0 hasta aproximadamente la muestra 1000.A partir de la muestra 1000, la amplitud de la señal aumenta rápidamente, indicando el inicio de la contracción muscular.
En comparación con la Contracción 11, esta señal muestra un incremento más gradual de la amplitud y un mayor número de oscilaciones de alta frecuencia. La amplitud alcanza su máximo alrededor de la muestra 1500 y se mantiene elevada hasta cerca de la muestra 1750. Luego, la señal empieza a decaer paulatinamente, lo que sugiere una relajación más progresiva del músculo en comparación con la Contracción 11.
La forma de la señal sugiere que esta contracción podría haber requerido más esfuerzo o haber sido mantenida por más tiempo.

- Para la parte de espectro;
Al igual que en la Contracción 11, la mayor parte de la energía está concentrada en el rango 0-100 Hz, con un pico dominante en torno a 50 Hz. Se observa un patrón de distribución de energía más amplio en comparación con la Contracción 11, lo que indica la presencia de más componentes de alta frecuencia. A partir de los 100 Hz, la energía decae de manera más gradual en comparación con la señal anterior, lo que sugiere una mayor variabilidad en la contracción muscular.



Imagen 16. CONTRACCIÓN Y ESPECTRO 13.

<img width="569" alt="Figure 2025-03-27 191053 (14)" src="https://github.com/user-attachments/assets/ca08fc91-c744-4499-8cbe-d6c80d3a867d" />


- En esta gráfica se muestra la fase inicial (0-250 muestras): La señal se mantiene cerca de 0, indicando un estado de reposo muscular antes de la contracción. Inicio de la contracción (250-500 muestras): La amplitud comienza a aumentar gradualmente, mostrando una activación progresiva del músculo. Fase de contracción máxima (500-1750 muestras): Se observa una oscilación sostenida con amplitudes variables, lo que sugiere una contracción continua y posiblemente una variación en la activación de las fibras musculares. Relajación (1750-2000 muestras): La amplitud comienza a disminuir, indicando la relajación del músculo después de la contracción.
Comparación con contracciones anteriores: Esta señal muestra una activación más irregular con amplitudes variables, lo que podría reflejar un esfuerzo menos constante o un mayor nivel de fatiga en el músculo.


Para la parte del espectro;
- Distribución de energía: La mayor concentración de energía se encuentra en el rango 0-100 Hz, lo cual es típico en señales EMG. Pico dominante: Se encuentra cerca de 50 Hz, indicando que la mayor actividad muscular se presenta en esta frecuencia.
Disminución progresiva: A partir de los 100 Hz, la energía del espectro comienza a descender rápidamente, con valores casi nulos después de los 200 Hz. Comparación con espectros anteriores: Esta señal presenta una mayor variabilidad en las frecuencias bajas, lo que podría estar relacionado con cambios en la activación muscular durante la contracción. También se observa una mayor dispersión de la energía en comparación con la Contracción 11, lo que puede ser indicativo de una mayor activación de fibras musculares o de una contracción más inestable.



Imagen 17. CONTRACCIÓN Y ESPECTRO 14.

<img width="569" alt="Figure 2025-03-27 191053 (15)" src="https://github.com/user-attachments/assets/6ed15224-8351-49e2-8e2b-bd28fd41b725" />


Fase inicial (0-100 muestras): Presenta valores bajos, lo que indica un estado de reposo antes de la activación muscular.Inicio de la contracción (100-250 muestras): Se observa un aumento en la amplitud, lo que marca el comienzo de la actividad muscular.Fase de contracción máxima (250-1250 muestras): Hay una oscilación sostenida con picos relativamente altos, reflejando una contracción mantenida con posibles variaciones en la intensidad.Descenso de actividad (1250-1500 muestras): Se observa una disminución progresiva en la amplitud, lo que indica el inicio de la relajación muscular.Relajación (1500-2000 muestras): La amplitud disminuye significativamente, mostrando que el músculo regresa a un estado de reposo.
Comparación con otras contracciones: En comparación con la Contracción 13, esta señal parece presentar una contracción menos sostenida en el tiempo y una relajación más progresiva.


Para la parte de espectro;
Distribución de energía: La mayor parte de la energía se encuentra en el rango 0-100 Hz, lo cual es característico de señales EMG. Pico dominante: Se encuentra cerca de 50 Hz, lo que es común en señales de actividad muscular.
Disminución de energía: A partir de los 100 Hz, la magnitud cae rápidamente, con valores muy bajos más allá de los 200 Hz. Comparación con otras contracciones: Presenta un patrón de frecuencia similar a la Contracción 13, pero con una distribución de energía más concentrada en los primeros 100 Hz, lo que sugiere una activación más estable del músculo.


Imagen 18. CONTRACCIÓN Y ESPECTRO 15.

<img width="569" alt="Figure 2025-03-27 191053 (16)" src="https://github.com/user-attachments/assets/b3305a7a-38c4-4e38-a7ac-c6f8c0609a74" />


Fase inicial (0-800 muestras): Se observa un período prolongado de reposo con baja amplitud, lo que indica inactividad muscular. Inicio de la contracción (800-1000 muestras): La amplitud comienza a aumentar progresivamente, señalando la activación del músculo. Fase de contracción máxima (1000-1800 muestras): Se presenta una oscilación con alta amplitud, mostrando una contracción sostenida con variabilidad en la intensidad de los picos. Fase de relajación (1800-2000 muestras): Se observa una disminución en la amplitud, lo que indica que el músculo regresa a su estado de reposo. Comparación con otras contracciones: En comparación con la Contracción 13 y 14, esta contracción inicia más tarde y parece tener una duración menor en su fase activa, pero con picos de mayor amplitud.


Para la parte del espectro;
Distribución de energía: La mayor parte de la energía se concentra entre 0 y 100 Hz, lo que es característico de las señales EMG.
Pico dominante: Se encuentra en torno a 50-60 Hz, lo que coincide con la actividad neuromuscular esperada.Disminución de energía: A partir de los 100 Hz, la magnitud cae rápidamente y se mantiene en valores bajos después de los 200 Hz.
Comparación con otras contracciones: Esta señal tiene un pico de mayor magnitud en comparación con las anteriores, lo que sugiere una activación muscular más intensa o con mayor esfuerzo.


Imagen 19. CONTRACCIÓN Y ESPECTRO 16.

<img width="569" alt="Figure 2025-03-27 191053 (17)" src="https://github.com/user-attachments/assets/488dc30e-229d-43a9-8527-ef94cf6cdaa6" />


Fase inicial (0-250 muestras): Presenta una actividad basal con amplitudes bajas, lo que indica que el músculo está en reposo.
Inicio de la contracción (250-500 muestras): Se observa un incremento progresivo en la amplitud de la señal, reflejando el inicio de la activación muscular.
Fase de contracción máxima (500-1250 muestras): Durante este intervalo, la señal presenta oscilaciones con amplitud significativa, lo que sugiere una contracción sostenida con variabilidad en la intensidad.
Fase de relajación (1250-2000 muestras): La amplitud comienza a disminuir hasta acercarse nuevamente a valores bajos, lo que indica que el músculo regresa a su estado de reposo. Comparación con otras contracciones: Esta contracción muestra una activación temprana y sostenida con una fase de relajación más definida en comparación con las anteriores.


Para la parte del espectro; 
Distribución de energía: La mayor parte de la energía se concentra entre 0 y 100 Hz, lo cual es típico en señales EMG.Pico dominante: Se observa un pico de alta magnitud en torno a 50-60 Hz, lo que indica la presencia de una activación muscular fuerte.
Magnitud máxima: Es una de las señales con mayor magnitud observada hasta el momento, lo que podría estar relacionado con una contracción más intensa o prolongada.
Disminución de energía: A partir de los 100 Hz, la magnitud cae rápidamente y se mantiene baja después de los 200 Hz. Comparación con otras contracciones: El pico de energía en esta señal es más alto en comparación con las contracciones 13, 14 y 15, lo que podría indicar una mayor activación neuromuscular o una contracción más fuerte y estable.


Imagen 20. CONTRACCIÓN Y ESPECTRO 17.

<img width="569" alt="Figure 2025-03-27 191053 (18)" src="https://github.com/user-attachments/assets/5d8aeb1a-cf51-41f7-93b7-e773de954ff7" />

Análisis de la señal EMG (Contracción 17)
Fase inicial (0-100 muestras): Se observa una activación temprana con oscilaciones de amplitud moderada, lo que indica el inicio de la contracción.
Pico de actividad (100-600 muestras): La amplitud alcanza su máximo con oscilaciones más densas y fuertes, reflejando la fase de contracción más intensa.
Fase de relajación (600-1250 muestras): Se nota una disminución gradual en la amplitud, lo que sugiere que el músculo está relajándose.
Reposo final (1250-2000 muestras): La señal vuelve a una actividad mínima, indicando el término de la contracción. Comparación con otras contracciones: Esta contracción tiene una duración activa más corta y una relajación más rápida en comparación con la contracción 16.

Para la parte del espectro;
Distribución de energía: La mayor parte de la energía se encuentra en el rango de 0-100 Hz, lo que es común en señales EMG. Pico de frecuencia dominante: Se presenta en torno a 50-60 Hz, lo cual puede deberse a la activación neuromuscular o a interferencia de la red eléctrica. Magnitud máxima: Menor en comparación con la contracción 16, lo que indica una menor intensidad de la contracción.
Rápida disminución de energía: La señal pierde energía rápidamente después de los 100 Hz, lo que sugiere una menor presencia de componentes de alta frecuencia.



5. Luego a todo esto, se observará como cambia el espectro se la señal en cada ventana mientras más se acerque  a la fatiga muscular, para evaluar la disminución de la frecuencia mediana en cada ventana como indicador de la fatiga, por último se implementa una prueba de hipótesis para verificar si el cambio en la mediana tiene un valor significativo en la estadistíca.


calculos estadisticos por ventana y test de hipotesis 



<img width="735" alt="Captura de pantalla 2025-03-27 a la(s) 7 17 36 p m" src="https://github.com/user-attachments/assets/a8292e93-f78e-4ff8-b9df-3baff28326d0" />


<img width="730" alt="Captura de pantalla 2025-03-27 a la(s) 7 18 02 p m" src="https://github.com/user-attachments/assets/1020933d-0686-419f-8e0f-5e4e2006a16d" />


<img width="734" alt="Captura de pantalla 2025-03-27 a la(s) 7 18 14 p m" src="https://github.com/user-attachments/assets/8fbea60d-c114-4a6e-b679-340ece349e57" />

<img width="722" alt="Captura de pantalla 2025-03-27 a la(s) 7 18 27 p m" src="https://github.com/user-attachments/assets/914243fe-b87a-41a6-84af-231ad0d3e4b5" />


<img width="730" alt="Captura de pantalla 2025-03-27 a la(s) 11 03 52 p m" src="https://github.com/user-attachments/assets/adc64868-c39c-4d63-bf82-de36c0fed371" />

- se procederá a hacer el análisis de los valores obtenidos;
En el análisis de señales, la aplicación de ventanas es fundamental para minimizar efectos indeseados en el dominio de la frecuencia, como la fuga espectral. En este caso, se ha utilizado una ventana de Hann, seleccionada por su capacidad de reducir los lóbulos laterales en el espectro, lo que permite una mejor resolución de las componentes de frecuencia.

Criterio de selección: Se eligió la ventana de Hann porque proporciona una atenuación gradual en los extremos de la señal, lo que minimiza discontinuidades y mejora la precisión del análisis espectral.

Tamaño de la ventana: La ventana aplicada tiene un tamaño de N  muestras, asegurando que cada segmento analizado tenga suficiente resolución en el dominio de la frecuencia sin introducir distorsiones significativas.

Forma de la ventana: La ventana de Hann sigue una función senoidal elevada al cuadrado, suavizando la señal antes del análisis espectral.

Se ha comparado la señal antes y después de la aplicación de la ventana. Antes de la convolución, la señal presenta discontinuidades en los límites de los segmentos, lo que podría generar ruido en el espectro. Tras la aplicación de la ventana, las transiciones son más suaves, reduciendo la contribución de frecuencias no deseadas.

- Para el analisis e interpretación de resultados: 

Se han extraído estadísticas espectrales de 17 segmentos de la señal, analizando frecuencia dominante, mediana, media y desviación estándar. A continuación, se realiza una evaluación de estos valores:

Frecuencia Dominante: Representa la frecuencia con mayor energía en cada segmento.

Frecuencia Mediana: Divide el espectro en dos partes de igual energía.

Frecuencia Media: Valor promedio de las frecuencias presentes en el segmento.

Desviación Estándar: Indica la dispersión de las frecuencias en el espectro.

- Análisis por Segmentos:

Los segmentos presentan una media de frecuencias entre 49.60 Hz y 63.30 Hz, con variaciones significativas en ciertos segmentos, especialmente en el segmento 8, donde la frecuencia media alcanza 63.30 Hz con una desviación estándar alta de 59.88 Hz, lo que indica una gran dispersión en las frecuencias. Esto puede estar relacionado con la presencia de señales transitorias o ruido en esa región.

La frecuencia dominante varía entre 26.50 Hz y 51.50 Hz, lo que sugiere que algunos segmentos tienen mayor concentración de energía en frecuencias más bajas, mientras que otros presentan picos más altos.

Los segmentos 6, 9 y 10 presentan frecuencias dominantes bajas (26.50 Hz - 32.50 Hz), lo que podría indicar cambios en la dinámica de la señal.

La desviación estándar en varios segmentos supera 30 Hz, lo que indica una gran dispersión en el contenido espectral, reflejando variaciones en la estabilidad de la señal analizada.

- Prueba de Hipótesis sobre la Media de Frecuencia:
Hipótesis Nula (H₀): La media de la frecuencia no es significativamente diferente de 50 Hz.
Hipótesis Alternativa (H₁): La media de la frecuencia es significativamente diferente de 50 Hz.

- Se obtuvo un estadístico t = 0.9415 y un valor p = 0.5192, lo que indica que no hay suficiente evidencia estadística para rechazar la hipótesis nula. Esto significa que, en términos generales, la media de la frecuencia no difiere significativamente de 50 Hz, aunque algunos segmentos individuales presenten variaciones.



El análisis del rango de frecuencias revela que las señales oscilan entre 24 Hz y 450 Hz. Para determinar la fatiga en la señal, se considera la diferencia entre las medias de frecuencia en diferentes segmentos:

Si Media 1 - Media 2 = 0, se concluye que existe fatiga nula, lo que indica estabilidad en la señal.

Si Media 1 - Media 2 ≠ 0, se detecta fatiga alternante, lo que sugiere una variabilidad en la carga o el comportamiento dinámico del sistema analizado.






6. Conclusiones generales;
La aplicación de la ventana de Hann mejoró la calidad del análisis espectral, reduciendo fugas espectrales y mejorando la resolución en frecuencia.

Aunque existen variaciones en algunos segmentos, el análisis estadístico indica que la media de la frecuencia no es significativamente diferente de 50 Hz en términos globales.

Se identificaron diferencias entre segmentos, lo que sugiere que la señal puede experimentar períodos de fatiga alternante en ciertos momentos.

La desviación estándar elevada en algunos segmentos sugiere que existen momentos de inestabilidad en la frecuencia.









