import logging
logging.basicConfig(level=logging.DEBUG)

path = "detecciones/"

def ToFile(file, objects):
    #file -> Nombre del archivo sobre el que se han realizado las detecciones
    #obj -> "Objetos" detectados
    
    logging.info("Escribiendo la informacion de las detecciones...")
    
    #Creo un archivo nuevo
    file_name = path + file + "_detections.txt"
    logging.info("Nombre del archivo: " + file_name)
    f = open(file_name, "w") # x -> Create - will create a file, returns an error if the file exist
                        # a -> Append - will create a file if the specified file does not exist
                        # w -> Write - will create a file if the specified file does not exist
    
    #Recorro los objetos detectados y los escribo en el archivo .txt
    for i, object in enumerate(objects):
        #Tipo
        tipo = object.type
        #Posicion -> [0, 1, 2]
        position = object.t
        #Alto
        alto = object.h
        #Ancho
        ancho = object.w
        #Largo
        largo = object.l
        #Orientacion
        orientacion = object.ry
        #Porcentaje de acierto
        porcentaje = object.score
        
        #Escribimos
        final = str(tipo) + ";" + str(position[0]) + ";" + str(position[1]) + ";" + str(position[2]) + ";" + str(alto) + ";" + str(ancho) + ";" + str(largo) + ";" + str(orientacion) + ";" + str(porcentaje)
        
        if i == (len(objects) - 1):
            f.write(final) #Escribo en el archivo
        else:
            f.write(final + "\r") #Escribo en el archivo
        
    #Cerramos el archivo
    f.close()

    #open and read the file after the appending:
    f = open(file_name, "r")
    logging.debug(f.read())
    f.close()
    
    logging.info("¡Tarea finalizada con exito!")
