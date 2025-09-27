from os import chdir, path, getcwd, environ

class CdCommand:
    def __init__(self, terminal):
        self.terminal = terminal
        self.description = "Change the current directory"
        self.usage = "cd [directory]"

    def execute(self, *args):
        if not args:
            current = self.terminal.terminalData['session'].get('current_directory')
            print(f"Current directory: {current}")
            return

        target_directory = args[0]

        home_dir = self.terminal.terminalData['client'].get('home_directory') or environ.get('HOME') or path.expanduser('~')
        if target_directory.startswith('~'):
            target_directory = path.join(home_dir, target_directory[2:] if target_directory.startswith('~/') else target_directory[1:])

        if not path.isabs(target_directory):
            current = self.terminal.terminalData['session']['current_directory'] or getcwd()
            target_directory = path.join(current, target_directory)

        if not path.exists(target_directory):
            print(f"Directory not found: {target_directory}")
            return

        try:
            previous_dir = self.terminal.terminalData['session']['current_directory'] or getcwd()
            chdir(target_directory)
            self.terminal.terminalData['session']['previous_directory'] = previous_dir
            self.terminal.terminalData['session']['current_directory'] = getcwd()
        except PermissionError:
            print(f"Permission denied: {target_directory}")
        except Exception as e:
            print(f"Error changing directory: {e}")