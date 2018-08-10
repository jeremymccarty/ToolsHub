# Big Bang Environment Setup Tool
# Version 1.2
# Created by Jeremy McCarty, 2017-2018
# All content © 2018 DigiPen (USA) Corporation and Jeremy McCarty, all rights reserved.

import maya.cmds as cmds

def Startup(self):
	# Set linear units to cm
	cmds.currentUnit( linear='cm' )

	# Change grid size to 1000 length and width, 10 grids every line, and 1 subdivision
	cmds.grid( size=500, spacing=10, d=1 )
	cmds.optionVar (fv=("gridDivisions",1))
	cmds.optionVar (fv=("gridSize",500))
	cmds.optionVar (fv=("gridSpacing",10))

	# Make a reference cube that is 1/1/1
	cmds.polyCube( sx=1, sy=1, sz=1, h=100, w=100, d=100 )
	cmds.CenterPivot()

def Reset(self):
	# Reset to default
	# Set linear units to cm
	cmds.currentUnit( linear='cm' )

	# Change grid size to 1000 length and width, 10 grids every line, and 1 subdivision
	cmds.grid( size=12, spacing=5, d=5 )
	cmds.optionVar (fv=("gridDivisions",5))
	cmds.optionVar (fv=("gridSize",12))
	cmds.optionVar (fv=("gridSpacing",5))

def WindowSetup():
	# Make the window
	window = cmds.window(title="Big Bang: Environment Setup Tool", widthHeight=(200, 100))

	# Set up the columns
	cmds.columnLayout(adjustableColumn=True)

	# Format with a seperator
	cmds.separator(style='none', height=15)
	cmds.text( label='Would you like to setup the environment or reset?', align='center', wordWrap=True )
	cmds.separator(style='none', height=15)

	# Make a row for the Startup and Reset buttons
	cmds.rowLayout(nc=2, columnAlign2=("right", "right"))
	cmds.button(label="Setup", width=100, backgroundColor=(.2,.4,.2), command=Startup)
	cmds.button(label="Reset", width=100, backgroundColor=(.4,.2,.2), command=Reset)
	cmds.setParent("..")

	cmds.showWindow( window )

WindowSetup()
