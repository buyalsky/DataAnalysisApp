import sys, os
sys.path.append(os.path.abspath(os.path.join("..")))
from node import Node


class CsvLoader(Node):
    def __init__(self, scene):
        super().__init__(scene, title="Csv Loader", inputs=0, outputs=1)


if __name__ == '__main__':
    print(Node(None))