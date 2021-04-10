bl_info = {
    "name": "Complex-Yolo Importer",
    "author": "Monzonís Marti, Calos",
    "version": (1, 0),
    "blender": (2, 90, 0),
    "location": "View3D > Complex-Yolo",
    "description": "Carga la geometria y las posiciona según un archivo leido.",
    "warning": "",
    "doc_url": "",
    "category": "Add Geometry",
} 

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

import bpy
import math

CLASS_NAME_TO_ID = {
    'Car': 				0,
    'Pedestrian': 		1,
    'Cyclist': 			2,
    'Van': 				3,
    'Truck': 			4,
    'Person_sitting': 	5,
    'Tram': 			6,
    'Misc': 			7,
    'DontCare': 		8,
}

"""Extructura para la url del .txt de las geometrias"""
class WorthGroupToolsSettings(bpy.types.PropertyGroup):
    file_path: bpy.props.StringProperty(name="Geometrias",
                                        description="Ruta hasta el archivo donde estan las geometrias",
                                        default="",
                                        maxlen=1024,
                                        subtype="FILE_PATH")

"""Extructura para la url del .txt de las detecciones"""
class WorthGroupToolsSettings2(bpy.types.PropertyGroup):
    file_path: bpy.props.StringProperty(name="Detecciones",
                                        description="Ruta hasta el archivo donde estan las detecciones",
                                        default="",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
                                        
"""Extructura para la url del .ply de la nube de puntos"""
class WorthGroupToolsSettings3(bpy.types.PropertyGroup):
    file_path: bpy.props.StringProperty(name="Nube",
                                        description="Ruta hasta el archivo donde esta la nube de puntos",
                                        default="",
                                        maxlen=1024,
                                        subtype="FILE_PATH")
                                        
"""Clase del operador que ejecuta la funcion para cargar las geometrias"""
class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.operator_comlpex_yolo"
    bl_label = "Importar"
    
    text: bpy.props.StringProperty(
        name = 'geometria',
        default = ''
        )
        
    text2: bpy.props.StringProperty(
        name = 'detecciones',
        default = ''
        )
        
    text3: bpy.props.StringProperty(
        name = 'nube',
        default = ''
        )

    @classmethod
    def poll(cls, context):
        return context.active_object is None

    def execute(self, context):
        print("URL de la Nube de puntos: ", self.text3)
        print("URL de las geometrias: ", self.text)
        print("URL de las detecciones: ", self.text2)
        
        """Codigo para la carga e importacion de las geometrias"""
        #Fichero donde se almacenan los path hasta las geometrias
        path = self.text
        file_goemtries_locations = open(path, 'r')
        contents = file_goemtries_locations.read()
        
        #Almaceno las geometrias en un array, siguiendo el orden
        Geometrias = contents.split('\n')     #0 -> Car | 1 -> Pedestrian ...
        print("Geometrias: ", Geometrias)
        
        #Leo el fichero donde estan las deteciones
        path = self.text2
        file_detections = open(path, 'r')
        contents = file_detections.read()
        #Almaceno las detecciones en un array
        Detections = contents.split('\n')
        print("Detecciones: ", Detections)
        
        #Recorro el array de detecciones
        for i, Detection in enumerate(Detections):
            #Saco la informacion de la deteccion
            Info = Detection.split(';')
            tipo = CLASS_NAME_TO_ID[Info[0]]
            print("Tipo: ", tipo)
            p_x = Info[1]
            print("p_x: ", p_x)
            p_y = Info[2]
            print("p_y: ", p_y)
            p_z= Info[3]
            print("p_z: ", p_z)
            s_h = Info[4]
            s_w = Info[5]
            s_l = Info[6]
            r_y = Info[7]
            #Cargo cargo la geometria correcta y la coloca en la escena
            imported_object = bpy.ops.import_scene.obj(filepath=Geometrias[tipo])
            #Selecciono el objeto que acabo de cargar
            obj_object = bpy.context.selected_objects[0]
            #Modifico su oriantacion
            obj_object.rotation_euler[2] = float(r_y) + (90 * math.pi / 180)
            obj_object.rotation_euler[0] = 0.0
            obj_object.rotation_euler[1] = 0.0
            #Modifico su posicion
            obj_object.location[0] = float(p_z)
            obj_object.location[1] = -float(p_x)
            obj_object.location[2] = float(p_y)
            
        #importo la nube de puntos
        imported_cloud = bpy.ops.import_mesh.ply(filepath=self.text3)
        
        return {'FINISHED'}

class ImportDetections:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Complex-Yolo"
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod
    def poll(cls, context):
        return (context.object is None)


class Panel_PT_panel(ImportDetections, bpy.types.Panel):
    bl_idname = "Complex_Yolo_Import_Geometry"
    bl_label = "Import Geometry"

    def draw(self, context):
        self.layout.label(text="Introduce las url hasta los archivos que hay que leer.")
        
        row3 = self.layout.row()
        worth_group_tools3 = context.scene.worth_group_tools3
        row3.prop(worth_group_tools3, "file_path")
        
        row = self.layout.row()
        worth_group_tools = context.scene.worth_group_tools
        row.prop(worth_group_tools, "file_path")
        
        row2 = self.layout.row()
        worth_group_tools2 = context.scene.worth_group_tools2
        row2.prop(worth_group_tools2, "file_path")
        
        row = self.layout.row()
        op = row.operator("object.operator_comlpex_yolo")
        op.text = worth_group_tools.file_path
        op.text2 = worth_group_tools2.file_path
        op.text3 = worth_group_tools3.file_path

classes = (WorthGroupToolsSettings,
           WorthGroupToolsSettings2,
           WorthGroupToolsSettings3,
           SimpleOperator,
           Panel_PT_panel)
           
def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.worth_group_tools = bpy.props.PointerProperty(type=WorthGroupToolsSettings)
    bpy.types.Scene.worth_group_tools2 = bpy.props.PointerProperty(type=WorthGroupToolsSettings2)
    bpy.types.Scene.worth_group_tools3 = bpy.props.PointerProperty(type=WorthGroupToolsSettings3)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.worth_group_tools
    del bpy.types.Scene.worth_group_tools2
    del bpy.types.Scene.worth_group_tools3


if __name__ == "__main__":
    register()
