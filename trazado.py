import matplotlib.pyplot as plt
import argparse
import matplotlib.patches as patches
import matplotlib.image as mpimg
import numpy as np
import os

def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:

            lineas = archivo.readlines()

            ##coordenadas_aux = [tuple(map(float, linea.strip().split()[1:])) for linea in lineas]                                  
            '''for linea in lineas:
                linea = linea.replace(',','')'''
                                                        # línea = (x, y, width, height)   [(x, y, width, height),(x, y, width, height),...]
                                                                                            # map (type converter) + split 
            return [tuple(map(float, linea.split()[1:])) for linea in lineas]               # Devuelve una lista de cada fila (file)
    
    except FileNotFoundError:
        return f"El archivo '{nombre_archivo}' no fue encontrado."
    except Exception as e:
        return f"Ocurrió un error: {e}"

def count_dir():
    try:
        archivos = os.listdir("runs/detect")       # Lista todos los archivos en la carpeta
        return len(archivos)              # Devuelve el número de archivos
    except OSError:
        return -1

def Ubicar_img(j):
    if(j == 499):
        nombre_img = "runs/detect" + "/exp/" + f"{j:06d}.png"
    else:
        num = j-498
        nombre_img = "runs/detect" + "/exp"+str(num) + "/" + f"{j:06d}.png"
    return nombre_img

def ubicar_txt(i):
    if(i == 499):
        dir = "runs/detect" + "/exp" + "/labels/"+ f"{i:06d}.txt"
    else:
        num = i-498
        dir = "runs/detect" + "/exp"+str(num) + "/labels/" + f"{i:06d}.txt"
    return dir

def draw_rect(coordenadas, i, file, ax):
    colores = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    x2 = coordenadas[file][i][0] - coordenadas[file][i][2] / 2
    y2 = coordenadas[file][i][1] - coordenadas[file][i][3] / 2
        
    rectangulo = patches.Rectangle((x2, -y2),
                                    coordenadas[file][i][2],
                                    -coordenadas[file][i][3],
                                    linewidth=1, edgecolor=colores[i % len(colores)], facecolor='none')
    ax.add_patch(rectangulo)

def color_por_distancia(x):
    if x > 20:
        return 'b'
    elif x > 10:
        return 'c'
    elif x > 6:
        return 'g'
    elif x > 4:
        return 'y'
    elif x > 1:
        return 'r'
    else:
        return 'w'

def ubicar_ply(i):
    return "FusionSens-Lidar/lidar/" + f"{i:06d}.ply"

def leer_coordenadas_lidiar(nombre_archivo): 
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
    #X = [X[0], X[1], X[2]]
    X = [X[1], -X[2], X[0]]
    point_img = np.dot(k, X)
    # Normalize
    point_img[0] /= point_img[2]
    point_img[1] /= point_img[2]
    return point_img[0:2]

def main(leer_archivo, count_dir, Ubicar_img, ubicar_txt, draw_rect):
    parser = argparse.ArgumentParser(description="Comprobación sobre el control de las coordenadas en las que se detecto actividad.") 
    parser.add_argument("-img", action="store_true", help="Mostrar imagen de fondo.")
    parser.add_argument("-s", action="store_true", help="Mostrar gráfico.")
    parser.add_argument("--n", type=int, default=float('inf'), help="Número máximo de rectángulos a dibujar.")
    args = parser.parse_args()
    #Lista[][][] Coordenadas de todos los experimentos a trazar
    coordenadas = []

    for i in range(499, 499+count_dir()):
        #Read   
        nombre_archivo = ubicar_txt(i) 
        coordenadas_rectangulo = leer_archivo(nombre_archivo)
        coordenadas.append(coordenadas_rectangulo)                      # Se añade la lectura de un fichero  

        nombre_img = Ubicar_img(i)
        background_img = mpimg.imread(nombre_img)
        
        nombre_ply = ubicar_ply(i)
        detecciones_lidiar = leer_coordenadas_lidiar(nombre_ply)
        matrices = matrix_type_converter(detecciones_lidiar)


        #Draw
        fig, ax = plt.subplots()
        ax.set_xlim(-500, 1500)
        ax.set_ylim(-1000, 0)
        ax.set_aspect('equal', adjustable='datalim')
        ax.set_frame_on(False)
        plt.title(f'Verificación de funcionamiento - Archivo-{str(i - 498)}')              
        # Eje y  invertido
        for j in range(len(detecciones_lidiar)):
            if(detecciones_lidiar[j][1] > -11 and detecciones_lidiar[j][1] < 11):
                if(detecciones_lidiar[j][0] > 1):
                    if(detecciones_lidiar[j][2] > -0.8 ):
                        punto = matrix_mult(matrices[j])
                        color = color_por_distancia(detecciones_lidiar[j][0])
                        ax.plot(punto[0], -punto[1], color + 'o', alpha=0.5)


        

        # Guarda y mostrar           Argumentos para el guardado de los eventos {}
        if(args.img):
            #ax.imshow(background_img, extent=[0, 1, -1, 0])
            ax.imshow(background_img, extent=[0, 1200, -900, 0])
            plt.savefig('results/Laser-Traces-img/lidiar-' + str(i), bbox_inches='tight')
        
        #plt.savefig('results/Laser-Traces/lidiar-' + str(i), bbox_inches='tight')
        
        if(args.s):
            plt.show()
        plt.close()

if __name__ == "__main__":
    main(leer_archivo, count_dir, Ubicar_img, ubicar_txt, draw_rect)