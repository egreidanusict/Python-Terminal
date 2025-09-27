from modules.clear import clear as clearScreen

class ClearCommand:
    def __init__(self, terminal, *args, **kwargs):
        self.terminal = terminal
        self.description = "Clear the terminal screen"
        self.usage = "clear"

    def execute(self, *args):
        clearScreen()