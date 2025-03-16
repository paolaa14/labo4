En este laboratorio se realizó un evento tipo coctel en una aula insonorizada, se instalaron varios micrófonos en distintos lugares para escuchar inicialmente el ruido ambiente, posterior se grabaron las voces de 2 sujetos para saber que era lo que estaban diciendo; una vez terminó la fiesta, se solicitó a los ingenieros que entregaran el audio de la voz de uno de los participantes.

Posterior , se analizaron las voces grabadas por los microfonos que eran mezclas de señales que provenían de diferentes fuentes (personas) para todos los casos y se encontraron con el problema de aislar la voz de interés. El problema de la "fiesta de cóctel" se refiere a la capacidad de un sistema para concentrarse en una sola fuente sonora mientras filtra las demás en un entorno con múltiples emisores de sonido. Este problema es común en sistemas de audición tanto humanos como artificiales, y su resolución es esencial enaplicaciones como la mejora de la voz, el reconocimiento de habla y la cancelación de ruido. Para este laboratorio,se recreó el problema de la fiesta de coctel, donde existen 2 fuentes sonoras capturadas por un arreglo de 2 micrófonos de acuerdo con la siguiente metodología.

Configuración del sistema:
1.1. Se conectaron los 2 micrófonos al sistema de adquisición de datos y se distribuyeron de una forma estratégica en la sala insonorizada. Los micrófonos estaban ubicados de manera que cada uno capturó diferentes combinaciones de las señales provenientes de las dos fuentes, tal como se evidenciará en la imagen 1.

Imagen 1. Organizacion microfonos;

WhatsApp Image 2025-02-27 at 20 49 38

En cuanto a las coordenadas, de estos dos microfonos, se evidencia en la imagen 1, que el primer microfono esta abajo a la izquierda, y el otro en la parte superior derecha, la distancia diagonal entre los dos es de 3.3 m , esta medida se tomó con un metro virtual que posee el disposito iphone, y para ser más precisos, el micrfono 1, que es el de abajo tiene una distancia de 1.5 m desde el centro de la sala hasta donde está, y el microfono 2, tiene una distancia de 1.8 m desde el centro de la sala.

Para continuar, se ubicaron dos personas en posiciones fijas dentro de la sala insonorizada (una en cada extremo). Es importante mencionar que estaban localizados a distancias diferentes y orientados en distintas direcciones para simular un entorno de "fiesta de cóctel".

Es importante destacar, que como se evidencia en la imagen 1, los microfonos implementados son de tipo apple, el cual posee distintas características que interfieren en las señales que se observarán más adelante, los dispositivos apple que implementamos poseen una frecuencia de muestreo de 44.1 kHz. Asimismo, el sistema de adquisición es de digitalización, es decir que en esta práctica de laboratorio se diseñó para que logrará capturar las señales de voz en un entorno que a pesar de ser insonorizado se escucha ruido de ambiente, donde de la misma manera para el tiempo de la captura fue de aproximadamente 15 segundos por audio, también se calculará el snr midiendo el ruido en la sala con los dos micrófonos.

Captura de la señal:
2.1.Se generó la señal mediante la voz de los dos sujetos de prueba; cada uno dijo una frase diferente durante el tiempo de captura de la señal (aproximadamente 15 segundos). Las señales de los micrófonos deben ser registradas por el sistema de adquisición y guardas para ser analizadas, lo que se evidencia en la imagen 2, donde se observa la señal de voz de Paola junto con las señales de Andrea y el ruido en el dominio del tiempo. Se aprecia una superposición entre las señales, lo que sugiere que la separación de fuentes es necesaria para extraer la voz de interés.

imagen 2; señales voz y ruido en el dominio del tiempo

Figure 2025-02-27 201341 (0)
2.2. Se grabo el ruido de la sala que en nuestro caso fue un salón insonorizado, con 2 micrófonos distintos (como se observó previamente en la imagen 1), donde es importante mencionar que los audios del ruido ambiente y la voz de paola y andrea, se encuentran en la parte inicial de este trabajo, es decir, que si desean escuchar los audios los pueden descargar, esto se hizo con el fin de mostrar la práctica simultanemanete a la explicación.

