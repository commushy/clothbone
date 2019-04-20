# run in edit mode with vertices selected

import bpy
from mathutils import Vector  

# sort selected vertices by ZAXIS with reverse order
#bpy.ops.mesh.sort_elements(type=‘VIEW_ZAXIS’)
# get selected vertices

myob = bpy.context.active_object  
bpy.ops.object.mode_set(mode = 'OBJECT')  
selected_idx = [i.index for i in myob.data.vertices if i.select]

isfirst = True
head_offset = Vector((0,0,0.1))

for v_index in selected_idx:
    
    # get world coordinate of the vertice
    vert_coordinate = myob.data.vertices[v_index].co  
    vert_coordinate = myob.matrix_world @ vert_coordinate
    
    if isfirst == True:
        # add armature at vert_coordinate
        bpy.ops.object.add(type='ARMATURE', enter_editmode=True)
        amt = bpy.context.object
        # add root bone
        b = amt.data.edit_bones.new(str(v_index))
        b.head = vert_coordinate + head_offset
        b.tail = vert_coordinate
        b.use_deform = False
        # set origin of object to vert_coordinate
        # create vertex goup 'pinned' from vertex
        # add object constraint "Copy Location" of root bone
        isfirst = False
    
    else:
        # parent empty
        empty = bpy.data.objects.new("Empty", None)
        empty.parent = myob
        empty.parent_type = 'VERTEX'
        empty.parent_vertices = [v_index] * 3
        bpy.context.scene.collection.objects.link(empty)
    
        # add bone at head(prev_vert_coordinate),tail(vert_coordinate)
        amt.select_set(state=True)
        bpy.ops.object.mode_set(mode='EDIT')
        b = amt.data.edit_bones.new(str(v_index))
        b.head = prev_vert_coordinate
        b.tail = vert_coordinate
        b.parent = prev_b
        b.use_connect = True
        bpy.context.scene.update()
        #bpy.ops.object.mode_set(mode='OBJECT')
        
        # set bone constraint DAMPED TRACK
        #objbone = bp.constraints
        #objbone.new('DAMPED_TRACK')
        #objbone['Damped Track'].target = empty

    # set prev_vert_coordinate  
    prev_vert_coordinate = vert_coordinate
    prev_b = b