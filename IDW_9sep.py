# -*- coding: utf-8 -*-

from math import pow
from math import sqrt
import numpy as np
import pylab
import matplotlib.pyplot as plt
import csv
import pandas as pd

costa  = np.loadtxt('CostaRdP.txt')
cuenca = np.loadtxt('CuencaSASD.txt')
P  = 2
S  = 500
Xs = 17
Ys = 17

def pointValue(x, y, power, smoothing, xv, yv, values):
    nominator   = 0
    denominator = 0

    for i in range(len(values)):
        # La X y la Y que recibimos como parámetro corresponden a la esquina superior derecha de la celda
        # que estamos trabajando, por lo que hace falta mover la X hasta el centro de la celda sumando la
        # mitad del tamaño de esta, y lo mismo con la Y pero restando ese tamaño
        xDistance = x - xv[i] + 1000
        yDistance = y - yv[i] - 1000
        dist = sqrt(pow(xDistance, 2) + pow(yDistance, 2) + smoothing);

        # If the point is really close to one of the data points, return the data point value to avoid singularities
        if(dist < 0.0000000001):
            return values[i]

        weight = pow(dist, power)
        nominator   += values[i] / weight
        denominator += 1 / weight

    # Return NODATA if the denominator is zero
    if denominator == 0:
        return -9999
    else:
        return nominator/denominator

def invDist(xv, yv, values, xsize=0, ysize=0, power=0, smoothing=0):
    valuesGrid = np.zeros((ysize,xsize))
    smoothing = pow(smoothing, 2)

    for x in range(xsize):
        for y in range(ysize):
            valuesGrid[x][y] = pointValue(XI[x,y], YI[x,y], power, smoothing, xv, yv, values)

    return valuesGrid

if __name__ == "__main__":
    power = P
    smoothing = S

    #Creating some data, with each coodinate and the values stored in separated lists
    nodos = np.loadtxt('Prueba.txt', skiprows = 0)

    # Tomar primera fila de nodos
    values = nodos[0]

    xv = [5647903, 5658452, 5634830, 5654339, 5658679, 5647516, 5660435, 5661111, 5650557]
    yv = [6132110, 6134653, 6142450, 6147277, 6147746, 6148650, 6154264, 6158592, 6166454]

    #Creating the output grid (100x100, in the example)
    tix = np.linspace(5636000, 5668000, Xs)
    # tiy = np.linspace(6134000, 6166000, Ys)
    # Acá le doy vuelta los límites (primero el número más grande y después el más chico) para que
    # arme el arreglo con el la fila 0 con los valores de la primera fila del mapa
    tiy = np.linspace(6166000, 6134000, Ys)

    XI, YI = np.meshgrid(tix, tiy)

    matrix = []
    for filaDeValores in nodos:
        #Creating the interpolation function and populating the output matrix value
        ZI = invDist(xv, yv, values, Xs, Ys, power, smoothing)
        Zii = ZI[:,4:11]

        # flatZI solo representa una fila la matriz final que se espera armar.
        # Esa fila es para un determinado horario. Se supone que deberia haber una fila cada 5 minutos
        # Aca habria que armar una matriz con todas esas filas y pasarla al armador de CSV de abajo.
        flatZI = Zii.flatten()
        matrix.append(flatZI)


    # En esta variable vamos a guardar la cabecera de las columnas
    cabeceras = []

    # Armar la primera fila con las coordenadas de cada punto
    for x in range(Xs):
        for y in range(4, 11):
            cabeceras.append("(%.2f,%.2f)" % (XI[x,y], YI[x,y]))

    # Esta forma de guardar el archivo no la vamos a usar porque vamos a usar el CSV de abajo
    # np.savetxt('matrix.txt', matrixk, fmt="%.2f", delimiter = ',')

    with open('matrix.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Escribir cabecera con las coordenadas como primera fila del CSV
        csvwriter.writerow(cabeceras)

        # Escribir cada una de las matrices, una por fila
        for fila in matrix:
            fila_con_dos_decimales = map("{:.2f}".format, fila)
            csvwriter.writerow(fila_con_dos_decimales)

    # Dibujar los resultados
    #n = plt.normalize(0.0, 100.0)
    plt.subplot(1, 1, 1)
    plt.pcolor(XI, YI, ZI)
    plt.scatter(xv, yv, 100, values,".", None, None, 0, None, None, 1, None, 'Face',100)
    plt.title('Grilla')
    plt.xlim(5636000, 5668000)
    plt.ylim(6134000, 6166000)
    plt.colorbar()
    plt.plot(costa[:,0], costa[:,1], color='black')
    plt.plot(cuenca[:,0], cuenca[:,1], color='white')

    plt.xticks
    plt.yticks
    fig = pylab.gcf()
    fig.set_size_inches(8, 10)

    #plt.savefig("CuencaSSD_P2_S500_XsYs16.png", dpi=500)
    plt.show()
