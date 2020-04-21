from argumentation import Argument, Framework
from analysis import Analyser
from sketch import Sketch
import sys # used to read command line arguments and exit program if error
import pandas # used for data analysis of csv file

framework = Framework()
try: # reads text file
    filename = str(sys.argv[1]) # passed via command line argument
    with open("debates/"+filename+".txt","r") as debate:
        instruction = (debate.readline().strip(),1) # stores instruction and line number
        print("Reading "+filename+".txt")
        while instruction[0]:
            try: # separates instruction into command and attributes + formatting
                command = instruction[0][:3].lower()
                parameters = instruction[0][4:-1].lower().replace('\n','').split(',')
                # at most three values - if no votes for 'arg', 0 is used for each number of votes
                attributes = [parameters[i] if len(parameters) > i else 0 for i in range(3)]
                # performs actions based on command
                # adds new argument to framework, if no number of votes, 0 is used
                if command == 'arg': framework.addArgument(Argument(attributes[0],int(attributes[1]),int(attributes[2])))
                # locates the two arguments and adds an attack or support between them
                elif command == 'att': framework.locate(attributes[0]).attack(framework.locate(attributes[1]))
                elif command == 'sup': framework.locate(attributes[0]).support(framework.locate(attributes[1]))
                else: print("Ignoring: Line", instruction[1], "->", instruction[0])
            except: print("Syntax error: Line", instruction[1], "->", instruction[0]); sys.exit()
            # load next instruction from file
            instruction = (debate.readline().strip(),instruction[1]+1)
except: sys.exit("Unable to read file \""+filename+".txt\"")
try: # reads csv file - has same name as txt file
    # formats positive and negative votes from csv file
    data = pandas.read_csv("debates/"+filename+".csv",names=["positive","negative"])
    for vote in data.positive.dropna(): framework.locate(str(vote)).positiveVotes += 1
    for vote in data.negative.dropna(): framework.locate(str(vote)).negativeVotes += 1
except: print("No further votes to add")
try: # performs evaluation of framework
    Analyser(framework) # calculates score, strengths, extensions
    Sketch(filename, framework) # generates graph
except: sys.exit("Error performing analysis")