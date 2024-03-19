import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.image as mpimg


def leer_coordenadas_lidiar(): # Input nombre de archivo
    nombre_archivo = "FusionSens/lidar/000503.ply"
    try:
        with open(nombre_archivo, 'r') as archivo:

            lineas = archivo.readlines()    #Líneas[8] Comienzan las coordenadas
            del lineas[0:8]
            # [tuple(map(float, linea.strip().split()[1:])) for linea in lineas] 
            return [tuple(map(float, linea.split()[:-1])) + (1,) for linea in lineas]
        #[tuple(map(float, linea.split()[:-1])) + (1,) for linea in lineas]
            
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no existe.")
    except Exception as e:
        print(f"Error al leer las coordenadas desde {nombre_archivo}: {e}")

def matrix_type_converter(coordenadas):
    try:
        # Verificar que la entrada sea del tipo esperado
        if not all(isinstance(coor, tuple) and len(coor) == 4 for coor in coordenadas):
            raise ValueError("La entrada debe ser una lista de tuplas de tres elementos")
        # Convertir cada tupla en una matriz 4x1
        return [np.array(coor).reshape(4, 1) for coor in coordenadas]

    except Exception as e:
        print("Error al convertir coordenadas a matrices:", str(e))
        return None

def build_projection_matrix(w, h, fov):
    focal = w / (2.0 * np.tan(fov * np.pi / 360.0))
    K = np.identity(3)
    K[0, 0] = K[1, 1] = focal
    K[0, 2] = w / 2.0
    K[1, 2] = h / 2.0
    return K

def matrix_mult(X):
    k = build_projection_matrix(1200, 900, 90)

    X = [X[1], -X[2], X[0]]
    point_img = np.dot(k, X)
    
    # Normalize
    point_img[0] /= point_img[2]
    point_img[1] /= point_img[2]
    return point_img[0:2]


    

if __name__ == "__main__":

    coordenadas_laser = leer_coordenadas_lidiar()        
    matrices = matrix_type_converter(coordenadas_laser)
    fig, ax = plt.subplots()
    ax.set_xlim(-10000, 10000)
    ax.set_ylim(-10000, 10000)
    ax.set_aspect('equal', adjustable='datalim')
    ax.set_frame_on(False)
    puntos = []
    max_val = 0
    for i in range(len(coordenadas_laser)):
        if(coordenadas_laser[i][1] > -5.8 and coordenadas_laser[i][1] < -1.67):
            if(coordenadas_laser[i][0] > 2 and coordenadas_laser[i][0] < 9):
                if(coordenadas_laser[i][2] > -3.3 ):
                    punto = matrix_mult(matrices[i])
                    puntos.append(punto)
        
    for i in range(len(puntos)):    
        #Draw
        plt.title('Puntos láser')
        ax.plot(puntos[i][0], -puntos[i][1], 'ro')  # 'bo' para indicar un punto azul ('b') sin conexión ('o')
       
    
    plt.show()


    

