from os import path

from PySide6 import QtCore

from memory_atlas.models import MemoryAtlas, BinaryObjectModel, SemVer
from memory_atlas.mat_json import MatJsonFile
from memory_atlas.editor.tree_view import AtlasTreeViewModel, BomTreeViewModel, AtlasTreeViewModelItemFactory

project_dir = path.dirname(path.dirname(__file__))


def test_vm_factory():
    atlas = MemoryAtlas(SemVer(0, 0, 0))
    bom = BinaryObjectModel("foo", "desc", SemVer(0, 0, 0))
    atlas.boms.append(bom)

    factory = AtlasTreeViewModelItemFactory()
    atlas_vm = factory.get_vm(atlas, None)
    assert isinstance(atlas_vm, AtlasTreeViewModel)
    bom_vm = factory.get_vm(bom, atlas_vm)
    assert isinstance(bom_vm, BomTreeViewModel)


def test_atlas_boms():
    file_obj = MatJsonFile(path.join(project_dir, 'examples/test.mat.json'))
    file_obj.load()
    atlas = file_obj.atlas
    atlas_vm = AtlasTreeViewModel(atlas)
    assert atlas_vm.get_model() == atlas
    assert atlas_vm.rowCount() == 1
    index = QtCore.QModelIndex()
    index.row()
    assert atlas_vm.data(atlas_vm.createIndex(0, 0), QtCore.Qt.DisplayRole) == atlas.boms[0].name
    bom_vm_index = atlas_vm.index(0, 0, QtCore.QModelIndex())
    bom = bom_vm_index.model()
    assert isinstance(bom, BomTreeViewModel)
