"""
This provides the MainWindow class that acts essentially as a "controller" to wire up the main editor window.
This instantiates the top level view models and assigns them to the ui view widgets that display them. For example,
this class instantiates a ...tree_view.AtlasTreeViewModel and set it as the model of the atlasTree QTreeView widget.
"""
from PySide6 import QtWidgets, QtCore

from .ui_main_window import Ui_MainWindow
from .tree_view import AtlasTreeViewModel, BinaryObjectModelTreeItemViewModel
from ..models import MemoryAtlas
from ..mat_json import MatJsonFile


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # TODO: remember last open file, prompt for one on startup, etc.
        self.atlas = None
        self.tree_vm = None
        self.file_obj = None
        self.new()

    @QtCore.Slot()
    def new(self):
        self.atlas = MemoryAtlas()
        self._create_vm()

    @QtCore.Slot()
    def open(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, caption='Open MAT JSON File',
                                                             filter='MAT JSON Files (*.mat.json)')
        self.file_obj = MatJsonFile(file_path)
        self.file_obj.load()
        self.atlas = self.file_obj.atlas
        self._create_vm()

    @QtCore.Slot()
    def save(self):
        if self.file_obj is not None:
            self.file_obj.save()

    @QtCore.Slot()
    def exit(self):
        self.close()

    def _create_vm(self):
        self.tree_vm = AtlasTreeViewModel(self.atlas, self)
        self.ui.atlasTree.setModel(self.tree_vm)

    @QtCore.Slot()
    def tree_selection_changed(self, clicked: QtCore.QModelIndex):
        selected_vm = clicked.internalPointer()
        detail_panel = selected_vm.get_detail_panel()
        panel_index = self.ui.detailsPanelStack.indexOf(detail_panel)
        if panel_index < 0:
            panel_index = self.ui.detailsPanelStack.addWidget(detail_panel)
        self.ui.detailsPanelStack.setCurrentIndex(panel_index)