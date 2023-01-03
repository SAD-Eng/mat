"""
This module contains ViewModel (aka 'Qt model') classes which implement the left-hand navigation tree in the
editor. This uses the Qt Model/View where the .ui file has a QTreeView whose model is set to an instance
of the AtlasTreeViewModel in this module. That view model then offers up other child view models which are also
in this module.
"""
from typing import Union, Any

from PySide6 import QtCore

from ..models import MemoryAtlas, BinaryObjectModel, BomVariable


class AtlasTreeViewModel(QtCore.QAbstractItemModel):
    def __init__(self, atlas: MemoryAtlas, parent=None):
        super().__init__(parent)
        self.atlas = atlas

    def rowCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return len(self.atlas.boms)

    def columnCount(self, parent: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex] = ...) -> int:
        return 1

    def data(self, index: Union[QtCore.QModelIndex, QtCore.QPersistentModelIndex], role: int = ...) -> Any:
        if role == QtCore.Qt.DisplayRole:
            return self.atlas.boms[index.row()].name
        return