Antes de continuar se debe aclarar;
Para correr el codigo y que funcione correctamente se deben descargar ciertas cosas, inicialmente en la consola de spyder se deben descargar librerías de la siguiente manera; pip install numpy matplotlib wfdb scipy, estas son para;

import numpy as np: es para que permita correr cálculos númericos y arrays en caso de tenerlos.
import matplotlib.pyplot as plt :grafica señales de audio y transformaciones, como espectros de frecuencia
import scipy.io.wavfile as wavfile ; lee archivos en formato WAV, Con wavfile.read() se cargan archivos WAV y se obtiene su frecuencia de muestreo y los datos. -from scipy.fftpack import fft; Importa la Transformada Rápida de Fourier (FFT), que se usa para convertir una señal del dominio del tiempo al dominio de la frecuencia.
from sklearn.decomposition import FastICA; implementa el Análisis de Componentes Independientes (ICA), que se usa para separar señales mezcladas (más adelante lo veremos).
import sounddevice as sd; permite la grabación y reproducción de audio en tiempo real, se usa para capturar sonido desde un micrófono o reproducir audio procesado.
from scipy.signal import butter, filtfilt; se usa para diseñar y aplicar filtros (como el que usaremos más adelante), butter(); crea un filtro Butterworth, que es un tipo de filtro pasa-bajos, pasa-altos, pasa-banda, etc y filtfilt() aplica el filtro a una señal sin introducir desfases.
Los métodos de separación de fuentes son;
El Análisis de Componentes Independientes (ICA);este separa las señales mezcladas pero asumiento que las fuentes son independientes, este usualmente se usa para recuperar voces separadas cuando se habla al mismo tiempo.
El Análisis de Componentes principales (PCA); este reduce la dimensionalidad de las señales, pero manteniendo máxima varianza, es decir, se implementa en ambitos como eliminar ruido en señales acústicas y mejora la señal en entorno que sea muy ruidoso, por ejemplo si se tienen microfonos, este permite identificar las direcciones dominantes de las fuentes de sonido.
El Beamforming; en este se implementan microfonos o arreglos de microfonos, para identificar las señales que vienen de una dirección especifica, como por ejemplo para captar la voz en conferencias o grabaciones, donde se mejora la voz del usuario y se reduce el ruido del fondo.
Filtrado adaptativo (LMS, RLS); este asjusta los coeficientes de un filtro digital para quitar las interferncias, como por ejemplo para quitar el eco de las llamadas de voz, o eleminar el ruido en señales cerebrales.
Transformada de fourier corto tiempo; esta separa las señales en el dominio del tiempo- frecuencia para lograr identificar y de la misma forma aislar los componentes, como por ejemplo, separar voz y música o eliminar ruido de señales de radar.
Redes neuronales profundas (DNN) ; aprende patrones de separacion pero a partir de grandes volumenes de datos, es decir cuando se mejora el audio en las llamadas de voz o videoconferencias o separar fuentes en grabaciones musicales.
3.1. A partir de esto, se seleccionó la técnica de separación ¨análisis de componentes independientes (ICA)¨, que basicamente recupera señales originales que surgen de una mezcla sin saber como se combinaron inicialmente, tal como se escucha en los audios, en el código en particular que desarrollamos se implementa ¨FastICA(n_components=3)¨ (significa que se requiere separar las tres señales), lo que se aplica a as tres señales (Voz Andrea, Ruido y Voz Paola) y para lograr sacar los commponentes independientes se utilizó la función fit_transform() (encuentra y extrae las fuentes independientes de la mezcla), es decir las voces y el ruido por aparte, las señales realizadas mediante la voz se evidenciarán en las imagenes 3 ( voz andrea separada), imagen 5 (voz paola separada) y la imagen 7( ruido separado:).

Seguido a esto se realizó un análisis temporal y espectral de las señales capturadas por cada micrófono, identificando las características principales de cada fuente sonora. Utilizando la transformada de Fourier discreta (DFT) o la transformada rápida de Fourier (FFT), describiendo la información que se puede obtener con cada una de ellas.

