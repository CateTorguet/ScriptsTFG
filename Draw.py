import matplotlib.patches as patches
from Proyeccion_2D import matrix_mult, matrix_mult_radar

# Yolov5
def draw_rect(coordenadas, i, file, ax):
    colores = ['r', 'g', 'b', 'c', 'm', 'y', 'k']
    x2 = coordenadas[file][i][0] - coordenadas[file][i][2] / 2
    y2 = coordenadas[file][i][1] - coordenadas[file][i][3] / 2
        
    rectangulo = patches.Rectangle((x2, -y2),
                                    coordenadas[file][i][2],
                                    -coordenadas[file][i][3],
                                    linewidth=1, edgecolor=colores[i % len(colores)], facecolor='none')
    ax.add_patch(rectangulo)


#   Lidar
def draw_lidar(detecciones_lidiar, matrices, ax):
    for j in range(len(detecciones_lidiar)):
        if(detecciones_lidiar[j][1] > -11 and detecciones_lidiar[j][1] < 11):
            if(detecciones_lidiar[j][0] > 1):
                if(detecciones_lidiar[j][2] > -0.8 ):
                    punto = matrix_mult(matrices[j])
                    color = color_por_distancia(detecciones_lidiar[j][0])
                    ax.plot(punto[0], -punto[1], color + 'o', markersize=1, alpha=0.5)

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
    
# Radar
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