from pyglet.graphics import draw
from pyglet.gl import (GL_TRIANGLE_STRIP, GL_BLEND, glEnable, glBlendFunc, 
    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, glIsEnabled)
from math import cos, sin, sqrt

"""Module that store function to draw Tree object using pyglet

To use this module pyglet must be installed
"""

def drawOrientedRectangle(x, y, dir_x, dir_y, width, height, r, g, b, a):
	"""Draw an oriented rectangle 
	
	Args:
		x: A floating point indicating the rectangle's x position in window
		coordinate
		y: A floating point indicating the rectangle's y position in window
		coordinate 
		dir_x: A floating point that represent the x coordinate of the vertor
			that give the direction relative to the rectangle's position of the
			side that have the height as length
		dir_y: A floating point that represent the y coordinate of the vertor
			that give the direction relative to the rectangle's position of the
			side that have the height as length
		width: A float indicating the rectangle's width
		height: A float indicating the rectangle's height
		r: An integer in the range [0, 255] that represent the rectangle's
			color's red component
		g: An integer in the range [0, 255] that represent the rectangle's
			color's green component
		b: An integer in the range [0, 255] that represent the rectangle's
			color's blue component
		a: An integer in the range [0, 255] that represent the rectangle's
			color's alpha component
	"""

	dir_length = sqrt(dir_x ** 2 + dir_y ** 2)
	dir_x = dir_x / dir_length
	dir_y = dir_y / dir_length

	draw(4, GL_TRIANGLE_STRIP,
        #Vertices of a rectangle in which the right side is diriged by dir
        ('v2f', (x, y,
                 x + width * dir_y, y - width * dir_x,
                 x + height * dir_x, y + height * dir_y,
                 x + width * dir_y + height * dir_x,
                 y + height * dir_y - width * dir_x)),
        ('c4B', ((r, g, b, a) * 4)))

def drawTree(tree, x, y, height, width, r, g, b, a, angle=0):
    """Draw a tree recursively
        
    Args:
        tree: The Tree to be drawn
        x: A number indicating the x position of the tree's base's middle in
            the window
        y: A number indicating the y position of the tree's base's middle in
            the window's coordinate
        height: the height of the tree's trunk in window's coordinate
        width: the width of the tree's trunk in window's coordinate
        r: A integer in the range [0, 255] representing the red component of
            the tree's color
        g: A integer in the range [0, 255] representing the green component of
            the tree's color
        b: A integer in the range [0, 255] representing the blue component of
            the tree's color
        a: A integer in the range [0, 255] representing the alpha component of
            the tree's color
        angle: A float indicating the angle in radiant the trunk of the tree 
            make with the window's bottom side
    """

    if not glIsEnabled(GL_BLEND):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #Vector indicating the up direction of the tree
    dir_x = sin(angle)
    dir_y = cos(angle)

	#Center the Tree on the coordinate
    drawOrientedRectangle(x - width * dir_y / 2, y + width * dir_x / 2, 
    	dir_x, dir_y, width, height, r, g, b, a)

    for branch in tree.branches:
        drawTree(branch.tree, 
            x + dir_x * branch.height * height, y + dir_y * branch.height * height,
            height * branch.ratio, width * branch.ratio,
            r, g, b, a,
            angle + branch.angle)

def drawBranches(tree, length, x, y, height, width, r, g, b, a, angle=0):
    """Draw the branches that have their length less or equal to length
        
    Args:
        tree: The Tree to be drawn
        length: The maximum length of the branches that will be drawn
        x: A number indicating the x position of the tree's base's middle in
            the window
        y: A number indicating the y position of the tree's base's middle in
            the window's coordinate
        height: the height of the tree's trunk in window's coordinate
        width: the width of the tree's trunk in window's coordinate
        r: A integer in the range [0, 255] representing the red component of
            the tree's color
        g: A integer in the range [0, 255] representing the green component of
            the tree's color
        b: A integer in the range [0, 255] representing the blue component of
            the tree's color
        a: A integer in the range [0, 255] representing the alpha component of
            the tree's color
        angle: A float indicating the angle in radiant the trunk of the tree 
            make with the window's bottom side
    """
    if len(tree) != length:
        for branch in tree.branches:
            drawBranches(branch.tree, length,
                x + sin(angle) * branch.height * height,
                y + cos(angle) * branch.height * height,
                height * branch.ratio, width * branch.ratio,
                r, g, b, a,
                angle + branch.angle)
    else:
        drawTree(tree, x, y, height, width, r, g, b, a, angle)

def drawLastBranches(tree, x, y, height, width, r, g, b, a, angle=0):
    """Draw the last branches of the tree
        
    Args:
        tree: The Tree to be drawn
        x: A number indicating the x position of the tree's base's middle in
            the window
        y: A number indicating the y position of the tree's base's middle in
            the window's coordinate
        height: the height of the tree's trunk in window's coordinate
        width: the width of the tree's trunk in window's coordinate
        r: A integer in the range [0, 255] representing the red component of
            the tree's color
        g: A integer in the range [0, 255] representing the green component of
            the tree's color
        b: A integer in the range [0, 255] representing the blue component of
            the tree's color
        a: A integer in the range [0, 255] representing the alpha component of
            the tree's color
        angle: A float indicating the angle in radiant the trunk of the tree 
            make with the window's bottom side
    """
    drawBranches(tree, 1, x, y, height, width, r, g, b, a, angle)

def drawTreeMultiColor(tree, x, y, height, width, colors,
	default=(255, 255, 255, 255), angle=0):
	"""Draw a tree giving colors to the branch according to their length

	Args:
		tree: The Tree to be drawn
        length: The maximum length of the branches that will be drawn
        x: A number indicating the x position of the tree's base's middle in
            the window
        y: A number indicating the y position of the tree's base's middle in
            the window's coordinate
        height: the height of the tree's trunk in window's coordinate
        width: the width of the tree's trunk in window's coordinate
        colors: A SuccesiveInterval object that link some colors to interval of
        	color length.
        default: The color used when no interval are for found for a given
        	length
        angle: A float indicating the angle in radiant the trunk of the tree 
            make with the window's bottom side
	"""

    if not glIsEnabled(GL_BLEND):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    #Vector indicating the up direction of the tree
    dir_x = sin(angle)
    dir_y = cos(angle)

	#Center the Tree on the coordinate
    drawOrientedRectangle(x - width * dir_y / 2, y + width * dir_x / 2, 
    	dir_x, dir_y, width, height, *colors.get(len(tree), default))

    for branch in tree.branches:
        drawTreeMultiColor(branch.tree, 
            x + dir_x * branch.height * height, y + dir_y * branch.height * height,
            height * branch.ratio, width * branch.ratio,
            colors, default,
            angle + branch.angle)