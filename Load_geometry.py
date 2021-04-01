bl_info = {
    "name": "Load Geometry",
    "author": "Monzonís, Calos",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Add > Mesh > New Object",
    "description": "Carga la geometria y posiciona una geometria según el archivo leido.",
    "warning": "",
    "doc_url": "",
    "category": "Add Mesh",
}

import bpy
from bpy.props import (StringProperty,
                       PointerProperty,
                       )

from bpy.types import (Panel,
                       Operator,
                       AddonPreferences,
                       PropertyGroup,
                       )
                       
from bpy_extras.object_utils import AddObjectHelper, object_data_add

def add_object(self, context):
    #Fichero donde se almacenan los path hasta las geometrias
    path = "D:\OneDrive\Estudios\Master\TFMA\Remplaciamiento\Files_Path.txt"
    file_goemtries_locations = open(path, r)
    contents = file_goemtries_locations.read()
    
    #Almaceno las geometrias en un array, siguiendo el orden
    Path_Locations = contents.spit('\n')     #0 -> Car | 1 -> Pedestrian ...
    #Files_Locations = 'D:\OneDrive\Estudios\Master\TFMA\Remplaciamiento\Lexus\lexus_hs.obj'
    
    #Leo el fichero donde estan las deteciones
    path = ""
    file_detections = open(path, r)
    contents = file_detections.read()
    #Almaceno las detecciones en un array
    Detections = contents.spit('\n')
    
    #Recorro el array de detecciones
    for Detection in Detections:
        #Saco la informacion de la deteccion
        Info = Detection.split(';')
        tipo = Info[0]
        p_x = Info[1]
        p_y = Info[2]
        p_z= Info[3]
        s_h = Info[4]
        s_w = Info[5]
        s_l = Info[6]
        r_y = Info[7]
        #Cargo cargo la geometria correcta y la coloca en la escena
        imported_object = bpy.ops.import_scene.obj(filepath=file_loc)
        #Selecciono el objeto que acabo de cargar
        obj_object = bpy.context.selected_objects[0]
        #Modifico su posicion
        
        #Modifico su oriantacion
        

class OBJECT_OT_add_object(Operator, AddObjectHelper):
    """Carga la geometria y la posiciono según el archivo detecciones leido"""
    bl_idname = "mesh.add_object"
    bl_label = bl_info.get("name")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        add_object(self, context)
        return {'FINISHED'}


# Registration
def add_object_button(self, context):
    self.layout.operator(
        OBJECT_OT_add_object.bl_idname,
        text=bl_info.get("name"),
        icon='PLUGIN')


# This allows you to right click on a button and link to documentation
def add_object_manual_map():
    url_manual_prefix = "https://docs.blender.org/manual/en/latest/"
    url_manual_mapping = (("bpy.ops.mesh.add_object", "scene_layout/object/types.html"),)
    return url_manual_prefix, url_manual_mapping

def register():
    bpy.utils.register_class(OBJECT_OT_add_object)
    bpy.utils.register_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.append(add_object_button)

def unregister():
    bpy.utils.unregister_class(OBJECT_OT_add_object)
    bpy.utils.unregister_manual_map(add_object_manual_map)
    bpy.types.VIEW3D_MT_mesh_add.remove(add_object_button)

if __name__ == "__main__":
    register()
