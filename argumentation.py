# represents an argument node to be made in the framework
class Argument():
    
    idCounter = 0

    def __init__(self, name, score = 0):
        self.id = Argument.idCounter
        self.name = name
        self.attacks, self.attackedBy = [],[]
        self.supports, self.supportedBy = [],[]
        self.score, self.strength = score,0
        self.pos, self.neg = 0,0
        Argument.idCounter += 1
    
    def attack(self, other):
        if self is not other:
            self.attacks.append(other)
            other.attackedBy.append(self)
        else: print("error")

    def support(self, other):
        if self is not other:
            self.supports.append(other)
            other.supportedBy.append(self)
        else: print("error")

    # would be linked to a user, but simplified for the purposed of implementation.
    def setPos(self, pos): self.pos = pos
    def setNeg(self, neg): self.neg = neg
    def addPos(self): self.pos += 1
    def addNeg(self): self.neg += 1
    def removePos(self): self.pos -= 1
    def removeNeg(self): self.neg -= 1 

    # score of the argument: ratio of positive to negative votes.
    def calculateScore(self):
        if self.pos == 0 and self.neg == 0: self.score = 0
        else: self.score = self.pos / float(self.pos + self.neg)

    def setStrength(self, strength): self.strength = "{0:.2f}".format(strength)

    def __str__(self): 
        string = "(" + str(self.id) + ": " + self.name + ", " + str(self.score) + ", " + str(self.strength) + ")  "
        if self.attacks: string += "| attacks: "
        for arg in self.attacks: string += "(" + str(arg.id) + ": " + arg.name + ")" + ", "
        if self.attackedBy: string += "| attacked by: "
        for arg in self.attackedBy: string += "(" + str(arg.id) + ": " + arg.name + ")" + ", "
        return string[:-2]

# represents a Social Bipolar Abstract Argumentation Framework
class Framework():
    
    def __init__(self):
        self.arguments = []

    def addArg(self, arg): 
        if arg not in self.arguments: 
            self.arguments.append(arg)

    def addArgs(self, args): 
        for arg in args: self.addArg(arg)

    def addAttack(self, first, second): first.attack(second)
    def addSupport(self, first, second): first.support(second)

    def addAttacks(self, attacks):
        for args in attacks:
            self.addAttack(args[0], args[1])

    def addSupports(self, supports):
        for args in supports:
            self.addSupport(args[0], args[1])

    def reset(self): self.arguments = []

    def locate(self, name): return next((arg for arg in self.arguments if arg.name == name), None)

    def __str__(self): 
        state = "Debate Results: \n" 
        for a in self.arguments: state += a.__str__() + "\n"
        return state