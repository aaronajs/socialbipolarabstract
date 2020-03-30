# contains code to control program flow via terminal based commands.
from argumentation import Argument, Framework
from socialModel import Model

class Controller():

    def __init__(self):
        self.analyser = Model()
        self.frame = Framework()
        self.awaitCommand()

    def awaitCommand(self):
        command = ''
        while command != 'exit':
            command = input().lower()
            self.commandList(command)

    def commandList(self, command):
        switcher={
            'exit': self.bye,
            'reset': self.frame.reset,
            'example': self.runExample,
            'help': self.help,
            'show': self.show
        }
        func = switcher.get(command,0)
        if func == 0: print("Invalid command.")
        else: func()

    def bye(self): print("Goodbye.")
    def show(self): print("Placeholder to make graph.")

    def help(self):
        print("Manual:")
        print("Available commands:")
        print("help, example, reset, show, exit")

    def runExample(self):
        self.frame.reset()
        a,b,c,d,e,f = Argument("a",0.5),Argument("b",0.5),Argument("c",0.86),Argument("d",0.2),Argument("e",0.8),Argument("f",0.6)
        self.frame.addArgs([a,b,c,d,e,f])
        self.frame.addAttacks([(a,b),(b,a),(c,b),(d,c),(d,e),(e,c),(e,d),(f,c),(c,f)])
        for arg in self.frame.arguments: print(arg)
        self.analyser.calculateStrengths(self.frame.arguments)
        for arg in self.frame.arguments: print(arg)
        self.frame.reset()

if __name__ == '__main__': Controller()