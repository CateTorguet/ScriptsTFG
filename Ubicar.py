import os
import shutil

def count_dir():
    try:
        archivos = os.listdir("Recursos/2D_Yolo_labels")       # Lista todos los archivos en la carpeta
        return len(archivos)                       # Devuelve el número de archivos
    except OSError:
        return -1

def Ubicar_img(j):
    return "Recursos/RGB_camera/" + f"{j:06d}.png"

def Ubicar_ply(i):
    return "Recursos/3D_lidar/" + f"{i:06d}.ply"

def Ubicar_txt(i):
    return "Recursos/2D_Yolo_labels/" + f"{i:06d}.txt"

def Capturar_labels():
    
    base_dir = r'C:\Users\Pablo\Desktop\IA\runs\detect'
    dest_dir = r'C:\Users\Pablo\Desktop\IA\Recursos\2D_Yolo_labels'
    for root, dirs, files in os.walk(base_dir):
        if os.path.basename(root) == 'labels':
                file_path = os.path.join(root, files[0])
                shutil.move(file_path, os.path.join(dest_dir, files[0]))
        else:
            pass

def Ubicar_txt_radar(i):
    return "Recursos/3D_Radar/" + f"{i:06d}.txt"