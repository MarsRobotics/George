class State():
    #init attributes of state
    def __init__(self, name, nextState):
        self.name = name
        self.nextState = nextState

    #each state must implement run()
    def run(self):
        print(self.name)
        print("\n>run() not implemented\n")
