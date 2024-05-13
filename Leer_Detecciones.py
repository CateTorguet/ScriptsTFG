def leer_coordenadas_yolo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            ##coordenadas_aux = [tuple(map(float, linea.strip().split()[1:])) for linea in lineas]                                  
            '''for linea in lineas:
                linea = linea.replace(',','')'''
                                                        # línea = (x, y, width, height)   [(x, y, width, height),(x, y, width, height),...]
                                                                                            # map (type converter) + split 
            return [tuple(map(float, linea.split()[1:])) for linea in lineas]               # Devuelve una lista de cada fila (file)
    except FileNotFoundError:
        return f"El archivo '{nombre_archivo}' no fue encontrado."
    except Exception as e:
        return f"Ocurrió un error: {e}"
    
def leer_coordenadas_lidiar(nombre_archivo): 
    try:
        with open(nombre_archivo, 'r') as archivo:

            lineas = archivo.readlines()    #Líneas[8] Comienzan las coordenadas
            del lineas[0:8]
            return [tuple(map(float, linea.split()[:-1])) + (1,) for linea in lineas]  #[tuple(map(float, linea.split()[:-1])) + (1,) for linea in lineas]
        
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no existe.")
    except Exception as e:
        print(f"Error al leer las coordenadas desde {nombre_archivo}: {e}")

def leer_coordenadas_radar(nombre_archivo):
    try:
        with open(nombre_archivo, 'r') as archivo:
            lineas = archivo.readlines()
            return [tuple(map(float, linea.split(','))) for linea in lineas]
    except FileNotFoundError:
        print(f"Error: El archivo {nombre_archivo} no existe.")
    except Exception as e:
        print(f"Error al leer las coordenadas desde {nombre_archivo}: {e}")

        