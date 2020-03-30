# test to solve non linear set of equations
from argumentation import Argument, Framework
from scipy.optimize import fsolve, fmin
from scipy import stats
from numpy import array

class Model(): 

    def __init__(self):
        self.args = []

    # simplify
    def equationGenerator(self, values):
        equations = []
        for index in range(len(self.args)):
            arg = self.args[index]
            equations.append(values[index] - (arg.score * (1 - self.findByIndex(arg, "attack", values)) * (1 + self.findByIndex(arg, "support", values))))
        return equations

    def findByIndex(self, arg, relationType, values):
        if relationType == "attack": relationBy = arg.attackedBy
        else: relationBy = arg.supportedBy 
        noRelations = len(relationBy)
        if noRelations == 0: return 0
        elif noRelations == 1: return values[self.args.index(relationBy[0])]
        else: return self.collectRelations(arg, values, relationBy, noRelations, 1, values[self.args.index(relationBy[0])])

    def collectRelations(self, arg, values, relationBy, noRelations, current, collection):
        for curr in range(1, noRelations):
            collection = collection + values[self.args.index(relationBy[curr])] - (collection * values[self.args.index(relationBy[curr])])
        return collection
        
    def initialEstimate(self, values): return abs(sum(array(self.equationGenerator(values))**2)-0)

    def calculateStrengths(self, args):
        self.args = args
        strengths = fsolve(self.equationGenerator, tuple(fmin(self.initialEstimate,tuple(arg.score for arg in self.args),disp=False)))
        for index in range(len(strengths)):
            self.args[index].setStrength(strengths[index])