La Transformada Rápida de Fourier (FFT) es un método para convertir una señal del dominio del tiempo al dominio de la frecuencia y en el aspecto del código en términos generales permite visualizar el contenido espectral de las señales separadas y lo usamos para verificar que las señales separadas contienen las frecuencias correctas de la voz y que el ruido ha sido reducido, donde se usa ¨np.fft.fft()¨ para calcular la FFT y se grafican los resultados en escala logarítmica ¨(plt.semilogx())¨.

En este lab, se usa un sistema que realiza un análisis en el dominio del tiempo y en el dominio de la frecuencia, lo que nos permitió comprender la calidad de la separación de las señales y la eficacia del filtrado que se aplicó. Las señales en el dominio del tiempo representan la variación del voltaje en función del tiempo. En las gráficas proporcionadas se pueden observar las señales de voz filtradas para "Paola" y "Andrea".

El análisis espectral permite visualizar la distribución de la energía de la señal en distintas frecuencias. Para ello, se ha utilizado la Transformada Rápida de Fourier (FFT), que convierte la señal en el dominio del tiempo al dominio de la frecuencia.

Se utiliza la Transformada Rápida de Fourier para visualizar el espectro de las señales separadas y filtradas verificando si las señales están correctamente aisladas y si el ruido ha sido reducido, lo cual, se evidnecia en las imagénes 4 (espectro voz andrea separado), imagen 6 (espectro voz paola separada) y la imagen 8 ( espectro ruido separado).

Con esto claro, vamos a ver las señales separadas y su respectivo espectro;

señal ANDREA:

Imagen 3; voz andrea separada:

Figure 2025-02-27 201341 (1)
En esta gráfica es importante mencionar que, se observa una señal con variaciones claras en amplitud, lo que indica la presencia de segmentos con mayor energía (palabras enfatizadas) y pausas naturales entre palabras, también observamos que la señal parece tener una buena relación señal/ruido (SNR), ya que las variaciones de amplitud son más significativas en comparación con el ruido de fondo y asu vez, no se observan patrones repetitivos ni artefactos evidentes de interferencia, lo que sugiere una buena separación de la voz.

Imagen 4; espectro voz andrea separado:

Figure 2025-02-27 201341 (2)
La señal procesada mantiene las componentes dominantes dentro del rango del habla y se observa una disminución en las frecuencias más altas y bajas, indicando que el filtrado ha eliminado ruido externo.

señal PAOLA:

Imagen 5; voz paola separada:

Figure 2025-02-27 201341 (5)
En esta gráfica es importante mencionar que, la forma de onda tiene características similares a la de Andrea, pero con diferencias en el patrón de amplitud y en la duración de los segmentos hablados, observamos que la señal ha sido correctamente aislada, ya que no se observan rastros significativos de la voz de Andrea ni del ruido ambiental, de la misma manera hay partes de menor amplitud, lo que podría deberse a una diferencia en la intensidad de la voz del hablante o a la posición relativa del micrófono.

imagen 6; espectro voz paola separada:

Figure 2025-02-27 201341 (6)
Se identifica la presencia de componentes frecuenciales en el rango de voz humana (aproximadamente entre 100 Hz y 4 kHz) y se observa una reducción significativa en las frecuencias fuera de este rango, indicando que el filtrado ha sido efectivo, la representación utiliza escala logarítmica para facilitar la observación de detalles en un amplio espectro.

señal RUIDO AMBIENTE:

Imagen 7; ruido separado:

Figure 2025-02-27 201341 (3)
En esta gráfica es importante mencionar que, el ruido separado muestra una señal más uniforme, sin grandes variaciones de amplitud como en las señales de voz, también se pueden notar picos en ciertos momentos, lo que podría deberse a sonidos externos como movimientos de objetos o ecos en la sala. La energía del ruido parece distribuida a lo largo de toda la señal sin pausas marcadas, lo cual es característico de un ruido de fondo constante.

