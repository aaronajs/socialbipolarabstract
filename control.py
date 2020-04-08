from argumentation import Argument, Framework
from analysis import Analyser
from sketch import Sketch
import sys
import pandas
framework = Framework()
try:
    filename = str(sys.argv[1])
    with open("debates/"+filename+".txt","r") as debate:
        instruction = (debate.readline().strip(), 1)
        print("Reading "+filename+".txt")
        while instruction[0]:
            try:
                command, parameters = instruction[0][:3].lower(), instruction[0][4:-1].lower().replace('\n','').split(',')
                attributes = [parameters[i] if len(parameters) > i else 0 for i in range(3)]
            except: sys.exit("Parse error: Line", instruction[1], "->", instruction[0])
            try:
                if command == 'arg': framework.addArgument(Argument(attributes[0],float(attributes[1]),float(attributes[2])))
                elif command == 'att': framework.locate(attributes[0]).attack(framework.locate(attributes[1]))
                elif command == 'sup': framework.locate(attributes[0]).support(framework.locate(attributes[1]))
                else: print("Ignoring: Line", instruction[1], "->", instruction[0])
            except: sys.exit("Syntax error: Line", instruction[1], "->", instruction[0])
            instruction = (debate.readline().strip(), instruction[1]+1)
except: sys.exit("Unable to read file \"" + filename + ".txt\"")
try:
    data = pandas.read_csv("debates/"+filename+".csv",names=["positive","negative"])
    for vote in data.positive.dropna(): framework.locate(str(vote)).positiveVotes += 1
    for vote in data.negative.dropna(): framework.locate(str(vote)).negativeVotes += 1
except: print("No further votes to add")
try:
    Analyser(framework)
    Sketch(filename, framework, True)
except: sys.exit("Error performing analysis")