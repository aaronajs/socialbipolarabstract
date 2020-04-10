from argumentation import Argument, Framework
from scipy.optimize import fsolve, fmin # used to generate and solve non-linear equations
from numpy import array # used for formatting

class Model(): 

    def __init__(self, framework):
        self.arguments = framework.arguments
        self.calculateStrengths() 

    def equationGenerator(self, values): # values contains current solution (strength) for each Argument
        equations = []
        # generates a non-linear equation for each Argument
        for index in range(len(self.arguments)):
            argument = self.arguments[index]
            # in the social model format - see report for equation
            equations.append(values[index] - (argument.score * (1 - self.findByIndex(argument, "attack", values)) * (1 + self.findByIndex(argument, "support", values))))
        return equations

    # find all relations towards a particular Argument
    def findByIndex(self, argument, relationType, values):
        # identifies if checking attack or support
        relationBy = argument.attackedBy if relationType == "attack" else argument.supportedBy
        relationsCount = len(relationBy) # counts number of relations on argument
        if relationsCount == 0: return 0 # if no relations, no further affect
        # else use product notation of social modal to finish off equation
        else: return self.collectRelations(values, relationBy, relationsCount, 1, values[self.arguments.index(relationBy[0])])

    # iterates through each relation (of the same type) on an Argument to get strength (current interation)
    def collectRelations(self, values, relationBy, relationsCount, current, collection):
        for current in range(1, relationsCount):
            collection = collection + values[self.arguments.index(relationBy[current])] - (collection * values[self.arguments.index(relationBy[current])])
        return collection
        
    # uses estimation theory to generate initial guess for the iteration algorithm
    def initialEstimate(self, values): return abs(sum(array(self.equationGenerator(values))**2)-0)

    # gets initial estimate and uses iterative process to get strengths for each Argument.
    def calculateStrengths(self):
        print("Calculating strengths")
        # uses scores to get initial estimate
        # uses initial estimate as first iteration values of strengths
        # updates each iteration until convergence (ideally)
        # change 'disp' to 'True' to print iteration details and stats
        strengths = fsolve(self.equationGenerator,tuple(fmin(self.initialEstimate,tuple(argument.score for argument in self.arguments),disp=False)))
        # updates strength for each Argument
        for index in range(len(strengths)):
            self.arguments[index].strength = strengths[index]

class Analyser():

    def __init__(self, framework):
        self.extension = []
        framework.calculateScores() # update all scores
        Model(framework) # calculate strengths
        self.generateExtension(framework) # get extension

    # checks if Argument attacks or is attacked by one of the Arguments already in the extension
    def isConflictFree(self, argument):
        for extensionArgument in self.extension:
            if argument in extensionArgument.attacks or argument in extensionArgument.attackedBy: return False
        return True

    # checks if the Argument (A) or the Arguments in the extension attack all Arguments that attack the Argument (A)
    def isDefended(self, argument):
        attackers = argument.attackedBy 
        for attacker in attackers: # iterates through all attackers
            if argument in attacker.attackedBy: # checks if Argument attacks attacker
                try: # can't remove same attacker
                    attackers.remove(attacker)
                except: pass
            # checks if Arguments in extension attack attacker
            for extensionArgument in self.extension: 
                if extensionArgument in attacker.attackedBy: 
                    try:
                        attackers.remove(attacker)
                    except: pass
        if len(attackers) == 0: return True # if all attackers are attacked in some way
        return False # else not defended

    def isAdmissible(self, argument): # only if conflict free and defended
        return self.isConflictFree(argument) and self.isDefended(argument)

    def generateExtension(self, framework):
        print("Evaluating extension") # sorts arguments in order of strength (strongest -> weakest)
        sortedArguments = sorted(framework.arguments, key=lambda argument: argument.strength, reverse=True)
        self.extension = [sortedArguments[0]] # strongest argument has to be in extension
        for argument in sortedArguments[1:]: # checks if remaining arguments are admissible
            if self.isAdmissible(argument): self.extension.append(argument) # added if admissible
        print("Strongest complete extension: {"), # print extension in terminal
        for argument in self.extension:
            print(argument),
        print("}")