import matplotlib.patches as patches
from Proyeccion_2D import matrix_mult, matrix_mult_radar, matrix_type_converter

# Yolov5
def draw_rect(coordenadas, ax):
    colores = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    for i in range(len(coordenadas)):
        x2 = coordenadas[i][0] - coordenadas[i][2] / 2
        y2 = coordenadas[i][1] - coordenadas[i][3] / 2
        rectangulo = patches.Rectangle((x2 * 1200, -y2 * 900), coordenadas[i][2] * 1200, -coordenadas[i][3] * 900 ,
                                        linewidth=1, edgecolor=colores[i % len(colores)], facecolor='none')
        ax.add_patch(rectangulo)


# Lidar
def draw_lidar(puntos_2D, colores, ax): 
    for point, color in zip(puntos_2D, colores):
        ax.plot(point[0], -point[1], color + 'o', markersize=2, alpha=0.5)
    
# Radar
# Tasks: Cambiar iterador draw_radar()

def draw_radar(coordenadas_radar, puntos_radar, matrices_radar, ax):
    for k in range(len(coordenadas_radar)):    
        r, g, b = norm_v(puntos_radar[k][3])
        pun= matrix_mult_radar(matrices_radar[k])
        ax.plot(pun[0], -pun[1], color=(r/255, g/255, b/255), markersize=2,marker='o')

def clamp(min_value, max_value, value):
    return max(min_value, min(max_value, value))

def norm_v(v):
    norm_velocity = v/ 7.5 # range [-1, 1]
    r = int(clamp(0.0, 1.0, 1.0 - norm_velocity) * 255.0)
    g = int(clamp(0.0, 1.0, 1.0 - abs(norm_velocity)) * 255.0)
    b = int(abs(clamp(- 1.0, 0.0, - 1.0 - norm_velocity)) * 255.0)
    return r,g,b