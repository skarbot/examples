class ProductionClass():
    def __init__(self, param):
        self.param = param

    def process(self):
        # Some processing logic
        return self.param

    def run(self):
        return self.process(self.param)


class ProductionClass2():
    def __init__(self, param):
        self.param = param

    def process(self):
        # Some processing logic
        return self.param

    def run(self):
        return self.process(self.param)