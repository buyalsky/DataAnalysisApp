import sys, os
sys.path.append(os.path.abspath(os.path.join("..")))
from node import Node


class TextOutput(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Text Output", inputs=1, outputs=0)
        self.is_last = True


class ScatterPlot(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Scatter Plot", inputs=1, outputs=0)
        self.is_last = True


class Histogram(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Histogram", inputs=1, outputs=0)
        self.is_last = True
