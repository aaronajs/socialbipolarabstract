# represents an argument node to be made in the framework
class Argument():
    
    def __init__(self, name, score):
        self.name = name
        self.attacks, self.attackedBy = [],[]
        self.supports, self.supportedBy = [],[]
        self.score, self.strength = score, 0
    
    def attack(self, other):
        if self is not other and other not in self.supports:
            self.attacks.append(other)
            other.attackedBy.append(self)
        else: print("unable to add attack from " + self.name + " to " + other.name)

    def support(self, other):
        if self is not other and other not in self.attacks:
            self.supports.append(other)
            other.supportedBy.append(self)
        else: print("unable to add support from " + self.name + " to " + other.name)

    def setStrength(self, strength): self.strength = "{0:.2f}".format(strength)

    def __str__(self): 
        string = "\'" + self.name + "\' : " + str(self.score) + " -> " + str(self.strength) + ")  |"
        if self.attacks: string += " attacks: "
        for argument in self.attacks: string += argument.name + ", "
        if self.supports: string += " supports: "
        for argument in self.supports: string += argument.name + ", "
        return string[:-2]

# represents a Social Bipolar Abstract Argumentation Framework
class Framework():
    
    def __init__(self):
        self.arguments = []

    def addArgument(self, argument): 
        if argument not in self.arguments: 
            self.arguments.append(argument)

    def locate(self, name): return next((argument for argument in self.arguments if argument.name == name), None)

    def __str__(self): 
        state = "Debate Results: \n" 
        for a in self.arguments: state += a.__str__() + "\n"
        return state