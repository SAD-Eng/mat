"""
This provides the MainWindow class that acts essentially as a "controller" to wire up the main editor window.
This instantiates the top level view models and assigns them to the ui view widgets that display them. For example,
this class instantiates a ...tree_view.AtlasTreeViewModel and set it as the model of the atlasTree QTreeView widget.
"""
from PySide6 import QtWidgets

from .ui_mainwindow import Ui_MainWindow
from .tree_view import AtlasTreeViewModel
from ..models import MemoryAtlas


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # TODO: remember last open file, prompt for one on startup, etc.
        self.atlas = MemoryAtlas()
        self.tree_vm = AtlasTreeViewModel(self.atlas, self)
        self.ui.atlasTree.setModel(self.tree_vm)