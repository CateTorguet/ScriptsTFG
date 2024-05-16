import numpy as np
import matplotlib.patches as patches 

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

def Prepare_lidar_data(detecciones_lidiar):
    puntos = []
    colores = []
    indices= []

    matrices = matrix_type_converter(detecciones_lidiar)
    for j in range(len(matrices)):
        # if -11 < detecciones_lidiar[j][1] < 11 and detecciones_lidiar[j][0] > 1 and detecciones_lidiar[j][2] > -0.8:
        if(matrices[j][1] > -11 and matrices[j][1] < 11):
            if(matrices[j][0] > 1):
                if(matrices[j][2] > -0.8 ):
                    colores.append(color_por_distancia(detecciones_lidiar[j][0]))
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

def Obtener_lidar_ObjetosDetectados(coordenadas_yolo, detecciones_lidar, puntos_lidar, indices):
    trazado_person = []
    for categoria in coordenadas_yolo:
        match categoria[0]:
            case 0:
                peaton = categoria[1:]
                x2 = peaton[0] - peaton[2] / 2
                y2 = peaton[1] - peaton[3] / 2
                rectangulo = patches.Rectangle((x2 * 1200, -y2 * 900), 
                                           peaton[2] * 1200, 
                                           -peaton[3] * 900,
                                        linewidth=1, facecolor='r')
                for punto, i in zip(puntos_lidar, indices):
                    if rectangulo.contains_point(punto):
                        # Capture
                        trazado_person.append(detecciones_lidar[i])
                        pass
                    
            case 2:
                print("._. Coche")
            case 7:
                print("PickUp Some Whatevah")
            case _:
                pass