Imagen 8; espectro ruido separado:

Figure 2025-02-27 201341 (4)
Se observa que el ruido tiene un pico de magnitud en frecuencias bajas y medias, lo que sugiere la presencia de ruido ambiental o de fondo, la eliminación de este ruido mejora significativamente la inteligibilidad de la señal de voz.

3.2. Posterior a esto, se implementa un filtro Butterworth pasa banda (se implementa este filtro porque despues de separarla con la técnica mencioanda la señal puede tener frecuencias no deseadas) para mejorar la calidad de las señales de voz y se definieron frecuencias de corte entre los 300 Hz Y 3400 Hz (que es el rango de frecuencias de la voz humana), que quiere decir que permitirá eliminar el ruido fuera del espectro típico del habla de nuestras voces, respecto al código se implementa ¨butter_bandpass()¨, con frecuencia de corte baja ; 300 Hz y la frecuencia de corte alta 3.400 Hz y se aplica con apply_filter() usando scipy.signal.filtfilt(), que evita distorsiones en la señal filtrada, es necesario mencionar que este filtrado permitirá mejorar la calidad de la voz al eliminar el ruido de baja y alta frecuencia, por lo que el SNR que se obtendrá será mucho mejor después de la separación. estas voces filtradas Y sus respectivos espectros se evidenciarán a continuación en las imagénes 9,10,11 y 12.

señal PAOLA:

Imagen 9. Voz paola filtrada;

Figure 2025-02-27 201341 (9)
La señal de voz de Paola ha sido filtrada, mostrando una variación en el tiempo que representa la modulación natural del habla, también se observa un rango de amplitud entre aproximadamente -8 mV y 8 mV y la señal presenta una estructura característica del habla, con regiones de mayor y menor intensidad.

Imagen 10. Espectro de voz paola filtrada;

Figure 2025-02-27 201341 (10)
En esta gráfica se muestra una concentración de energía en un rango de frecuencias específico, lo cual es característico de una señal de voz bien definida.;

señal ANDREA:

Imagen 11. voz andrea filtrada;

Figure 2025-02-27 201341 (7)
La señal de voz filtrada de Andrea muestra variaciones similares a la de Paola, con amplitudes comparables, se nota la presencia de pausas y momentos de mayor energía, característicos del habla natural.

Imagen 12;espectro de voz andrea filtrada;

Figure 2025-02-27 201341 (8)
En esta gráfica se un observa una concentración de energía en un rango de frecuencias específico, similar a la voz filtrada de paola, sin embargo la de andrea posee picos de magnitud que indican las principales frecuencias componentes de la señal vocal.

Por otro lado, Con las librerias descargadas anteriormente, se procedió a calcular el SNR, el código calcula el SNR de cada señal antes y después del filtrado ,que se usa para medir como se encuentra la señal o mas bien la calidad de esta, este cálculo se va a explicar por partes para entenderlo y no tener la neesidad de abrir o cargar el código, sin embargo, en caso de así quererlo pueden descargar las librerias ya mencionadas y compilar el codigo para visualizarlo usted mismo/a;
Explicación método ICA, parte del código;

Antes de aplicar ICA, el código carga y normaliza las señales de entrada, de la siguiente manera:

¨fs1, voz_andrea = wavfile.read('Voz%20Andrea.wav') fs2, ruido = wavfile.read('RuidoAmbiente.wav') fs3, voz_paola = wavfile.read('Voz%20Paola.wav')

voz_andrea = voz_andrea.astype(np.float32) / np.max(np.abs(voz_andrea)) ruido = ruido.astype(np.float32) / np.max(np.abs(ruido)) voz_paola = voz_paola.astype(np.float32) / np.max(np.abs(voz_paola))¨

Aquí se cargan las señales de voz de Andrea, Paola y el ruido ambiente. Luego, se normalizan para asegurarse de que todas tengan valores dentro del mismo rango (-1 a 1), lo que mejora la estabilidad del algoritmo ICA.

Después, el código ajusta la longitud de las señales para que todas sean del mismo tamaño, lo cual se hace de esta forma :

