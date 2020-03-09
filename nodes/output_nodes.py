import sys, os
sys.path.append(os.path.abspath(os.path.join("..")))
from node import Node


class TextOutput(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Csv Loader", inputs=1, outputs=0)
        self.is_last = True


class ScatterPlot(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Csv Loader", inputs=1, outputs=0)
        self.is_last = True


class Histogram(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Csv Loader", inputs=1, outputs=0)
        self.is_last = True
