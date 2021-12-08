import bpy
import numpy as np
from os import listdir, path

def fbx2bvh(data_path, file):
    out_path = "D:\\tuc\\exam10\\Thesis\\Dataset\\FIXED_CMU_FBX\\"
    sourcepath = data_path+"\\"+file
    fbx_path = out_path+"\\"+file.split(".bvh")[0]+".fbx"
    bpy.ops.import_anim.bvh(filepath=sourcepath)
    bpy.ops.export_scene.fbx(filepath=fbx_path, axis_forward='-Z', axis_up='Y', use_selection=True)


data_path = "D:\\tuc\\exam10\\Thesis\\Dataset\\FIXED_CMU_BVH\\"
directories = sorted([f for f in listdir(data_path) if not f.startswith(".")])
files = directories

for file in files:    
    fbx2bvh(data_path, file)
    mynewscene = bpy.data.scenes.new(name="MyScene")
    bpy.context.window.scene = mynewscene
    break