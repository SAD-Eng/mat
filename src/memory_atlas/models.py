

class MemoryAtlas:
    def __init__(self):
        self.boms = []  # list of BinaryObjectModel


class BinaryObjectModel:
    def __init__(self, name):
        self.name = name
        self.variables = []  # list of BomVariable


class BomVariable:
    def __init__(self, name, version_major, version_minor):
        self.name = name
        self.description = ''
        self.version_major = version_major
        self.version_minor = version_minor
        self.version_patch = 0

