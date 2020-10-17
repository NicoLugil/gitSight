
class xy:
    """ 
    A class that bundles x, y and label
    """

    def __init__(self, label='no-label', x=None, y=None):
        self.label=label
        self.x = x if x is not None else []
        self.y = y if y is not None else []

