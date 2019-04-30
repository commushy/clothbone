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

# need update: get armature reference from selected bones
armature = "Armature"

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

vec1 = loclist[1]-loclist[0]
vec2 = loclist[2]-loclist[1]
vec3 = vec1.cross(vec2) #normal vector of first 2 edges
vec4 = -vec3 #inverse of vec3

print(vec1)
print(vec2)
print(vec3)
print(vec4)



msh = bpy.data.meshes.new(name="physmesh")
msh.from_pydata(loclist, edgelist, [])
msh.update()

obj = bpy.data.objects.new(name="physobj", object_data=msh)
scene = bpy.context.scene
scene.collection.objects.link(obj)

