# run in pose mode with bone chain selected
# currently generate edge only

import bpy
import bmesh
from mathutils import Vector  

loclist=[]
edgelist=[]
bonelist=[]
vidx = 0
initial = True

armature = "Armature" # change this to the name of your armature 

for x in bpy.context.selected_pose_bones:
    bonelist.append(x)
    xheadloc = bpy.data.objects[armature].location + x.head
    xtailloc = bpy.data.objects[armature].location + x.tail
    
    if initial == True:
        loclist.append(xheadloc)
        loclist.append(xtailloc) 
        initial = False
    else:
        loclist.append(xtailloc)
    edgelist.append([vidx,vidx+1])
    vidx=vidx+1
    
print(bonelist)
print(loclist)
print(edgelist)

msh = bpy.data.meshes.new(name="physmesh")
msh.from_pydata(loclist, edgelist, [])
msh.update()

obj = bpy.data.objects.new(name="physobj", object_data=msh)
scene = bpy.context.scene
scene.collection.objects.link(obj)

