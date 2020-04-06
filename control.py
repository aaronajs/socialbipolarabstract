from argumentation import Argument, Framework
from analysis import Model, Analyser
from sketch import Sketch
import sys

model = Model()
framework = Framework()
sketch = Sketch()
try:
    filename = str(sys.argv[1])
    debate = open("debates/"+filename+".txt","r")
    instruction = debate.readline().strip()
    lineNo = 1
    print("reading file")
    while instruction:
        try:
            command = instruction[:3].lower()
            params = instruction[4:].lower().replace(')','').replace('\n','').split(',')
        except:
            print("Parse error: Line", lineNo, "->", instruction)
            debate.close()
            sys.exit()
        try:
            if command == 'arg': framework.addArgument(Argument(params[0],float(params[1])))
            elif command == 'att': framework.locate(params[0]).attack(framework.locate(params[1]))
            elif command == 'sup': framework.locate(params[0]).support(framework.locate(params[1]))
            elif command == 'ske': sketch.draw(filename+"/at_line_"+str(lineNo), framework, False)
            elif command == 'sco': framework.locate(params[0]).score = params[1]
            elif command == 'cal': model.calculateStrengths(framework)
            else: print("Ignoring: Line", lineNo, "->", instruction)
        except:
            print("Syntax error: Line", lineNo, "->", instruction)
            debate.close()
            sys.exit()
        instruction = debate.readline().strip()
        lineNo += 1
    debate.close()
    print("end of file")
except:
    print("File not found")
    sys.exit()
try:
    model.calculateStrengths(framework)
    sketch.draw(filename+"/_completed", framework, True)
    print("Strongest Admissible Extension:", [arg.name for arg in Analyser(framework).generateExtension()])
except:
    print("Error calculating strengths.")