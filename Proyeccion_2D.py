import numpy as np


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