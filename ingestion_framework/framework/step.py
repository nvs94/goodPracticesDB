class Step:
    """
    Base class for pipeline steps.
    """

    def __init__(self, name, logger=None):
        self.name = name
        self.logger = logger

    def run(self, data):
        raise NotImplementedError("Step must implement run()")
