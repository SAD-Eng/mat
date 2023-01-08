"""
This module contains ViewModel (aka 'Qt model') classes which implement the left-hand navigation tree in the
editor. This uses the Qt Model/View where the .ui file has a QTreeView whose model is set to an instance
of the AtlasTreeViewModel in this module. That view model then offers up other child view models which are also
in this module.
"""
from __future__ import annotations  # enable forward references in type hints https://stackoverflow.com/a/33844891

import functools
from abc import abstractmethod
from typing import Union, Any

from PySide6 import QtCore

from ..models import MemoryAtlas, BinaryObjectModel, BomVariable


class AtlasTreeViewModelItemFactory:
    """
    Factory which creates child view models (descended from AtlasTreeBaseViewModel). View models are cached
    by the identity of the model object they wrap. This ensures that if an object is relocated in the tree and
    a new request is made to list that item, the same view model instance will be returned in the new location
    in the tree. Because of this approach, sharing a factory instance across e.g. a new file being opened
    has undefined behavior. Therefore, the lifetime of each factory object is managed by the root
    view model (AtlasTreeViewModel).

    The factory works by maintaining a "static" registry of view model types, which use the @atlas_tree_view_model
    decorator to register themselves. Typically, all such classes are in this same file, but this approach should
    allow arbitrary plugins or similar in the future as long as care can be taken to ensure all such models
    are imported so that the decorators execute.
    """
    _type_registry = {}

    def __init__(self):
        self._vm_cache = {}

    @classmethod
    def register_type(cls, vm_type: AtlasTreeBaseViewModel, model_type):
        print(f'Registering vm_type {vm_type.__name__} for model_type {model_type.__name__}')
        cls._type_registry[model_type.__name__] = vm_type

    def get_vm(self, model: Any, parent: AtlasTreeBaseViewModel):
        if id(model) not in self._vm_cache:
            try:
                vm_type = self._type_registry[type(model).__name__]
            except KeyError as err:
                raise NotImplementedError(f'Unsupported model type, {type(model).__name__} needs a view model class '
                                          f'defined with @atlas_tree_view_model') from err
            vm = vm_type(model, parent)
            self._vm_cache[id(model)] = vm
        return self._vm_cache[id(model)]


class atlas_tree_view_model:
    """
    Decorator to be applied to a view model class, which passes in the type of its model class. The purpose
    of this decorator is to automatically register the view model classes with the AtlasTreeViewModelItemFactory.
    Example:
    @atlas_tree_view_model(MemoryAtlas)
    class AtlasTreeViewModel...
    """
    def __init__(self, model_type):
        self.model_type = model_type

    def __call__(self, vm_type):
        # note that our wrapper is a subclass of vm_type so that e.g. isinstance() will work correctly
        class WrapperClass(vm_type):
            pass

        # copy over __name__ and such so that you can't tell the difference between the wrapper and the original
        for meta_attr in functools.WRAPPER_ASSIGNMENTS:
            setattr(WrapperClass, meta_attr, getattr(vm_type, meta_attr))

        # importantly, we need to register the WrapperClass, not the original, for isinstance() support
        AtlasTreeViewModelItemFactory.register_type(WrapperClass, self.model_type)

        return WrapperClass


class AtlasTreeBaseViewModel(QtCore.QAbstractItemModel):
    def __init__(self, parent):
        super().__init__(parent)
        self._parent_vm = parent  # in the case of AtlasTreeViewModel, this may be some Qt widget

    @abstractmethod
    def get_model(self) -> Any:
        """Child classes must override this to return their model instance"""
        pass

    def vm_factory(self) -> AtlasTreeViewModelItemFactory:
        """Returns the AtlasTreeViewModelItemFactory instance associated with this tree view"""
        runner = self
        while not hasattr(runner, 'factory'):
            runner = runner._parent_vm
        return runner.factory

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 1


@atlas_tree_view_model(MemoryAtlas)
class AtlasTreeViewModel(AtlasTreeBaseViewModel):
    def __init__(self, atlas: MemoryAtlas, parent=None):
        super().__init__(parent)
        self.atlas = atlas
        self.factory = AtlasTreeViewModelItemFactory()

    def get_model(self):
        return self.atlas

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self.atlas.boms)

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex], role: int = ...) -> Any:
        if role == QtCore.Qt.DisplayRole:
            return self.atlas.boms[index.row()].name
        return

    def index(self, row: int, column: int,
              parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> QtCore.QModelIndex:
        if self.hasIndex(row, column, parent):
            bom = self.atlas.boms[row]
            return self.createIndex(row, column, self.vm_factory().get_vm(bom, self))
        return QtCore.QModelIndex()

    def parent(self, child: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> QtCore.QModelIndex:
        # we are always the root of the tree, so we can return an empty index
        return QtCore.QModelIndex()


@atlas_tree_view_model(BinaryObjectModel)
class BomTreeViewModel(AtlasTreeBaseViewModel):
    def __init__(self, bom: BinaryObjectModel, parent: AtlasTreeBaseViewModel):
        super().__init__(parent)
        self.bom = bom

    def get_model(self):
        return self.bom

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self.bom.variables)

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex], role: int = ...) -> Any:
        if role == QtCore.Qt.DisplayRole:
            return self.bom.variables[index.row()].name
        return

    def index(self, row: int, column: int,
              parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> QtCore.QModelIndex:
        if self.hasIndex(row, column, parent):
            var = self.bom.variables[row]
            return self.createIndex(row, column, self.vm_factory().get_vm(var, self))
        return QtCore.QModelIndex()

    def parent(self, child: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex]) -> QtCore.QModelIndex:
        row = self._parent_vm.atlas.boms.index(self.bom)
        return self.createIndex(row, 0, self._parent_vm)
