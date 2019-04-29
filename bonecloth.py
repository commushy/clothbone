# run in pose mode with bone chain selected
# currently generate mesh only

import bpy
import bmesh
from mathutils import Vector  

loclist=[]
loclist2=[]
loclist3=[]

facelist=[]
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
    
print(bonelist)
print(loclist)

vec1 = loclist[1]-loclist[0]
vec2 = loclist[2]-loclist[1]
vec3 = vec1.cross(vec2) #normal vector of first 2 edges

print(vec1)
print(vec2)
print(vec3)

n = len(loclist)
print(n)

for vidx in range(n):
    v=loclist[vidx]
    print(v)
    loclist2.append(v+vec3)
    loclist3.append(v-vec3)
    if vidx < n-1: 
        facelist.append([vidx,vidx+1,vidx+n+1,vidx+n])
        facelist.append([vidx,vidx+1,vidx+n*2+1,vidx+n*2])

loclist4 = loclist + loclist2 + loclist3

n2=len(loclist4)

print(n2)
print(loclist2)
print(loclist3)
print(loclist4)
print(facelist)

msh = bpy.data.meshes.new(name="physmesh")
msh.from_pydata(loclist4, [], facelist)
msh.update()

obj = bpy.data.objects.new(name="physobj", object_data=msh)
scene = bpy.context.scene
scene.collection.objects.link(obj)

