from graphviz import Digraph

class Sketch():
    
    def __init__(self, name, framework, show):
        print("Sketching debate")
        dot = Digraph(comment=name)
        for arg in framework.arguments:
            dot.node(arg.name, arg.name, shape='circle')
            for attack in arg.attacks:
                dot.edge(arg.name, attack.name, label="-", arrowhead="normal")
            for support in arg.supports:
                dot.edge(arg.name, support.name, label="+", arrowhead="onormal")
        dot.render("sketch/"+name, view=show)