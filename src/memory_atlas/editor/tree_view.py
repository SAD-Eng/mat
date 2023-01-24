"""
This module contains ViewModel (aka 'Qt model') classes which implement the left-hand navigation tree in the
editor. This uses the Qt Model/View where the .ui file has a QTreeView whose model is set to an instance
of the AtlasTreeViewModel in this module. That view model then offers up other child view models which are also
in this module.

See https://doc.qt.io/qtforpython/overviews/qtwidgets-itemviews-simpletreemodel-example.html
"""
from __future__ import annotations  # enable forward references in type hints https://stackoverflow.com/a/33844891

import functools
from abc import abstractmethod
from typing import Union, Any

from PySide6 import QtCore

from ..models import MemoryAtlas, BinaryObjectModel, BomVariable
from .detail_panels import DetailPanel, BomDetailPanel, BomVariableDetailPanel


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
    def register_type(cls, vm_type: AtlasTreeItemViewModelBase, model_type):
        cls._type_registry[model_type.__name__] = vm_type

    def get_vm(self, model: Any, parent: AtlasTreeItemViewModelBase):
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


class AtlasTreeItemViewModelBase:
    """Base class for tree view items - each class in memory_atlas.models will have an associated subclass"""
    def __init__(self, parent_vm):
        self.parent_vm = parent_vm  # in the case of the root MemoryAtlasTreeItemViewModel this will be null

    @abstractmethod
    def get_model(self) -> Any:
        """Child classes must override this to return their model instance"""
        pass

    @abstractmethod
    def get_children(self) -> list:
        """Child classes must override this to return a list of their child models"""

    @abstractmethod
    def get_text(self) -> str:
        """Child classes must override this to return the text string that should appear in the tree"""

    @abstractmethod
    def get_detail_panel(self) -> DetailPanel:
        """Child classes must override this to return an instantiated detail panel widget for editing their model"""


class AtlasTreeViewModel(QtCore.QAbstractItemModel):
    """
    The tree view has this single implementation of QAbstractItemModel. This reduces complexity as the example
    shows a single model handling generic tree nodes. In our case the nodes are varied in type, but they are all
    subclasses of the abstract AtlasTreeItemViewModelBase. The base class gives us a clear contract for what
    each type of model needs to provide to be presented in the tree view.
    """
    def __init__(self, atlas: MemoryAtlas, parent: QtCore.QObject):
        # Note that "parent" here is a parent widget or other object, not related to the tree itself
        super().__init__(parent)
        self.atlas = atlas
        self.factory = AtlasTreeViewModelItemFactory()
        self.atlas_vm = self.factory.get_vm(self.atlas, None)

    def rowCount(self, parent: QtCore.QModelIndex = ...) -> int:
        if not parent.isValid():
            children = self.atlas_vm.get_children()
        else:
            children = parent.internalPointer().get_children()
        return len(children)

    def columnCount(self, parent: QtCore.QModelIndex = ...) -> int:
        return 1

    def data(self, index: QtCore.QModelIndex, role: int = ...) -> Any:
        if role == QtCore.Qt.DisplayRole:
            return index.internalPointer().get_text()
        return

    def index(self, row: int, column: int, parent: QtCore.QModelIndex = ...) -> QtCore.QModelIndex:
        if self.hasIndex(row, column, parent):
            parent_vm = parent.internalPointer()
            if parent_vm is None:
                children = self.atlas_vm.get_children()
            else:
                children = parent_vm.get_children()
            child_model = children[row]
            child_vm = self.factory.get_vm(child_model, parent_vm)
            return self.createIndex(row, column, child_vm)
        return QtCore.QModelIndex()

    def parent(self, child: QtCore.QModelIndex = ...) -> QtCore.QModelIndex:
        child_vm = child.internalPointer()
        parent_vm = child_vm.parent_vm
        if parent_vm is None:
            return QtCore.QModelIndex()
        row = parent_vm.get_children().index(child_vm.get_model())
        return self.createIndex(row, 0, parent_vm)


@atlas_tree_view_model(MemoryAtlas)
class MemoryAtlasTreeItemViewModel(AtlasTreeItemViewModelBase):
    def __init__(self, atlas: MemoryAtlas, parent_vm: AtlasTreeItemViewModelBase):
        super().__init__(parent_vm)
        self.atlas = atlas

    def get_model(self):
        return self.atlas

    def get_children(self):
        return self.atlas.boms

    def get_text(self) -> str:
        return f'Memory Atlas {self.atlas.mat_version}'

    def get_detail_panel(self) -> DetailPanel:
        raise NotImplementedError()


@atlas_tree_view_model(BinaryObjectModel)
class BinaryObjectModelTreeItemViewModel(AtlasTreeItemViewModelBase):
    def __init__(self, bom: BinaryObjectModel, parent_vm: AtlasTreeItemViewModelBase):
        super().__init__(parent_vm)
        self.bom = bom
        self.detail_panel = BomDetailPanel(bom)

    def get_model(self):
        return self.bom

    def get_children(self):
        return self.bom.variables

    def get_text(self) -> str:
        return f'BOM {self.bom.name}'

    def get_detail_panel(self) -> DetailPanel:
        return self.detail_panel


@atlas_tree_view_model(BomVariable)
class BomVariableTreeItemViewModel(AtlasTreeItemViewModelBase):
    def __init__(self, var: BomVariable, parent_vm: AtlasTreeItemViewModelBase):
        super().__init__(parent_vm)
        self.var = var
        self.detail_panel = BomVariableDetailPanel(var)

    def get_model(self):
        return self.var

    def get_children(self):
        return []

    def get_text(self) -> str:
        return f'Variable {self.var.name}'

    def get_detail_panel(self) -> DetailPanel:
        return self.detail_panel