¨min_length = min(len(voz_andrea), len(ruido), len(voz_paola)) voz_andrea = voz_andrea[:min_length] ruido = ruido[:min_length] voz_paola = voz_paola[:min_length]¨

Esto es importante porque ICA trabaja con matrices de tamaño uniforme. Una vez que las señales están listas, se crea una matriz que contiene las tres señales como columnas (una mezcla de las fuentes originales): ¨mezcla = np.vstack((voz_andrea, ruido, voz_paola)).T¨ y esto genera una matriz donde cada fila es una muestra de tiempo y cada columna es una de las señales mezcladas.

Luego, se aplica ICA utilizando la implementación de FastICA de scikit-learn, que en el código, se visualiza de la siguiente manera; ¨ica = FastICA(n_components=3) separadas = ica.fit_transform(mezcla)¨ ICA no garantiza que las señales separadas aparezcan en el mismo orden que las originales. Para corregir esto, el código calcula la correlación entre cada componente extraído y las señales originales: ¨correlaciones = np.array([[np.corrcoef(separadas[:, i], senales_originales[j])[0, 1] for i in range(3)] for j in range(3)]) orden_correcto = np.argmax(np.abs(correlaciones), axis=0)¨

Esto busca la mayor correlación entre las señales extraídas y las originales, y asigna cada componente a la señal correcta. Después, reorganiza las señales separadas de acuerdo con este orden:

¨senales_ordenadas = np.zeros_like(separadas) for i, index in enumerate(orden_correcto): senales_ordenadas[:, index] = separadas[:, i]¨ Ahora, las señales separadas coinciden con sus respectivas fuentes originales.

Para mejorar la calidad de las voces separadas, el código aplica un filtro pasabanda que conserva las frecuencias de la voz humana (300 Hz - 3400 Hz):

¨lowcut = 300 # Frecuencia de corte baja en Hz highcut = 3400 # Frecuencia de corte alta en Hz voz_andrea_filtrada = apply_filter(senales_ordenadas[:, componentes.index('Voz Andrea Separada')], lowcut, highcut, fs1) voz_paola_filtrada = apply_filter(senales_ordenadas[:, componentes.index('Voz Paola Separada')], lowcut, highcut, fs1)¨

Esto ayuda a eliminar posibles interferencias o ruido fuera del rango de la voz humana.

Y de esta forma llegamos a la parte donde el código mide la relación señal a ruido (SNR) antes y después del filtrado para evaluar la mejora en la calidad de la señal separada, teniendo en cuenta que los resultados se evalúan con el criterio:

-SNR < -10 dB → Mala calidad.

-SNR entre 10 y 20 dB → Aceptable.

-SNR > 20 dB → Excelente calidad.

En la imagen a continuación se observan los valores obtenidos;

Imagen 13; SNR antes y después del filtrado método (ICA)

Captura de pantalla 2025-03-01 a la(s) 3 06 04 p m
La voz de andrea pasó de 22.97 dB , a 40.58 dB, lo que indica una mejora significativa de las claridad de la señal, y la voz de paola pasó de 23.08 dB a 40.67dB, lo que evidencia una mejoría muy alta.

Es importante resaltar que el método ICA trabaja con matrices de tamaño uniforme, donde requiere que todas las señales tengan la misma cantidad de muestras (misma longitud) para poder construir la matriz de mezcla y aplicar el algoritmo correctamente. A partir de esto, ICA Es útil para separar señales de origen distinto (como dos voces habladas simultáneamente).

Para recordar;el código para reLizar este método, junto con todas las gráficas expuestas anteriormente, se encuentra en el archvivo lab333, el cual se puede seleccionar para conocer todo el codigo y en caso de quererlo , descargar las librerias como se explicó y se podrá ver en la consola de su spyder.

Como ítem adicional, relizamos el cálculo de la misma manera que ya se mencionó pero por el método de Análisis de Componentes principales (PCA), esto con el fin de comparar la calidad de separado por ambos métodos y definir cual resulta más óptimo,
En este método, antes de aplicar el PCA, el código carga y normaliza las señales (las voces), Se leen tres archivos de audio:

