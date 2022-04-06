# coding=UTF-8

'''
2022/02/10 
start collect code snippets
'''

import bpy
import os, ntpath
import re

# context

def select_object_hierarty_root(obj: object) -> object:
    tree = [obj]
    while obj.parent:
        obj = obj.parent
        tree.append(obj)

    return obj

def get_bbox_vertices(obj: object) -> list:
    '''obj: "mesh object"
       return lists: bbox_vertices, bbox_max, bbox_min, bbox_root
    '''
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    bbox = obj.bound_box
    bbox_vertices = [vector[:] for vector in bbox]
    bbox_vertices = [numpy.array(vertice) + obj.location for vertice in bbox_vertices]
    bbox_max_x = max([vertice[0] for vertice in bbox_vertices])
    bbox_max_y = max([vertice[1] for vertice in bbox_vertices])
    bbox_max_z = max([vertice[2] for vertice in bbox_vertices])
    bbox_min_x = min([vertice[0] for vertice in bbox_vertices])
    bbox_min_y = min([vertice[1] for vertice in bbox_vertices])
    bbox_min_z = min([vertice[2] for vertice in bbox_vertices])
    bbox_center_x = (bbox_max_x + bbox_min_x)/2
    bbox_center_y = (bbox_max_y + bbox_min_y)/2
    bbox_center_z = (bbox_max_z + bbox_min_z)/2

    bbox_max = (bbox_max_x, bbox_max_y, bbox_max_z)
    bbox_min = (bbox_min_x, bbox_min_y, bbox_min_z)
    bbox_root = (bbox_center_x, bbox_center_y, bbox_min_z)

    return bbox_vertices, bbox_max, bbox_min, bbox_root


def set_origin(obj: object, location: tuple) -> tuple:
    '''
    '''
    context = bpy.context
    # hold_selection = context.selected_objects
    [obj.select_set(False) for obj in context.selected_objects]
    cursor = context.scene.cursor
    hold_location = tuple(cursor.location)
    cursor.location = location
    obj.select_set(True)
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
    cursor.location = hold_location
    obj.select_set(False)

    return location


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