def findAttackedByIndex(self, arg, p): # format with multiple attackers.
        noAttackers = len(arg.attackedBy)
        if noAttackers == 0: return 0
        elif noAttackers == 1: 
            return p[args.index(arg.attackedBy[0])]
        elif noAttackers == 2: 
            # return (p[args.index(arg.attackedBy[0])]+p[args.index(arg.attackedBy[1])]-(p[args.index(arg.attackedBy[0])]*p[args.index(arg.attackedBy[1])]))
            return self.collectAttackers(arg, p, noAttackers, 1, p[args.index(arg.attackedBy[0])])
        else: 
            # x = p[args.index(arg.attackedBy[0])]+p[args.index(arg.attackedBy[1])]-(p[args.index(arg.attackedBy[0])]*p[args.index(arg.attackedBy[1])])
            # return (x + p[args.index(arg.attackedBy[2])] - (x * p[args.index(arg.attackedBy[2])] ))
            return self.collectAttackers(arg, p, noAttackers, 1, p[args.index(arg.attackedBy[0])])

    def collectAttackers(self, arg, p, noAttackers, current, collection):
        for curr in range(1, noAttackers):
            collection = collection + p[args.index(arg.attackedBy[curr])] - (collection * p[args.index(arg.attackedBy[curr])])
        return collection

def equations(self, p):
        x1 = p[0] - (0.5*(1-p[1]))
        x2 = p[1] - (0.5*(1-(p[0]+p[2]-(p[0]*p[2]))))
        x3 = p[2] - (0.86*(1-(p[3]+p[4]-(p[3]*p[4]))))
        x4 = p[3] - (0.2*(1-p[4]))
        x5 = p[4] - (0.8*(1-p[3]))