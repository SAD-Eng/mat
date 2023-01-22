"""
This module provides the various "detail panel" widgets which are "stacked" on in the center editing panel of the
main window. As selections are made in the left hand tree view, the "current page" of the stack is changed to swap
between the detail panel instances (one per model). Generally speaking these all use a QFormLayout to create
an "editing form" to edit the associated model.

The Qt model view architecture doesn't seem to provide any useful help here, and the UI XML form of this is uselessly
verbose, so for this portion of the GUI we are using traditional Qt procedural code.
"""
from abc import abstractmethod

from PySide6 import QtWidgets, QtCore

from ..models import BinaryObjectModel, BomVariable


def make_slot(model: object, prop: str, converter: callable = None):
    def callback(value):
        if converter is not None:
            value = converter(value)
        setattr(model, prop, value)
    return callback


class DetailPanel(QtWidgets.QWidget):
    @abstractmethod
    def model_to_view(self):
        """Child classes must override this method to populate model values to the appropriate view controls"""


class BomDetailPanel(DetailPanel):
    def __init__(self, bom: BinaryObjectModel):
        super().__init__()
        self.bom = bom

        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.textEdited.connect(make_slot(self.bom, 'name'))
        self.description_edit = QtWidgets.QLineEdit()
        self.description_edit.textEdited.connect(make_slot(self.bom, 'description'))
        # TODO: SemVer editor widget?
        self.version_edit = QtWidgets.QLineEdit()
        self.version_edit.textEdited.connect(make_slot(self.bom, 'version'))
        # TODO: How to add variables? tree action? button on this panel? toolbar action?

        form = QtWidgets.QFormLayout()
        form.addRow('Name:', self.name_edit)
        form.addRow('Description:', self.description_edit)
        form.addRow('Version:', self.version_edit)
        self.setLayout(form)

        self.model_to_view()

    def model_to_view(self):
        self.name_edit.setText(self.bom.name)
        self.description_edit.setText(self.bom.description)
        self.version_edit.setText(str(self.bom.version))


class BomVariableDetailPanel(DetailPanel):
    def __init__(self, var: BomVariable):
        super().__init__()
        self.var = var

        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.textEdited.connect(make_slot(self.var, 'name'))
        self.description_edit = QtWidgets.QLineEdit()
        self.description_edit.textEdited.connect(make_slot(self.var, 'description'))
        # TODO: variable types, swap out the editing controls based on selection

        form = QtWidgets.QFormLayout()
        form.addRow('Name:', self.name_edit)
        form.addRow('Description:', self.description_edit)
        self.setLayout(form)

        self.model_to_view()

    def model_to_view(self):
        self.name_edit.setText(self.var.name)
        self.description_edit.setText(self.var.description)
