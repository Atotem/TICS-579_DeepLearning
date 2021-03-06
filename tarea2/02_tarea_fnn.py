# -*- coding: utf-8 -*-
"""02-Tarea-FNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1RVRWzXKtxCHr4pRdtJom1arDusyYLRih

# Tarea 2

# Parte práctica (3 puntos)
La NASA mantiene la información de varios cometas y quiere determinar alguna manera de predecir el diametro de un cometa. Específicamente, han analizado en forma manual una muestra de 100.000 asteroides. Los datos consisten en 27 variables, con distinta información como por ejemplo nombre del asteroide, su periodo orbital, su periodo de rotación, etc. Todos los datos existentes, se encuentran en un puro archivo llamado asteroidTrain.csv. Mientras que las descripciones de cada una de las variables se encuentran en el archivo tarea2Informacion.txt

Desafortunadamente, la NASA todavía no ha evaluado 37.681 asteroides y no tienen tiempo para realizarlo. Por lo mismo, le piden que aplique una red neuronal feed forward para obtener una predicción de estos asteroides.

1. Lea los datos y borre las variables/asteroides que estime necesario. En caso que crea que la base de datos todavía es demasiado grande para aplicar los modelos, usted puede tomar una muestra de la misma (1.5 punto).
2. Entrene un modelo feed forward. Realice una busqueda de parámetros modifique el número de capas, de neuronas, funciones de activación, epocas, etc. Seleccione un solo modelo de los seleccionados y muestre ese modelo (0.5 puntos).
3. Seleccione uno de los modelos del punto anterior y evalue los 37.681 asteroides que la NASA no ha evaluado. Se deberá generar un archivo csv con 37.681 filas, cada fila deberá ser una estimación (1 punto). 

El punto de evaluación final será una competencia entre todas las tareas basados en los MSE más bajo obtenido por cada grupo. El puntaje final será una regresión lineal entre el peor y mejor puntaje.
"""

import numpy as np
import tensorflow as tf
import pandas as pd
from plotnine import *

"""# Teoría (3 puntos)
Una de las ventajas al usar redes multicapas es la posiblidad de abordar problemas con múltiples clases a través de la función softmax. 

Imaginemos que tenemos una red feed forward de múltiples capas con $k$ neuronas de salidas, función de activación softmax, y función de perdida $\displaystyle L=-\sum_{i=1}^ky_i\ln(o_i)$ (Note que la función de error esta definido para un punto, no un set de puntos). En este error, $o_i$ es la salida de la neurona de la clase $i$ e $y$ es un vector de $k$ valores correspondiente a la transformación one-hot-encoding de la clase (recuerde que tenemos $k$ clases).<br>
Por ejemplo, si el problema tiene 4 clases y el punto pertenece a la clase 3, entonces $y=[0,0,1,0]$, por lo tanto $y_1=0$, $y_2=0$, $y_3=1$ $y_4=0$.<br>
Note que nunca se define el número de puntos del set de datos, no importa en esta tarea.
 
Demuestre que $\displaystyle \frac{\partial L}{\partial h_i}=\sum_{j=1}^k\frac{\partial L}{\partial o_j}\frac{\partial o_j}{\partial h_i}=o_i-y_i$, donde $\displaystyle o_i=\frac{\exp(h_i)}{\sum_{j=1}^k\exp(h_j)}$ y $h_i$ es el valor continuo correspondiente a la neurona $i$ que es transformado a una probabilidad. <br><br>

Para realizar esta demostración realize lo siguiente
1. Demuestre que $\displaystyle\frac{\partial o_i}{\partial h_j}=-o_io_j$ si $i\neq j$ (1 punto)<br>
2. Demuestre que $\displaystyle\frac{\partial o_i}{\partial h_j}=o_i(1-o_i)$ si $i=j$ (1 punto)<br>
3. Utilizando las demostraciones anteriores demuestre $\displaystyle \frac{\partial L}{\partial h_i}=\sum_{j=1}^k\frac{\partial L}{\partial o_j}\frac{\partial o_j}{\partial h_i}=o_i-y_i$ (1 punto)

En caso que no pueda demostrar los puntos 1 y 2 acepte esas relaciones y demuestre directamente el punto 3 por un solo punto.
"""

