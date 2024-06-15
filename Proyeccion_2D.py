import numpy as np
import matplotlib.patches as patches 
import os

from Write_ply import escribir_archivo_ply
from Leer_Detecciones import leer_coordenadas_lidiar

def build_projection_matrix(w, h, fov):
    focal = w / (2.0 * np.tan(fov * np.pi / 360.0))
    K = np.identity(3)
    K[0, 0] = K[1, 1] = focal
    K[0, 2] = w / 2.0
    K[1, 2] = h / 2.0
    return K

#Lidar
def matrix_type_converter(coordenadas):
    try:
        if not all(isinstance(coor, tuple) and len(coor) == 4 for coor in coordenadas):     # Verificar que la entrada sea del tipo esperado
            raise ValueError("La entrada debe ser una lista de tuplas de tres elementos")
        return [np.array(coor).reshape(4, 1) for coor in coordenadas]                       # Convertir cada tupla en una matriz 4x1
    except Exception as e:
        print("Error al convertir coordenadas a matrices:", str(e))
        return None
    
def matrix_mult(X):
    k = build_projection_matrix(1200, 900, 90)
    #X = [X[0], X[1], X[2]]
    X = [X[1], -X[2], X[0]]
    point_img = np.dot(k, X)
    # Normalize
    point_img[0] /= point_img[2]
    point_img[1] /= point_img[2]
    return point_img[0:2]

def Prepare_lidar_data(detecciones_lidar):
    puntos = []
    colores = []
    indices= []

    matrices = matrix_type_converter(detecciones_lidar)
    for j in range(len(matrices)):
        # if -11 < detecciones_lidiar[j][1] < 11 and detecciones_lidiar[j][0] > 1 and detecciones_lidiar[j][2] > -0.8:
        if(matrices[j][1] > -11 and matrices[j][1] < 11):
            if(matrices[j][0] > 1):
                if(matrices[j][2] > -0.8 ):
                    colores.append(color_por_distancia(detecciones_lidar[j][0]))
                    punto = matrix_mult(matrices[j])
                    indices.append(j)
                    puntos.append(punto)
    return puntos, colores, indices

def Prepare_lidar_data_peaton(detecciones_lidar):
    puntos = []
    colores = []
    indices= []

    matrices = matrix_type_converter(detecciones_lidar)
    for j in range(len(matrices)):
        colores.append(color_por_distancia(detecciones_lidar[j][0]))
        punto = matrix_mult(matrices[j])
        indices.append(j)
        puntos.append(punto)
    return puntos, colores, indices

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

#Radar 
def matrix_type_converter_rardar(coordenadas_radar):
    puntos_radar = []
    for coor in coordenadas_radar:
        punto = polares_2_cartesianas(coor[1] * np.pi, coor[2] * np.pi, coor[3], coor[0])    
        puntos_radar.append(punto)
    matrices_radar = []
    for tup in puntos_radar:
        matrices_radar.append(np.array(tup).reshape(4, 1))
    return puntos_radar,matrices_radar

def matrix_mult_radar(X):
    k = build_projection_matrix(1200, 900, 90)
    X = [X[2], -X[0], X[1]]
    X = [X[1], -X[2], X[0]]
    point_img = np.dot(k, X)
    # Normalize
    point_img[0] /= point_img[2]
    point_img[1] /= point_img[2]
    return point_img[0:3]

def polares_2_cartesianas(azimuth, altitude, depth, v):
    x = depth * np.sin(altitude) * np.cos(azimuth)
    y = depth * np.sin(altitude) * np.sin(azimuth)
    z = depth * np.cos(altitude)
    return [x, y, z, v]

# Trazado peatón

def Posición_Real(input_text):
    data_control = np.genfromtxt(input_text, delimiter=",")
    x = []
    y = []
    z = []
    v_x = []
    v_y = []
    v_z = []

    for data in data_control:
        x.append(float(data[9:10])) 
        y.append(float(data[10:11]))
        z.append(float(data[11:12]))
        v_x.append(float(data[6:7]))
        v_y.append(float(data[7:8]))
        v_z.append(float(data[8:9])) 
    return x, y, v_x, v_y

