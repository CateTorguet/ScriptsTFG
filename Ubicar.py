import os

def count_dir():
    try:
        archivos = os.listdir("runs/detect")       # Lista todos los archivos en la carpeta
        return len(archivos)                       # Devuelve el número de archivos
    except OSError:
        return -1

def Ubicar_img(j):
    if(j == 499):
        nombre_img = "runs/detect" + "/exp/" + f"{j:06d}.png"
    else:
        num = j-498
        nombre_img = "runs/detect" + "/exp"+str(num) + "/" + f"{j:06d}.png"
    return nombre_img

def Ubicar_ply(i):
    return "FusionSens-Lidar/lidar/" + f"{i:06d}.ply"

def Ubicar_txt(i):
    if(i == 499):
        dir = "runs/detect" + "/exp" + "/labels/"+ f"{i:06d}.txt"
    else:
        num = i-498
        dir = "runs/detect" + "/exp"+str(num) + "/labels/" + f"{i:06d}.txt"
    return dir

def Ubicar_txt_radar(i):
    dir = "FusionSens-Radar/radar/" + f"{i:06d}.txt"
    return dir