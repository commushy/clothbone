# run in edit mode with vertices selected

import bpy
from mathutils import Vector  

# sort selected vertices by ZAXIS with reverse order
#bpy.ops.mesh.sort_elements(type=‘VIEW_ZAXIS’)
# get selected vertices

myob = bpy.context.active_object  
bpy.ops.object.mode_set(mode = 'OBJECT')  
selected_idx = [i.index for i in myob.data.vertices if i.select]

bonelist =[]
emptylist = []

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
        b = amt.data.edit_bones.new("Clothbone")
        b.head = vert_coordinate + head_offset
        b.tail = vert_coordinate
        b.use_deform = False
        
        # set origin of object to vert_coordinate
        #myob.select_set(state=True)
        #bpy.ops.object.mode_set(mode = 'OBJECT')  
        #saved_location = bpy.context.scene.cursor.location
        #bpy.context.scene.cursor.location = vert_coordinate
        #bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        #bpy.context.scene.cursor.location = saved_location
        
        # create vertex goup 'pinned' from vertex
        # add object constraint "Copy Location" of root bone
        #objc = myob.constraints.new(type='COPY_LOCATION')
        
        #myob.select_set(state=False)
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
        b = amt.data.edit_bones.new("Clothbone")
        b.head = prev_vert_coordinate
        b.tail = vert_coordinate
        b.parent = prev_b
        b.use_connect = True
        bpy.context.scene.update()
        
        bonelist.append(b)
        emptylist.append(empty)

    # set prev_vert_coordinate  
    prev_vert_coordinate = vert_coordinate
    prev_b = b
    
for b, empty in zip(bonelist, emptylist):
        #bpy.ops.object.mode_set(mode='OBJECT')
        
        # set bone constraint DAMPED TRACK
        bpy.ops.object.mode_set(mode='POSE')
        bp = amt.pose.bones[b.name]
        objbone = bp.constraints
        objbone.new('DAMPED_TRACK')
        objbone['Damped Track'].target = empty
