import argparse
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import tqdm as tq
from Ubicar import *
from Leer_Detecciones import *
from Draw import *
from Proyeccion_2D import *         # Importa write_ply


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
    for i in tq.tqdm(range(499, 499+count_dir())):
        
        #Read
        nombre_archivo = Ubicar_txt(i) 
        coordenadas_yolo = leer_coordenadas_yolo(nombre_archivo)

        nombre_img = Ubicar_img(i)
        # Poner imágenes sin la detección ed yolo
        background_img = mpimg.imread(nombre_img)
        
        nombre_ply = Ubicar_ply(i)
        #nombre_ply = "Peaton_lidar.ply"
        detecciones_lidar = leer_coordenadas_lidiar(nombre_ply)
        puntos_2D_lidar, colores, indices = Prepare_lidar_data(detecciones_lidar)

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

    
        draw_lidar(puntos_2D_lidar, colores, ax)
        #draw_rect(coordenadas_yolo, ax)
        #draw_radar(coordenadas_radar, puntos_radar, matrices_radar, ax)
            # Trazado Peaton
        trazado_person, trazado_coche = Obtener_lidar_ObjetosDetectados(coordenadas_yolo, detecciones_lidar, puntos_2D_lidar, indices)
        # Detección de peatón para la captura de ply
        if trazado_person:
            escribir_archivo_ply(trazado_person, f"Correlación_Ply_txt/peaton/{i:06d}.ply")
        #if trazado_coche:
        #    escribir_archivo_ply(trazado_coche, f"trazado/coche/{i:06d}.ply")

        # Guarda y mostrar           Argumentos para el guardado de los eventos {}   #plt.savefig('results/Laser-Traces/lidiar-' + str(i), bbox_inches='tight'
        if(args.img):
            ax.imshow(background_img, extent=[0, 1200, -900, 0])
        if(args.save):
            plt.savefig('results/Laser-Traces-img/lidiar-' + str(i), bbox_inches='tight')
        if(args.s):
            plt.show()
        plt.close()
    # Post-Procesado
    print("Ply-Calentito")
    Combinar_archivos_ply(directorio= "Correlación_Ply_txt/peaton" , archivo_salida= "Peaton_lidar.ply")
    exit()
    # 1.9 < 2.2
    '''
    Task Igualar columa de X a los valores más cercanos para poder mostrarla a timepo real
    '''
    Posición_Real('Tal.txt')
    