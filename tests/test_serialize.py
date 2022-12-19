import json
import tempfile
from os import path

from memory_atlas.models import MemoryAtlas, BinaryObjectModel, BomVariable
from memory_atlas.mat_json import MatJsonFile


def test_simple_atlas_serialize():
    atlas = MemoryAtlas()
    bom = BinaryObjectModel(name='foo')
    atlas.boms.append(bom)
    var = BomVariable(name='bar', version_major=1, version_minor=0)
    bom.variables.append(var)

    file = MatJsonFile('unused.txt', atlas)
    json_dict = json.loads(file.serialize())

    assert len(json_dict['boms']) == 1
    assert json_dict['boms'][0]['name'] == bom.name
    assert len(json_dict['boms'][0]['variables']) == 1
    var_obj = json_dict['boms'][0]['variables'][0]
    assert var_obj['name'] == var.name
    assert var_obj['version_major'] == var.version_major
    assert var_obj['version_minor'] == var.version_minor


def test_simple_atlas_round_trip():
    atlas = MemoryAtlas()
    bom = BinaryObjectModel(name='foo')
    atlas.boms.append(bom)
    var = BomVariable(name='bar', version_major=1, version_minor=0)
    bom.variables.append(var)

    with tempfile.TemporaryDirectory() as tempdir_name:
        file = MatJsonFile(path.join(tempdir_name, 'test.mat.json'), atlas)
        file.save()

        with open(file.path, 'r') as json_file:
            json_dict = json.load(json_file)

        assert len(json_dict['boms']) == 1
        assert json_dict['boms'][0]['name'] == bom.name

        file.load()
        round_trip = file.atlas

        assert bom.name == round_trip.boms[0].name
        assert var.name == round_trip.boms[0].variables[0].name
