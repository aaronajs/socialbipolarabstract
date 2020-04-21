import random, subprocess # random selection / number generation; run processes in command line
argumentSizes = [10, 20, 30, 50, 75, 100, 125, 150, 175, 200]
for numberOfArguments in argumentSizes:
    print("\nTest: "+str(numberOfArguments) + " arguments:")
    for round in range(5): # test each argument size 5 times.
        # generate argument names e.g. A0, A1, A2, ...
        argumentNames = ["A"+str(argument) for argument in range(numberOfArguments)]
        # generate relations between randomly selected arguments; random chance of attack/support
        relations = [random.choice(["att(","sup("])+random.choice(argumentNames)+","+random.choice(argumentNames)+")" for relation in range(numberOfArguments)]
        # generate random votes for arguments
        arguments = ["arg("+argument+","+str(random.randint(0,numberOfArguments))+","+str(random.randint(0,numberOfArguments))+")" for argument in argumentNames]
        # create text file; write arguments, then relations
        with open("debates/d"+str(numberOfArguments)+".txt","w") as debate:
            for line in arguments + relations: debate.write(line+"\n")
        # run control script with text file in command line interface
        subprocess.call(str.split("time python control.py d"+str(numberOfArguments)))