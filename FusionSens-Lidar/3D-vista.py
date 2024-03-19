import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def leer_coordenadas_lidiar(): # Input nombre de archivo
    nombre_archivo = "FusionSens/lidar/000547.ply"
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()    #Líneas[i][8] Comienzan las coordenadas
            del lineas[0:8]
            # [i][tuple(map(float, linea.strip().split()[i][1:])) for linea in lineas] 
            return [tuple(map(float, linea.split()[:-1])) for linea in lineas ]
        #[i][tuple(map(float, linea.split()[i][:-1])) + (1,) for linea in lineas]
            
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no existe.")
    except Exception as e:
        print(f"Error al leer las coordenadas desde {nombre_archivo}: {e}")


coordenadas_laser = leer_coordenadas_lidiar() 
z_coords = [coord[2] for coord in coordenadas_laser]
z_ords = z_coords.sort()
# Crear la figura
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Dibujar puntos
left=0
#print(len(coordenadas_laser)) 11024

for i in range(0,len(coordenadas_laser)):
    if(coordenadas_laser[i][1] > -11 and coordenadas_laser[i][1] < 10.7):
            if(coordenadas_laser[i][0] > 2 and coordenadas_laser[i][0] < 20):
                if(coordenadas_laser[i][2] > -0.8 ):
                    ax.scatter(coordenadas_laser[i][0], coordenadas_laser[i][1], coordenadas_laser[i][2], c='r', marker='o', alpha=0.05)

opcion = int(input("Seleccione la opción \n(1: desde arriba, 2: Lateral, 3: predeterminada)\nEnter: "))
if opcion == 1:
    ax.view_init(elev=90, azim=0)  # Desde arriba
elif opcion == 2:
    ax.view_init(elev=0, azim=-90)  # Lateral
else:
    ax.view_init(elev=0, azim=0)  # Frontal


ax.set_xlim(-1, 25)  # Ajustar los límites del eje x según sea necesario
ax.set_ylim(-20, 20)  # Ajustar los límites del eje y según sea necesario
ax.set_zlim(-3, 10)  # Ajustar los límites del eje z según sea necesario
plt.show()
