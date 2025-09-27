# commands/ls.py
from os import listdir, path
from modules.colors import Colors

class LsCommand:
    def __init__(self, terminal):
        self.terminal = terminal
        self.description = "List directories first, then files, in a colored grid"
        self.usage = "ls"

    def execute(self, *args):
        current_dir = self.terminal.terminalData['session'].get('current_directory')
        if not current_dir:
            print("Current directory not set.")
            return

        try:
            entries = sorted(listdir(current_dir))
            if not entries:
                print("Directory is empty.")
                return

            dirs = [f"{Colors.GREEN}{e}/{Colors.RESET}" for e in entries if path.isdir(path.join(current_dir, e))]
            files = [f"{Colors.BRIGHT_BLUE}{e}{Colors.RESET}" for e in entries if not path.isdir(path.join(current_dir, e))]
            formatted = dirs + files

            def visible_length(s):
                import re
                return len(re.sub(r'\033\[[0-9;]*m', '', s))

            col_width = max(visible_length(f) for f in formatted) + 2
            cols = 4

            for i in range(0, len(formatted), cols):
                row = formatted[i:i+cols]
                print("".join(f"{f:<{col_width}}" for f in row))

        except Exception as e:
            print(f"Error reading directory: {e}")
