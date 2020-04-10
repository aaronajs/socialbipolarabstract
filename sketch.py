from graphviz import Digraph # used to generate graphs

 # could be converted to a script or add more methods for different graph types
class Sketch():
    def __init__(self, name, framework): # obtains file title and arguments
        print("Sketching debate")
        dot = Digraph(comment=name)
        for argument in framework.arguments: 
            # each argument is represented as a circle
            dot.node(argument.name, argument.name, shape='circle')
            for attack in argument.attacks:
                # each attack is represented as a filled in arrow 
                dot.edge(argument.name, attack.name, arrowhead="normal")
            for support in argument.supports:
                # each support is represented as an empty arrow 
                dot.edge(argument.name, support.name, arrowhead="onormal")
        # saves the dot file, the pdf file of the graph and opens it.
        dot.render("sketch/"+name, view=True)