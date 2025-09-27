from modules.colors import Colors

class Prompt:
    def __init__(self, terminal):
        self.terminal = terminal

    def prompt(self):
        prompt_parts = []

        client = self.terminal.terminalData.get('client', {})
        username = client.get('username')
        hostname = client.get('hostname')

        if username:
            prompt_parts.append(f"{Colors.BRIGHT_GREEN}{username}{Colors.RESET}")
        if hostname:
            prompt_parts[-1] += f"{Colors.BRIGHT_CYAN}@{hostname}{Colors.RESET}" if prompt_parts else f"{Colors.BRIGHT_CYAN}{hostname}{Colors.RESET}"

        session = self.terminal.terminalData.get('session', {})
        current_dir = session.get('current_directory')
        home_dir = client.get('home_directory')
        home_char = self.terminal.config.get('home_directory_char', '~')

        if current_dir:
            display_dir = current_dir
            if home_dir and current_dir.startswith(home_dir):
                display_dir = f"{home_char}{current_dir[len(home_dir):]}"
            prompt_parts.append(f"{Colors.BRIGHT_YELLOW}:{display_dir}{Colors.RESET}")

        prompt_parts.append(f" {Colors.BRIGHT_CYAN}$ {Colors.RESET}")

        return ''.join(prompt_parts)
