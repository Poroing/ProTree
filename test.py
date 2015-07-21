from protree.tree import Tree, TreeBuilder
from protree.treeDrawer import drawTree, drawLastBranches, drawTreeMultiColor
from protree.sinter import SuccesiveInterval
from pyglet.window import Window, key
from pyglet.gl import Config, glClearColor
from pyglet import app

t = Tree()
tb = TreeBuilder()
colors = SuccesiveInterval([(8, (64, 0, 0, 255)), (5, (240, 40, 170, 64))])

config = Config(alpha_size=8)
w = Window(config=config)

glClearColor(0.2, 0.2, 1.0, 0.5)

@w.event
def on_key_press(symbols, modifier):
    global t
    global tb

    if symbols is key.R:
        t = Tree()
        w.clear()
        drawTree(t, 300, 0, 200, 20, 255, 255, 255, 16)
    if symbols is key.N:
        tb.addBranchesToEnd(t)
        drawLastBranches(t, 300, 0, 200, 20, 255, 255, 255, 16)
        print('Done Drawing')
    if symbols is key.D:
        w.clear()
        drawTreeMultiColor(t, 300, 0, 200, 20, colors)

app.run()
