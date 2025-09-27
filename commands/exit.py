class ExitCommand:
    def __init__(self, app, *args, **kwargs):
        self.app = app
        self.description = "Exit the terminal"
        self.usage = "exit"

    def execute(self, *args):
        self.app.stop(0)
