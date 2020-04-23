class CodeContainer:
    def __init__(self, filename):
        file = open(filename, 'r')
        code = file.read().strip()
        self.code = code
    

    def run(self):
        exec(self.code)