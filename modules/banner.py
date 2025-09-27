class Banner:
    def __init__(self, name="App", version="1.0", author="Author", description="A simple terminal application"):
        self.name = name
        self.version = version
        self.author = author
        self.description = description

    def display(self):
        print(f"{self.name} v{self.version} by {self.author}\n{self.description}\n")