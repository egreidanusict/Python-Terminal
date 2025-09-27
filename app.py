from modules.clear import clear as clearScreen
from modules.command import Command
from modules.prompt import Prompt
from modules.banner import Banner
from os import listdir, system, getlogin, environ, path
from socket import gethostname
from importlib import import_module

class Terminal:
    def __init__(self):
        self.running = True
        self.stopped = False
        
        self.commands = {}

        self.config = {
            'name': 'Python Terminal',
            'version': '1.0.0',
            'author': 'Eelco Greidanus',
            'license': 'MIT',
            'description': 'A simple terminal application built with Python.',
            'home_directory_char': '~'
        }

        self.terminalData = {
            'client': {
                'username': None,
                'hostname': None,
                'home_directory': None
            },

            'session': {
                'current_directory': None,
                'previous_directory': None,
                'command_history': []
            }
        }

    
    def loadCommands(self):
        commands_folder = 'commands'

        for file in listdir(commands_folder):
            if file.endswith('.py') and not file.startswith('__'):
                module_name = f"{commands_folder}.{file[:-3]}"
                module = import_module(module_name)

                class_name = ''.join(word.capitalize() for word in file[:-3].split('_')) + 'Command'
                if hasattr(module, class_name):
                    command_class = getattr(module, class_name)

                    try:
                        instance = command_class(self)
                    except TypeError:
                        instance = command_class(self.commands)

                    command_name = file[:-3]
                    self.commands[command_name] = Command(
                        command_name,
                        instance.execute,
                        getattr(instance, 'description', '')
                    )
    
    def syncClientData(self):
        if 'client' not in self.terminalData:
            self.terminalData['client'] = {}

        self.terminalData['client']['username'] = getlogin() if hasattr(__import__('os'), 'getlogin') else environ.get('USER', 'unknown')
        self.terminalData['client']['hostname'] = gethostname()

        if not self.terminalData['client'].get('home_directory'):
            home_dir = environ.get('HOME') or environ.get('USERPROFILE') or path.expanduser('~')
            self.terminalData['client']['home_directory'] = home_dir

            if 'session' not in self.terminalData:
                self.terminalData['session'] = {}
            if not self.terminalData['session'].get('current_directory'):
                self.terminalData['session']['current_directory'] = home_dir
                self.terminalData['session']['previous_directory'] = None

    def run(self):
        try:
            self.loadCommands()
            self.syncClientData()
            clearScreen()
            Banner(
                name=self.config["name"], 
                version=self.config["version"], 
                author=self.config["author"], 
                description=self.config["description"]
            ).display()

            while self.running:
                self.loop()

            self.stop(0)
        except KeyboardInterrupt:
            self.stop(1)
    
    def loop(self):
        self.syncClientData()

        line = input(Prompt(self).prompt()).strip()
        if not line:
            return

        self.terminalData['session']['command_history'].append(line)

        parts = line.split()
        command_name = parts[0]
        args = parts[1:]

        if command_name in self.commands:
            self.commands[command_name].execute(*args)
        else:
            print(f"Unknown command: {command_name}")

    def stop(self, code=0):
        if self.running:
            self.running = False
        
        if self.stopped:
            return
        self.stopped = True

        print(f"\n{self.config['name']} exited with code {code}")

if __name__ == "__main__":
    terminal = Terminal()
    terminal.run()