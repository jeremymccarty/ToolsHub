# Houdini Rock Generator
# Version 1.4
# Created by Jeremy McCarty, 2017-2018
# All content © 2018 DigiPen (USA) Corporation and Jeremy McCarty, all rights reserved.

# clear the session
hou.hipFile.clear()

# make a new geo node
geo = hou.node('/obj').createNode('geo')

# clear the file node
geo.children()[0].destroy()

# add a box module
box = geo.createNode('box')

# add an iso offset node
iso = geo.createNode('isooffset')

# move the node to a new position
iso.setPosition([1, -1])

# add a scatter node
scatter = geo.createNode('scatter')

# move the node to a new position
scatter.setPosition([1, -1.5])

# add a fracture node
fracture = geo.createNode('voronoifracture')

# move the node to a new position
fracture.setPosition([0, -2])

# add a exploded node
exploded = geo.createNode('explodedview')

# move the node to a new position
exploded.setPosition([0, -2.5])

# add a foreach subnetwork
feach = geo.createNode('foreach')

# move the node to a new position
feach.setPosition([0, -3])

# save the each node
each = feach.children()[0]

# add the delete node to the loop
de = feach.createNode('delete')

# move the node to a new position
de.setPosition([0, -0.25])

# add the switch to the loop
switch = feach.createNode('switch')

# move the node to a new position
switch.setPosition([1, -0.25])

# add a null node
nnode = feach.createNode('null')

# move the node to a new position
nnode.setPosition([1, 0])

# connect all of the necessary nodes
iso.setFirstInput(box)
scatter.setFirstInput(iso)
fracture.setInput(0, box)
fracture.setInput(1, scatter)
exploded.setFirstInput(fracture)
feach.setFirstInput(exploded)

# now the foreach nodes
de.setFirstInput(each)
switch.setInput(0, each)
switch.setInput(1, nnode)

# increase the detail
fracture.parm('addinteriordetail').set(True)
fracture.parm('planar').set(True)
fracture.parm('detailsize').set(0.07)
fracture.parm('intnoiseamp').set(0.2)
fracture.parm('intnoisetype').set('Original Perlin Noise')

# scale the cube
box.parm('sizex').set(2)
box.parm('sizey').set(2)
box.parm('sizez').set(2)
box.parm('scale').set(2)

# edit the group prefix
fracture.parm('groupprefix').set('P')

# set up the for each group mask
feach.parm('groupmask').set('P*')

# name the foreach nodes
each.setName("ALL")
de.setName("IN")

# mark the outside group for deletion
de.parm('group').set('outside')

# setup the network
expression = 'if(nprims("..//ALL") == nprims("../IN"),0,1)'
switch.parm('input').setExpression(expression)

# render the cube
switch.setDisplayFlag(True)
switch.setRenderFlag(True)
#switch.setCurrent(True, clear_all_selected=True)

feach.setDisplayFlag(True)
feach.setRenderFlag(True)
feach.setCurrent(True, clear_all_selected=True)

#TO ADJUST SCALE AND ADD CLUSTER
