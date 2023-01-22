"""
Serialization/deserialization support for saving to and loading from a
.mat.json file. This is the "native" file format for a MemoryAtlas object
graph.
"""
import jsonpickle


class MatJsonFile:
    def __init__(self, path, atlas=None):
        """
        Creates a new object to manage the state of a .mat.json file
        :param path: The path to save/open from
        :param atlas: The MemoryAtlas object to save to, or None for opening
        """
        self.path = path
        self.atlas = atlas

    def serialize(self):
        """Returns a JSON string for the current MemoryAtlas object"""
        return jsonpickle.encode(self.atlas, indent=4)

    def save(self):
        print(f'Saving MAT JSON to {self.path}')
        with open(self.path, 'w', newline='\n') as f:
            f.write(self.serialize())

    def deserialize(self, json):
        self.atlas = jsonpickle.decode(json)

    def load(self):
        print(f'Loading MAT JSON from {self.path}')
        with open(self.path, 'r') as f:
            json = f.read()
            self.deserialize(json)
