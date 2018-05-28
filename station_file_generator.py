# -*- coding: utf-8 -*-

import pandas as pd
dataframe = pd.read_csv('./matrix.csv')

# Cantidad de columnas sin incluír las últimas porque estas no
# tienen datos si no que tienen el año, mes, día, hora y minuto
columns = len(dataframe.columns) - 5

for i in range(columns):
  nombre = 'p' + str(i)

  # Obtener la primera columna y convertirla en DataFrame
  series = dataframe[dataframe.columns[i]]
  newDataFrame = series.to_frame()

  # Agregar en la primera columna el nombre de la estación
  newDataFrame.insert(0, 'estación', nombre)

  # Obtener datos de fecha de la matriz orishinal
  year   = dataframe[dataframe.columns[-5]]
  month  = dataframe[dataframe.columns[-4]]
  day    = dataframe[dataframe.columns[-3]]
  hour   = dataframe[dataframe.columns[-2]]
  minute = dataframe[dataframe.columns[-1]]

  # Agregar en las primeras columnas los datos de la fecha
  newDataFrame.insert(1, 'año',    year)
  newDataFrame.insert(2, 'mes',    month)
  newDataFrame.insert(3, 'día',    day)
  newDataFrame.insert(4, 'hora',   hour)
  newDataFrame.insert(5, 'minuto', minute)

  # Exportar DataFrame a archivo
  newDataFrame.to_csv(nombre + '.txt', index=False, header=None)
