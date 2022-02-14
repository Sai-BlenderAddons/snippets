# coding=UTF-8

'''
2022/02/10 
start collect code snippets
'''

import bpy
import os, ntpath
import re

# context

def context_collect_objects(mode: str, type: str) -> list:
    ''' mode: "ALL/SELECTION"
        type: "MESH/CURVE/SURFACE/LIGHT...etc"
    '''
    objects = None

    if mode == 'ALL':
        objects = [obj for obj in bpy.context.scene.objects if obj.type == type]
    elif mode == 'SELECTION':
        objects = [obj for obj in bpy.context.selected_objects if obj.type == type]

    return objects

# datablock operators

def datablock_op_remove_image(images: list) -> list: 
    '''remove image block, if None remove all image block
    '''
    [bpy.data.images.remove(image) for image in images]

    return bpy.data.images

def datablock_op_fix_image_name() -> list:
    '''force image block name as file name
    '''
    images = [image for image in bpy.data.images if image.name !="Render Result"]
    for image in images:
        image.name = ntpath.basename(image.filepath)

    images = [image for image in bpy.data.images if image.name !="Render Result"]
    return images 

def datablock_collect_materials(mode: str) -> list:
    '''mode: "ALL/SELECTION"
    '''
    objects = None
    materials = None

    if mode == 'ALL':
        materials = bpy.data.materials
    elif mode == 'SELECTION':
        objects = bpy.context.selected_objects
        materials = []
        for obj in objects:
            material_slots = obj.material_slots
            for slot in material_slots:
                if slot.material not in materials:
                    materials.append(slot.material)

    return materials

def datablock_collect_images(mode: str) -> list:
    '''mode: "ALL/SELECTION"
    '''
    images = []

    if mode == 'ALL':
        images = [image for image in bpy.data.images if image.name !="Render Result"]
    elif mode == 'SELECTION':
        materials = []
        objects = bpy.context.selected_objects
        for obj in objects:
            material_slots = obj.material_slots
            for slot in material_slots:
                if slot.material not in materials:
                    materials.append(slot.material)
        
        images = []
        for material in materials:
            node_images = [node.image for node in material.node_tree.nodes if node.type == 'TEX_IMAGE' and node.image is not None]
            [images.append(image) for image in node_images if image not in images]

    return images

# mesh object operators

def object_op_remove_uvlayer(obj: object):
    if obj.type == 'MESH':
        uv_layers = (bpy.context.object.data.uv_layers)
        [uv_layers.remove(uv_layer) for uv_layer in reversed(uv_layers) if uv_layer.active_render is False]
    return uv_layers