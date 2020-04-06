from argumentation import Argument, Framework
from scipy.optimize import fsolve, fmin
from numpy import array

class Model(): 

    def __init__(self):
        self.arguments = []

    def equationGenerator(self, values):
        equations = []
        for index in range(len(self.arguments)):
            argument = self.arguments[index]
            equations.append(values[index] - (argument.score * (1 - self.findByIndex(argument, "attack", values)) * (1 + self.findByIndex(argument, "support", values))))
        return equations

    def findByIndex(self, argument, relationType, values):
        if relationType == "attack": relationBy = argument.attackedBy
        else: relationBy = argument.supportedBy 
        relationsCount = len(relationBy)
        if relationsCount == 0: return 0
        elif relationsCount == 1: return values[self.arguments.index(relationBy[0])]
        else: return self.collectRelations(values, relationBy, relationsCount, 1, values[self.arguments.index(relationBy[0])])

    def collectRelations(self, values, relationBy, relationsCount, current, collection):
        for current in range(1, relationsCount):
            collection = collection + values[self.arguments.index(relationBy[current])] - (collection * values[self.arguments.index(relationBy[current])])
        return collection
        
    def initialEstimate(self, values): return abs(sum(array(self.equationGenerator(values))**2)-0)

    def calculateStrengths(self, framework):
        print("calculating strengths")
        self.arguments = framework.arguments
        strengths = fsolve(self.equationGenerator,tuple(fmin(self.initialEstimate,tuple(argument.score for argument in self.arguments),disp=False)))
        for index in range(len(strengths)):
            self.arguments[index].setStrength(strengths[index])

class Analyser():

    def __init__(self, framework):
        self.extension = []
        self.sortedArguments = sorted(framework.arguments, key=lambda argument: argument.strength, reverse=True)

    def isConflictFree(self, argument):
        for extensionArgument in self.extension:
            if argument in extensionArgument.attacks or argument in extensionArgument.attackedBy: return False
        return True

    def isDefended(self, argument):
        attackers = argument.attackedBy
        for attacker in attackers:
            if argument in attacker.attackedBy:
                try:
                    attackers.remove(attacker)
                except: pass
            for extensionArgument in self.extension:
                if extensionArgument in attacker.attackedBy: 
                    try:
                        attackers.remove(attacker)
                    except: pass
        if len(attackers) == 0: return True
        return False

    def isAdmissible(self, argument):
        return self.isConflictFree(argument) and self.isDefended(argument)

    def generateExtension(self):
        print("evaluating")
        self.extension = [self.sortedArguments[0]]
        for argument in self.sortedArguments[1:]:
            if self.isAdmissible(argument): self.extension.append(argument)
        return self.extension