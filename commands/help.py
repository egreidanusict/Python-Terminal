class HelpCommand:
    def __init__(self, terminal, *args, **kwargs):
        self.terminal = terminal
        self.description = "Show this help message"
        self.usage = "help"

    def execute(self, *args):
        print("\nAvailable commands:")
        for command in self.terminal.commands.values():
            desc = getattr(command, 'description', '')
            print(f"  {command.name}: {desc}")
        print()
