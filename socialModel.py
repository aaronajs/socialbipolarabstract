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
            equations.append(values[index] - (self.args[index].score * (1 - self.findAttackedByIndex(self.args[index], values))))
        return equations

    def findAttackedByIndex(self, arg, values):
        noAttackers = len(arg.attackedBy)
        if noAttackers == 0: return 0
        elif noAttackers == 1: return values[self.args.index(arg.attackedBy[0])]
        else: return self.collectAttackers(arg, values, noAttackers, 1, values[self.args.index(arg.attackedBy[0])])

    def collectAttackers(self, arg, values, noAttackers, current, collection):
        for curr in range(1, noAttackers):
            collection = collection + values[self.args.index(arg.attackedBy[curr])] - (collection * values[self.args.index(arg.attackedBy[curr])])
        return collection
        
    def initialEstimate(self, values): return abs(sum(array(self.equationGenerator(values))**2)-0)

    def calculateStrengths(self, args):
        self.args = args
        strengths = fsolve(self.equationGenerator, tuple(fmin(self.initialEstimate,tuple(arg.score for arg in self.args),disp=False)))
        for index in range(len(strengths)):
            self.args[index].setStrength(strengths[index])