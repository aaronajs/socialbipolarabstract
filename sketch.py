from graphviz import Digraph

class Sketch():
    
    def draw(self, name, framework, show):
        print("sketching")
        dot = Digraph(comment=name)
        for arg in framework.arguments:
            dot.node(arg.name, arg.name, shape='circle')
            for attack in arg.attacks:
                dot.edge(arg.name, attack.name, label="-", arrowhead="normal")
            for support in arg.supports:
                dot.edge(arg.name, support.name, label="+", arrowhead="onormal")
        dot.render("sketch/"+name, view=show)

    # def draw(self, name, framework, show):
    #     try:
    #         dot = Digraph(comment=name, format='svg')
    #         for arg in framework.arguments:
    #             dot.node(arg.name, arg.name.upper(), fontsize="22", shape="circle")
    #             for attack in arg.attacks:
    #                 dot.edge(arg.name, attack.name, arrowhead="normal", constraint="true")
    #             for support in arg.supports:
    #                 dot.edge(arg.name, support.name, arrowhead="onormal", constraint="true")
    #         dot.render("sketch/sbaeval", view=False)
    #     except:
    #         print("Error generating sketch.")