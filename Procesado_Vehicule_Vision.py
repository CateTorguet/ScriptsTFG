import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from Ubicar import *
from Leer_Detecciones import *
from Draw import *
from Proyeccion_2D import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Comprobación sobre el control de las coordenadas en las que se detecto actividad.") 
    parser.add_argument("-img", action="store_true", help="Mostrar imagen de fondo.")
    parser.add_argument("-s", action="store_true", help="Mostrar gráfico.")
    parser.add_argument("--save", action="store_true", help="Guardar Resultados")
    parser.add_argument("--n", type=int, default=float('inf'), help="Número máximo de rectángulos a dibujar.")
    args = parser.parse_args()
# Se añade la lectura de un fichero  coordenadas = []
# coordenadas.append(coordenadas_yolo)   
    puntos_peatón = []
    for i in range(499, 499+count_dir()):
        #Read   
        nombre_archivo = Ubicar_txt(i) 
        coordenadas_yolo = leer_coordenadas_yolo(nombre_archivo)

        nombre_img = Ubicar_img(i)
        background_img = mpimg.imread(nombre_img)
        
        nombre_ply = Ubicar_ply(i)
        detecciones_lidiar = leer_coordenadas_lidiar(nombre_ply)
        puntos_2D, colores, indices = Prepare_lidar_data(detecciones_lidiar)

        nombre_radar = Ubicar_txt_radar(i)
        coordenadas_radar = leer_coordenadas_radar(nombre_radar)
        puntos_radar, matrices_radar = matrix_type_converter_rardar(coordenadas_radar)

        #Draw
        fig, ax = plt.subplots()
        ax.set_xlim(0, 1200)
        ax.set_ylim(-900, 0)
        ax.set_aspect('equal', adjustable='datalim')
        ax.set_frame_on(False)
        plt.title(f'Verificación de funcionamiento - Archivo-{str(i - 498)}')              

        
        #draw_lidar(detecciones_lidiar, ax)
        draw_lidar(puntos_2D, colores, ax)
        draw_rect(coordenadas_yolo, ax)
        draw_radar(coordenadas_radar, puntos_radar, matrices_radar, ax)
        
        # Guarda y mostrar           Argumentos para el guardado de los eventos {}   #plt.savefig('results/Laser-Traces/lidiar-' + str(i), bbox_inches='tight'
        if(args.img):
            ax.imshow(background_img, extent=[0, 1200, -900, 0])
        if(args.save):
            plt.savefig('results/Laser-Traces-img/lidiar-' + str(i), bbox_inches='tight')
        if(args.s):
            plt.show()
        plt.close()