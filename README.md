Se realizó una práctica de laboratorio para lograr medir y explicar una señal EMG, para llevar a cabo esto, inicialmente se realizó la preparación del sujeto de prueba, este se posicionó en una silla para colocarle los electrodos de superficie (es decir que solo se pegan en la piel)en el músculo  Flexor superficial de los dedos que se adhieren bien a la piel por el gel conductor que posee el electrodo, para lograr adquierir la señal de emg, se implementó una tarjeta conocida como DAQ,pero a la vez fue necesario descargar un programa de Controlador NI-DAQmx para que el computador la reconociera y se logrará hacer una correcta toma de la señal.

En dado caso de querer descargarlo, se pueden dirigir a la paginal de national instruments (NI) para instalar esto, luego para ejecutar esto en el python, se debe abrir en el terminal, pip install nidaqmx, con el fin de instalar esto en el python y que lo reconozca, posterior a esto, se conecta la tarjeta DAQ al computador y se abre automaticamente el NI MAX, que reconoce esta como un device, con esto claro se procede hacer el código en python que se explicará detalladamente a continuación:



  
