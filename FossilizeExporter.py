# Fossilize Export Tool
# Version 1.3
# Created by Jeremy McCarty, 2017-2018
# All content © 2018 DigiPen (USA) Corporation and Jeremy McCarty, all rights reserved.

import maya.cmds as cmds
import maya.mel as mm

# Open a file browser and save the directory
def browse(*args):
	# Save the directory when the dialog executes
	global directory
	directory = cmds.fileDialog2(fileMode=3, caption="Select Directory", dialogStyle=2)

	# If that argument is not null
	if directory is not None:

		# Save it globally
		global text_field
		text_field = directory[0]

		# Update the text field
		cmds.textField('directory_group', edit=True, text=text_field)

# Export the file with the saved data
def export(*args):

	# If this is a prop
	assetType = cmds.optionMenu( "asset_type", query=True, value=True)

	if assetType == "Prop":
		# Delete the history and Freeze the transformations
		cmds.DeleteHistory()
		cmds.makeIdentity(apply=True, t=1, r=1, s=1, n=0)
	
	# Change based on pivot request
	pivotValue = cmds.optionMenu( "pivot", query=True, value=True)
	if pivotValue == "Bottom Pivot":
		selected = cmds.ls(sl=True,long=True)
		for n in selected:
			bbox = cmds.exactWorldBoundingBox(n)
			bottom = [(bbox[0] + bbox[3])/2, bbox[1], (bbox[2] + bbox[5])/2]
			cmds.xform(n, piv=bottom, ws=True)
		cmds.move(0,0,0, rotatePivotRelative=True)
	elif pivotValue == "Center Pivot":
		cmds.CenterPivot()
		cmds.move(0,0,0, rotatePivotRelative=True)

	# Setup export options
	# Geometry
	mm.eval("FBXExportSmoothingGroups -v true")
	mm.eval("FBXExportHardEdges -v false")
	mm.eval("FBXExportTangents -v false")
	mm.eval("FBXExportSmoothMesh -v true")
	mm.eval("FBXExportInstances -v false")
	mm.eval("FBXExportReferencedAssetsContent -v false")
	# Animation
	mm.eval("FBXExportBakeComplexAnimation -v false")
	# mm.eval("FBXExportBakeResampleAll -v true")
	mm.eval("FBXExportUseSceneName -v false")
	mm.eval("FBXExportQuaternion -v euler")
	mm.eval("FBXExportShapes -v true")
	mm.eval("FBXExportSkins -v true")
	# Constraints
	mm.eval("FBXExportConstraints -v false")
	# Cameras
	mm.eval("FBXExportCameras -v false")
	# Lights
	mm.eval("FBXExportLights -v false")
	# Embed Media
	mm.eval("FBXExportEmbeddedTextures -v false")
	# Connections
	mm.eval("FBXExportInputConnections -v false")
	# Axis Conversion
	mm.eval("FBXExportUpAxis y")

	# Save the filename
	file_name = cmds.textField('filename_group', query=True, text=True)

	# Rename the file with the directory / type and name
	if assetType == "Prop":
		# Name the file

		cmds.file(rename=text_field + "/" + "SM_" + file_name + ".fbx")
		
		# Export the static mesh
		cmds.file(force=True, exportSelected=True, type="FBX export")

	elif assetType == "Animation":

		# Name the file
		cmds.file(rename=text_field + "/" + "AN_" + file_name + ".fbx")

		# Save the number of animation frames
		startFrame = cmds.textField('startFrame', query=True, text=True)
		endFrame = cmds.textField('endFrame', query=True, text=True)

		# Animation setup
		mm.eval("FBXExportBakeComplexAnimation -v true")
		mm.eval("FBXExportBakeComplexStart -v "+str(startFrame))
		mm.eval("FBXExportBakeComplexEnd -v "+str(endFrame))
		mm.eval("FBXExportBakeComplexStep -v 1")

		# Export the animation
		cmds.file(force=True, exportAll=True, type="FBX export")

	elif assetType == "Skeletal Mesh":

		# Name the file
		cmds.file(rename=text_field + "/" + "SK_" + file_name + ".fbx")

		# Export the skeleton
		cmds.file(force=True, exportAll=True, type="FBX export")

	# Close the GUI
	cmds.deleteUI(window, window=True)

# If the window is already created, delete it
if cmds.window('Fossilize: Dino Delivery Export Tool', exists=True):
	cmds.deleteUI('Fossilize: Dino Delivery Export Tool', window=True)
	cmds.windowPref('Fossilize: Dino Delivery Export Tool', remove=True)

# Make the window
window = cmds.window(title="Fossilize: Dino Delivery Export Tool", widthHeight=(500, 390))

# Set up the columns
cmds.columnLayout(adjustableColumn=True)

# Format with a seperator
cmds.separator(style='none', height=5)

# Asset options
cmds.text( label='File Details', align='left' )

# Format with a seperator
cmds.separator(style='in', height=15)

# Make a row with the label and text field for the filename
cmds.text( label='Filename', align='left' )
cmds.textField('filename_group')

# Format with a seperator
cmds.separator(style='none', height=5)

# Make a row with the label and text field for the directory
cmds.text( label='Folder', align='left')
cmds.textField('directory_group', text='...')

# Format with a seperator
cmds.separator(style='none', height=10)

cmds.button(label="Browse", width=100, command=browse)

# Format with a seperator
cmds.separator(style='none', height=20)

# Asset options
cmds.text( label='Asset Options', align='left' )

# Format with a seperator
cmds.separator(style='in', height=15)

# What should the pivot settings of the model be?
cmds.text( label='Pivot Location', align='left' )
cmds.optionMenu("pivot")
cmds.menuItem( label='Bottom Pivot', parent="pivot" )
cmds.menuItem( label='Center Pivot', parent="pivot" )
cmds.menuItem( label='Current Pivot', parent="pivot" )

# Format with a seperator
cmds.separator(style='none', height=5)

# What type of asset is this?
cmds.text( label='Asset Type', align='left' )
cmds.optionMenu("asset_type")
cmds.menuItem( label='Prop', parent="asset_type")
cmds.menuItem( label='Animation', parent="asset_type")
cmds.menuItem( label='Skeletal Mesh', parent="asset_type")

# Format with a seperator
cmds.separator(style='none', height=20)

# Asset options
cmds.text( label='Animation Options', align='left' )

# Format with a seperator
cmds.separator(style='in', height=15)

# Make a row for the animation frame settings
cmds.rowLayout(nc=2, columnAlign2=("left", "left"))
cmds.text( label='Start Frame            ', align='left' )
cmds.text( label='End Frame', align='left' )
cmds.setParent("..")

cmds.rowLayout(nc=2, columnAlign2=("left", "left"))
cmds.textField('startFrame')
cmds.textField('endFrame')
cmds.setParent("..")

# Format with a seperator
cmds.separator(style='in', height=20)

# Make a row for the export and cancel buttons
cmds.rowLayout(nc=2, columnAlign2=("right", "right"))
cmds.button(label="Export", width=100, backgroundColor=(.2,.4,.2), command=export)
cmds.button(label="Cancel", width=100, backgroundColor=(.4,.2,.2), command=('cmds.deleteUI(\"' + window + '\", window=True)') )
cmds.setParent("..")

cmds.showWindow( window )