Voz Andrea.wav (voz de Andrea)
RuidoAmbiente.wav (ruido de fondo)
Voz Paola.wav (voz de Paola)
Se normalizan dividiéndolas por su máximo valor absoluto y se recortan a la misma longitud para que puedan ser analizadas juntas. luego se crea una matriz de mezcla, ¨mezcla = np.vstack((voz_andrea, ruido, voz_paola)).T¨, donde cada fila representa un instante de tiempo y cada columna es una señal, es decir, cada muestra en el tiempo contiene tres valores: la voz de Andrea, el ruido y la voz de Paola. se aplica el PCA, ¨pca = PCA(n_components=3) separadas = pca.fit_transform(mezcla)¨

Donde, Se usa la función PCA de sklearn.decomposition para encontrar tres componentes principales. fit_transform(mezcla) calcula las componentes principales y proyecta la mezcla en un nuevo espacio de coordenadas donde las señales están separadas y como el PCA no tiene información previa sobre qué señal corresponde a cada fuente, el código identifica las componentes usando correlación con las señales originales: ¨correlaciones_paola = [np.corrcoef(separadas[:, i], voz_paola)[0, 1] for i in range(3)] indice_paola = np.argmax(np.abs(correlaciones_paola))¨

Se calcula la correlación entre cada componente PCA y la voz original de Paola y se elige el índice de la componente con mayor correlación y lo mismo se hace para andrea, después de identificar las señales de voz separadas, se les aplica un filtro pasa banda para mejorar su calidad, es decir, se usa un filtro pasa banda Butterworth para conservar las frecuencias entre 300 Hz y 3400 Hz, que corresponden al rango de voz humana, por último se calcula el snr antes y después de la separación, esto se evidencia en la imagen 14.

Imagen 14; SNR antes y después del filtrado método (PCA);

Captura de pantalla 2025-03-01 a la(s) 3 08 20 p m
SNR antes del filtrado:

Voz Andrea: 22.97 dB
Voz Paola: 23.08 dB
SNR después del filtrado:

Voz Andrea: 21.61 dB
Voz Paola: 21.88 dB
Teniendo en cuenta esto, con el método ICA, el SNR mejora significativamente, pasando de valores alrededor de 23 dB a más de 40 dB, lo que indica una excelente calidad de separación. Con el método PCA, el SNR disminuye ligeramente después del filtrado, quedando cerca de 21 dB, lo que es apenas aceptable y sugiere que el filtrado no tuvo un impacto positivo.

Para conluir la parte del SNR, antes de realizar el filtrado, el SNR por el método (ICA) estaba en un rango aceptable (~23 dB), indicando que la señal tenía una calidad moderada, no obstante después del filtrado, el SNR aumentó a más de 40 dB, lo que indica una calidad excelente en la separación y limpieza de la señal, por lo que el método de separación de señales demuestra su efectividad en mejorar la señal capturada.

Es importante resaltar que, PCA busca componentes ortogonales (no necesariamente independientes) que expliquen la mayor varianza en los datos .Es más útil para reducir ruido.

Para recordar;el código para reLizar este segundo método, se encuentra en el archvivo metodo2, el cual se puede seleccionar para conocer todo el codigo y en caso de quererlo , descargar las librerias como se explicó y se podrá ver en la consola de su spyder.

POR ÚLTIMO, respecto a la voz de interes;
Para reproducir la voz de Paola, primero se debe calcular el SNR para evaluar la calidad de la separación, como se hizo previamente. Luego, se elige entre compilar el código de labb333 (recomendado, ya que usa el método ICA) o el método 2 (PCA), según se prefiera. Tras compilar y ejecutar el código seleccionado, se obtendrá la señal de la voz de interes (PAOLA) separada, en la cual la voz de Paola, aunque no completamente nítida, se entiende bien. Finalmente, para reproducir el audio filtrado, se usa la función sd.play(voz_paola_filtrada, samplerate=fs1) seguida de sd.wait(), la cual, pertenece a la biblioteca sounddevice y se usa para reproducir audio en Python, donde voz_paola_filtrada: es un array NumPy o una lista que contiene los valores de la señal de audio separada (en este caso, la voz de Paola) y la parte de samplerate=fs1: define la frecuencia de muestreo (en Hz) con la que se reproducirá el audio, mientras que la línea sd.wait() se usa para pausar la ejecución del código hasta que la reproducción del audio haya finalizado. Esto es útil para evitar que el programa continúe ejecutándose antes de que el sonido termine de reproducirse.

