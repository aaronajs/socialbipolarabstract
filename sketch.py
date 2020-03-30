from graphviz import Digraph
class BasicSketch():
    
    def draw(self, name, framework, show):
        try:
            dot = Digraph(comment=name)
            for arg in framework.arguments:
                dot.node(arg.name, arg.name + " : " + str(arg.strength))
                for attack in arg.attacks:
                    dot.edge(arg.name, attack.name, label="-", arrowhead="normal") #use 'vee'
                for support in arg.supports:
                    dot.edge(arg.name, support.name, label="+", arrowhead="onormal")
            dot.render("basicsketch/"+name, view=show)
        except:
            print("Error generating sketch.")