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

# get name of selected armature
armature = bpy.context.object.name
print(armature)

# generate list of bones and coordinates from selected bone chain
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

# calculate normal from first 2 edges
vec1 = loclist[1]-loclist[0]
vec2 = loclist[2]-loclist[1]
vec3 = vec1.cross(vec2)
# should normalize?

print(vec1)
print(vec2)
print(vec3)

# generate all vertice coordinate and face data
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

# generate list of all vertices
loclist4 = loclist + loclist2 + loclist3

# generate mesh data
n2=len(loclist4)

print(n2)
print(loclist2)
print(loclist3)
print(loclist4)
print(facelist)

msh = bpy.data.meshes.new(name="physmesh")
msh.from_pydata(loclist4, [], facelist)
msh.update()

# create new object from mesh
obj = bpy.data.objects.new(name="physobj", object_data=msh)

# link new object to scene
scene = bpy.context.scene
scene.collection.objects.link(obj)

# get world coordinate of vertice 0
origin_coordinate = obj.data.vertices[0].co
origin_coordinate = origin_coordinate @ obj.matrix_world

# set origin of object to origin_coordinate using 3d cursor
obj.select_set(state=True)
bpy.ops.object.mode_set(mode = 'OBJECT')  
saved_location = bpy.context.scene.cursor.location
bpy.context.scene.cursor.location = origin_coordinate
bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
bpy.context.scene.cursor.location = saved_location

