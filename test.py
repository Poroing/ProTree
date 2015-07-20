from protree.tree import Tree, TreeBuilder
from protree.treeDrawer import drawTree, drawLastBranches
from pyglet.window import Window, key
from pyglet.gl import Config
from pyglet import app

t = Tree()
tb = TreeBuilder()

config = Config(alpha_size=8)
w = Window(config=config)

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
    if symbols is key.D:
        w.clear()
        drawTree(t, 300, 0, 200, 20, 255, 255, 255, 16)

app.run()
