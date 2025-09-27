class Command:
    def __init__(self, name, func, description="No description provided"):
        self.name = name
        self.func = func
        self.description = description

    def execute(self, *args, **kwargs):
        return self.func(*args, **kwargs)