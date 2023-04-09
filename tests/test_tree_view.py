from os import path

from PySide6 import QtCore

from memory_atlas.models import MemoryAtlas, BinaryObjectModel, SemVer
from memory_atlas.mat_json import MatJsonFile
from memory_atlas.editor.tree_view import AtlasTreeViewModelItemFactory, AtlasTreeViewModel, \
    MemoryAtlasTreeItemViewModel, BinaryObjectModelTreeItemViewModel, BomVariableTreeItemViewModel

project_dir = path.dirname(path.dirname(__file__))


def test_vm_factory(qtbot):
    atlas = MemoryAtlas(SemVer(0, 0, 0))
    bom = BinaryObjectModel("foo", "desc", SemVer(0, 0, 0))
    atlas.boms.append(bom)

    factory = AtlasTreeViewModelItemFactory()
    atlas_vm = factory.get_vm(atlas, None)
    assert isinstance(atlas_vm, MemoryAtlasTreeItemViewModel)
    bom_vm = factory.get_vm(bom, atlas_vm)
    assert isinstance(bom_vm, BinaryObjectModelTreeItemViewModel)


def test_tree_child_listing(qtbot):
    file_obj = MatJsonFile(path.join(project_dir, 'examples/test.mat.json'))
    file_obj.load()
    atlas = file_obj.atlas
    atlas_tree = AtlasTreeViewModel(atlas, None)

    assert atlas_tree.rowCount(QtCore.QModelIndex()) == 1
    bom_vm_index = atlas_tree.index(0, 0, QtCore.QModelIndex())
    bom_vm = bom_vm_index.internalPointer()
    assert isinstance(bom_vm, BinaryObjectModelTreeItemViewModel)

    assert atlas_tree.rowCount(bom_vm_index) == 1
    var_vm_index = atlas_tree.index(0, 0, bom_vm_index)
    var_vm = var_vm_index.internalPointer()
    assert isinstance(var_vm, BomVariableTreeItemViewModel)
