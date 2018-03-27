from states.State import State

class ManualMoveState(State):
    #init attributes of state
    def __init__(self):
        super().__init__("ManualMoveState", "ManualMoveState")

    #implementation for each state: overridden
    def run(self, moveInstructions):
        print("\n>run() not implemented\n")
