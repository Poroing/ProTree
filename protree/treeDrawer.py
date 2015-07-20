from pyglet.graphics import draw
from pyglet.gl import (GL_TRIANGLE_STRIP, GL_BLEND, glEnable, glBlendFunc, 
    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA, glIsEnabled)
from math import cos, sin

"""Module that store function to draw Tree object using pyglet

To use this module pyglet must be installed
"""

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

    draw(4, GL_TRIANGLE_STRIP,
        #Vertices of a rectangle in which the right side is diriged by dir
        ('v2f', (x - width * dir_y / 2, y + width * dir_x / 2,
                 x + width * dir_y / 2, y - width * dir_x / 2,
                 x - width * dir_y / 2 + height * dir_x,
                    y + height * dir_y + width * dir_x / 2,
                 x + width * dir_y / 2 + height * dir_x,
                    y + height * dir_y - width * dir_x / 2)),
        ('c4B', ((r, g, b, a) * 4)))

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
