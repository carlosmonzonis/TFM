# -*- coding: utf-8 -*-
"""
Created on Wed Sep 16 19:10:32 2020

@author: carlo
"""

import numpy as np
import struct
from open3d import *

def convert_kitti_bin_to_pcd(binFilePath):
    size_float = 4
    list_pcd = []
    with open(binFilePath, "rb") as f:
        byte = f.read(size_float * 4)
        while byte:
            x, y, z, intensity = struct.unpack("ffff", byte)
            list_pcd.append([x, y, z])
            byte = f.read(size_float * 4)
    np_pcd = np.asarray(list_pcd)
    pcd = geometry.PointCloud()
    pcd.points = utility.Vector3dVector(np_pcd)
    io.write_point_cloud("D:/OneDrive/Estudios/Master/TFMA/Nubes/007403/007403.pcd", pcd)
    return 0

def convert_pcd_to_kitti_bin(pcdFilePath):
    file = io.read_point_cloud(pcdFilePath)
    
    final_file = open("D:/OneDrive/Estudios/Master/TFMA/Nubes/Prueba 2/009000.bin", "wb")
    
    for i, point in enumerate(file.points):
        byte = struct.pack("ffff", point[0], point[1], point[2], 0.05)
        final_file.write(byte)
        
    final_file.close()

    return 0

#convert_kitti_bin_to_pcd("D:/OneDrive/Estudios/Master/TFMA/Nubes/007403/007403.bin")
convert_pcd_to_kitti_bin("D:/OneDrive/Estudios/Master/TFMA/Nubes/Prueba 2/009000.pcd")