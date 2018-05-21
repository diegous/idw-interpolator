# -*- coding: utf-8 -*-

import pandas as pd
dataframe = pd.read_csv('./matrix.csv')

columns = len(dataframe.columns)

for i in range(columns):
  nombre = 'p' + str(i)

  # Obtener la primera columna y convertirla en DataFrame
  series = dataframe[dataframe.columns[i]]
  newDataFrame = series.to_frame()

  # Agregar en la primera columna el nombre de la estación
  newDataFrame.insert(0, 'estación', nombre)

  # Agregar en la segunda columna el año
  newDataFrame.insert(1, 'año', 2017)

  # Agregar en la tercera columna el mes
  newDataFrame.insert(2, 'mes', '09')

  # Exportar DataFrame a archivo
  newDataFrame.to_csv(nombre + '.txt', index=False)
