aux = img_paths[0].split('\\')
name = aux[len(aux) - 1]
aux = name.split('.')
name = aux[0]
#Escribo los objetos en el archivo
Writter.ToFile(name, objects_pred)