Todo esto, nos hace notar, que si se evalúan los dos métodos, en el caso del ICA logra extraer la voz de Paola de manera que sigue siendo entendible, lo que demuestra su efectividad en la separación de señales.

En esta parte se evaluan los resultados comparando la señal aislada con la señal original utilizado métricas de calidad como la relación señal/ruido para cuantificar el desempeño de la separación. Es neceario mencionar que la VOZ DE INTERÉS FUE LA DE PAOLA, por ende ;
-En la imagen 5, donde se muestra la señal de voz de Paola separada, se observa una reducción significativa de la interferencia de la voz de Andrea y del ruido. Esto indica que el proceso de separación ha sido exitoso.

Al comparar con la imagen 9, que muestra la voz de Paola después del filtrado, se aprecia que la señal conserva su estructura temporal, pero con una posible mejora en la claridad debido a la reducción del ruido residual.

Las imágenes 6 y 10 muestran el espectro de la señal de voz de Paola separada y filtrada. Se puede notar que la señal de interés (paola) mantiene componentes de frecuencia en un rango coherente con una voz humana (~300 Hz - 3.4 kHz).

La reducción de componentes de ruido fuera de este rango sugiere que el filtrado ha sido efectivo. En particular, la disminución de energía en frecuencias más altas o bajas indica que los métodos aplicados lograron aislar la voz sin distorsionar demasiado el contenido espectral.

Retomando SNR de la imagen 13; Dado que el SNR de la voz de Paola mejoró significativamente (de 23.88 dB a 40.67 dB), esto indica que la calidad de la señal aumentó notablemente tras la separación y el filtrado, este incremento sugiere que el método aplicado logró una limpieza efectiva de la señal, eliminando la mayoría del ruido y mejorando la inteligibilidad de la voz de Paola.

5.Preguntas finales refuerzo de aprendizaje;

Con esta práctica se espera que como estudiantes logreemos reproducir por separado el audio de cada una de las voces capturadas a partir de la obtención de dos señales con dos voces mezcladas.

5.2. ¿Cómo afecta la posición relativa de los micrófonos y las fuentes sonoras en la efectividad de la separación de señales?

La posición relativa de los micrófonos y las fuentes sonoras es un factor clave en la efectividad de la separación de señales. Afecta directamente la capacidad de separación para distinguir y aislar cada voz. Entonces, si la fuente está demasiado cerca de un micrófono y lejos de otro, la señal captada tendrá una diferencia de amplitud considerable, lo que puede ser útil para separar señales basadas en la intensidad, sin embargo, si la distancia es demasiado grande, la señal puede degradarse debido a la atenuación del sonido en el aire, afectando la claridad y precisión de la separación.
También, si los micrófonos están cerca de superficies reflectantes, las reflexiones pueden interferir con las señales directas, generando ecos y dificultando la separación de las voces como se realizó en este laboratorio. Asimismo, un solo micrófono tiene menos información espacial y depende más de técnicas de filtrado espectral.

5.3. ¿Qué mejoras implementaría en la metodología para obtener mejores resultados?

Asegurar que los micrófonos estén equidistantes de las fuentes para minimizar problemas en la captura de voces, esto lo podriamos mejorar tomando una medida más exacta, de esta forma se podría controlar más este factor.
Medir la respuesta de los micrófonos en la sala para compensar efectos de reflexiones.
optimizar la disposición de los micrófonos, usar algoritmos más avanzados de separación y mejorar la reducción de ruido para obtener mejores resultados en términos de claridad y calidad de la voz separada.