def Obtener_lidar_ObjetosDetectados(coordenadas_yolo, detecciones_lidar, puntos_lidar, indices):
    trazado_person = []
    trazado_coche = []
    for deteccion in coordenadas_yolo:
        match deteccion[0]:
            case 0:
                peaton = deteccion[1:]
                x2 = peaton[0] - peaton[2] / 2
                y2 = peaton[1] - peaton[3] / 2
                rectangulo = patches.Rectangle((x2 * 1200, -y2 * 900), 
                                           peaton[2] * 1200, 
                                           -peaton[3] * 900,
                                        linewidth=1, facecolor='r')
                for punto, i in zip(puntos_lidar, indices):
                    punto_evaluable = [float(punto[0][0]), float(-punto[1][0])]
                    if rectangulo.contains_point(punto_evaluable):
                        trazado_person.append(detecciones_lidar[i])
                        pass
                    
            case 2:
                coche = deteccion[1:]
                x2 = coche[0] - coche[2] / 2
                y2 = coche[1] - coche[3] / 2
                rectangulo = patches.Rectangle((x2 * 1200, -y2 * 900), 
                                           coche[2] * 1200, 
                                           -coche[3] * 900,
                                        linewidth=1, facecolor='r')
                for punto, i in zip(puntos_lidar, indices):
                    punto_evaluable = [float(punto[0][0]), float(-punto[1][0])]
                    if rectangulo.contains_point(punto_evaluable):
                        trazado_coche.append(detecciones_lidar[i])
                        pass
            case 7:
                coche = deteccion[1:]
                x2 = coche[0] - coche[2] / 2
                y2 = coche[1] - coche[3] / 2
                rectangulo = patches.Rectangle((x2 * 1200, -y2 * 900), 
                                           coche[2] * 1200, 
                                           -coche[3] * 900,
                                        linewidth=1, facecolor='r')
                for punto, i in zip(puntos_lidar, indices):
                    punto_evaluable = [float(punto[0][0]), float(-punto[1][0])]
                    if rectangulo.contains_point(punto_evaluable):
                        trazado_coche.append(detecciones_lidar[i])
                        pass
            case _:
                pass
            
    # Encontrar punto de contacto con el peatón
    if trazado_person:
        max_capture_zone = min(trazado_person, key=lambda row: row[0])[0] + 0.3 # Peaton width (lil)
        trazado_person = [p_lidar for p_lidar in trazado_person if 0 < p_lidar[0] <= max_capture_zone]

    return trazado_person, trazado_coche

def Combinar_archivos_ply(directorio, archivo_salida):
        todos_vertices = []

        file_numbers = sorted([int(f.split('.')[0]) for f in os.listdir(directorio)])
        sequences = []
        current_sequence = [file_numbers[0]]

        for num in file_numbers[1:]:
            if num == current_sequence[-1] + 1:
                current_sequence.append(num)
            else:
                if len(current_sequence) > 1:
                    sequences.append(current_sequence)
                current_sequence = [num]
        if len(current_sequence) > 1:
            sequences.append(current_sequence)
        successive_files = [f"{num:06d}.ply" for seq in sequences for num in seq]
        #print(len(successive_files))

        for archivo in successive_files:
            if archivo in successive_files:
                archivo_ply = os.path.join(directorio, archivo)
                vertices = leer_coordenadas_lidiar(archivo_ply)
                print(vertices[0])
                for i in range(len(vertices)):
                    
                    x = 2 + (vertices[i][0] % 1)
                    nueva_tupla = (x, vertices[i][1], vertices[i][2], vertices[i][3])
                    todos_vertices.append(nueva_tupla) 
                    '''if vertices[i][0] >= 3:
                    else:
                        todos_vertices.append(vertices)'''
                    #todos_vertices.extend(vertices)
        escribir_archivo_ply(todos_vertices, archivo_salida)