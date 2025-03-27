Se realizó una práctica de laboratorio para lograr medir y explicar una señal EMG y observar a su vez la fatiga del músculo, para llevar a cabo esto, inicialmente se realizó la preparación del sujeto de prueba, este se posicionó en una silla para colocarle los electrodos de superficie (es decir que solo se pegan en la piel) en el músculo  Flexor superficial de los dedos que se adhieren bien a la piel por el gel conductor que posee el electrodo, para lograr adquierir la señal de emg y la respectiva fatiga,  se implementó una tarjeta conocida como DAQ, pero a la vez fue necesario descargar un programa de Controlador NI-DAQmx para que el computador la reconociera y se logrará hacer una correcta toma de la señal.

En dado caso de querer descargarlo, se pueden dirigir a la paginal de national instruments (NI) para instalar esto, luego para ejecutar esto en el pythonn(sino se tiene descargado se puede descargar y en nuestro caso en particular estamos usando anaconda y más especificamente spyder), se debe abrir en el terminal, pip install nidaqmx, con el fin de instalar esto en el python y que lo reconozca, posterior a esto, se conecta la tarjeta DAQ al computador y se abre automaticamente el NI MAX, que reconoce esta como un device, con esto claro se procede hacer el código en python que se explicará detalladamente a continuación:




CODIGO:




A su vez, se conectaron los electrodos al sensor emg, que permitirá captar bien la señal muscular, teniendo claro que el músculo que elegimos, en la parte del antebrazo, el flexor superficial, se realiza un cálculo de la frecuencia de muestreo para realizar la captura de la señal.

2. Para continuar, el sujero ya estando conectado se le pidió realizar primero el movimiento de apretar una pelota antiestres para llegar a la contracción con mayor facilidad, entonces se le pidió que realizará la contracción del músculo mencionado y se registra la señal por medio el código de python.


<img width="609" alt="Figure 2025-03-27 111639" src="https://github.com/user-attachments/assets/b6fc20c2-1ca5-49aa-bca3-ce419dd2c262" />




3. Poaterior a esto, se aplica un filtro a la señal pasa alta, con el fin de eliminar componentes de baja frecuencia (ruido que se asocie al movimiento), y asu vez se implementó un filtro pasa baja para quitar frecuencias altas como el ruidp electromagnético.



   aqui con filtro
4. Es necesario mencionar, que para captar un pedazo de la señal que resultara analizable, se implementó una ventana, para observar determinado pedazo de la señal. y se le realizará un análisis espectral implementando la transformada de fourier para obtener el espectro de frecuencas en intervalos determinados de la señal EMG.




5. Luego a todo esto, se observará como cambia el espectro se la señal en cada ventana mientras más se acerque  a la fatiga muscular, para evaluar la disminución de la frecuencia mediana en cada ventana como indicador de la fatiga, por último se implementa una prueba de hipótesis para verificar si el cambio en la mediana tiene un valor significativo en la estadistíca.



La mediana se calcula con la formmula








