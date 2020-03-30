from argumentation import Argument, Framework
from socialModel import Model
from sketch import BasicSketch
import sys

model = Model()
framework = Framework()
sketch = BasicSketch()
try:
    filename = str(sys.argv[1])
    debate = open("debates/"+filename+".txt","r")
    instruction = debate.readline().strip()
    lineNo = 1
    while instruction:
        try:
            command = instruction[:3].lower()
            params = instruction[4:].lower().replace(')','').split(',')
        except:
            print("Parse error: Line", lineNo, "->", instruction)
            debate.close()
            sys.exit()
        try:
            if command == 'arg': framework.addArg(Argument(params[0],float(params[1])))
            elif command == 'att': framework.addAttack(framework.locate(params[0]),framework.locate(params[1]))
            elif command == 'sup': framework.addSupport(framework.locate(params[0]),framework.locate(params[1]))
            elif command == 'ske': sketch.draw(filename+"/at_line_"+str(lineNo), framework, False)
            elif command == 'res': framework.reset()
            elif command == 'pos': framework.locate(params[0]).addPos()
            elif command == 'neg': framework.locate(params[0]).addNeg()
            elif command == 'cal': model.calculateStrengths(framework.arguments)
            else: print("Ignoring: Line", lineNo, "->", instruction)
            # switcher={
            #     'exit': self.bye,
            #     'reset': self.frame.reset,
            #     'example': self.runExample,
            #     'help': self.help,
            #     'show': self.show
            # }
            # func = switcher.get(command,0)
            # if func == 0: print("Invalid command.")
            # else: func()
        except:
            print("Syntax error: Line", lineNo, "->", instruction)
            debate.close()
            sys.exit()
        instruction = debate.readline().strip()
        lineNo += 1
    debate.close()
except:
    print("File not found")
    sys.exit()
try:
    model.calculateStrengths(framework.arguments)
    sketch.draw(filename+"/_completed", framework, True)
    print(framework)
except:
    print("Error calculating strengths.")