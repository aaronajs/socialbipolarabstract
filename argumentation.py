# represents an Argument (node) to be made in the Framework
class Argument():
    
    def __init__(self, name, positive = 0, negative = 0):
        self.name = name # currently behaves as id 
        # two way monitoring of relations - like doubly linkedlist
        self.attacks, self.attackedBy = [],[]
        self.supports, self.supportedBy = [],[]
        # should be floats
        self.score, self.strength = 0, 0
        # should be ints
        self.positiveVotes, self.negativeVotes = positive, negative
    
    def attack(self, other):
        # can't attack itself, or Argument it already supports
        if self is not other and other not in self.supports:
            self.attacks.append(other)
            other.attackedBy.append(self) # double linked
        else: print("unable to add attack from " + self.name + " to " + other.name)

    def support(self, other):
        # can't support itself, or Argument it already attacks
        if self is not other and other not in self.attacks:
            self.supports.append(other)
            other.supportedBy.append(self) # doubly linked
        else: print("unable to add support from " + self.name + " to " + other.name)

    def updateScore(self): 
        # calculates score, if no votes then score is 0
        self.score = float(self.positiveVotes)/(float(self.positiveVotes + self.negativeVotes)) if self.positiveVotes != 0 and self.negativeVotes != 0 else 0

    # override
    def __str__(self): return self.name

# represents a Social Bipolar Abstract Argumentation Framework (directed graph)
class Framework():
    
    def __init__(self):
        self.arguments = [] # to store all Arguments

    def addArgument(self, argument): 
        # can't add the same Argument again
        if argument not in self.arguments: 
            self.arguments.append(argument)

    # finds Argument in list based on its name(id)
    def locate(self, name): return next((argument for argument in self.arguments if argument.name == name), None)

    # updates score for each Argument in the Framework
    def calculateScores(self):
        for argument in self.arguments:
            argument.updateScore()