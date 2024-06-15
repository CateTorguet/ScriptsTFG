def escribir_archivo_ply(vertices, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        archivo.write("ply\n")
        archivo.write("format ascii 1.0\n")
        archivo.write("element vertex {}\n".format(len(vertices)))
        archivo.write("property float x\n")
        archivo.write("property float y\n")
        archivo.write("property float z\n")
        archivo.write("property float32 I\n")
        archivo.write("end_header\n")
        for vertice in vertices:
            archivo.write("{} {} {} {}\n".format(vertice[0], vertice[1], vertice[2], vertice[3]))