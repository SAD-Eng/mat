# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.4.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QStackedWidget,
    QStatusBar, QToolBar, QTreeView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.widget = QWidget(MainWindow)
        self.widget.setObjectName(u"widget")
        self.gridLayout = QGridLayout(self.widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.atlasTree = QTreeView(self.widget)
        self.atlasTree.setObjectName(u"atlasTree")
        self.atlasTree.setHeaderHidden(True)

        self.gridLayout.addWidget(self.atlasTree, 0, 0, 1, 1)

        self.detailsPanelStack = QStackedWidget(self.widget)
        self.detailsPanelStack.setObjectName(u"detailsPanelStack")

        self.gridLayout.addWidget(self.detailsPanelStack, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)
        MainWindow.setCentralWidget(self.widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.actionNew = QAction(self.menubar)
        self.actionNew.setObjectName(u"actionNew")
        icon = QIcon(u":/icons/file-document-plus.svg")
        self.actionNew.setIcon(icon)
        self.actionOpen = QAction(self.menubar)
        self.actionOpen.setObjectName(u"actionOpen")
        icon1 = QIcon(u":/icons/folder-open.svg")
        self.actionOpen.setIcon(icon1)
        self.actionSave = QAction(self.menubar)
        self.actionSave.setObjectName(u"actionSave")
        icon2 = QIcon(u":/icons/content-save.svg")
        self.actionSave.setIcon(icon2)
        self.actionExit = QAction(self.menubar)
        self.actionExit.setObjectName(u"actionExit")
        self.actionAddBom = QAction(self.menubar)
        self.actionAddBom.setObjectName(u"actionAddBom")
        icon3 = QIcon(u":/icons/puzzle-plus.svg")
        self.actionAddBom.setIcon(icon3)
        self.actionAddBomVariable = QAction(self.menubar)
        self.actionAddBomVariable.setObjectName(u"actionAddBomVariable")
        icon4 = QIcon(u":/icons/variable-box.svg")
        self.actionAddBomVariable.setIcon(icon4)
        self.fileMenu = QMenu(self.menubar)
        self.fileMenu.setObjectName(u"fileMenu")
        self.addMenu = QMenu(self.menubar)
        self.addMenu.setObjectName(u"addMenu")
        MainWindow.setMenuBar(self.menubar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName(u"toolBar")
        MainWindow.addToolBar(Qt.TopToolBarArea, self.toolBar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.addMenu.menuAction())
        self.fileMenu.addAction(self.actionNew)
        self.fileMenu.addAction(self.actionOpen)
        self.fileMenu.addAction(self.actionSave)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actionExit)
        self.addMenu.addAction(self.actionAddBom)
        self.addMenu.addAction(self.actionAddBomVariable)
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAddBom)
        self.toolBar.addAction(self.actionAddBomVariable)

        self.retranslateUi(MainWindow)
        self.actionNew.triggered.connect(MainWindow.new)
        self.actionOpen.triggered.connect(MainWindow.open)
        self.actionSave.triggered.connect(MainWindow.save)
        self.actionExit.triggered.connect(MainWindow.exit)
        self.atlasTree.clicked.connect(MainWindow.tree_selection_changed)
        self.actionAddBom.triggered.connect(MainWindow.add_bom)
        self.actionAddBomVariable.triggered.connect(MainWindow.add_bom_variable)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Memory Atlas Editor", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.actionAddBom.setText(QCoreApplication.translate("MainWindow", u"Add BOM", None))
        self.actionAddBomVariable.setText(QCoreApplication.translate("MainWindow", u"Add Variable", None))
        self.fileMenu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.addMenu.setTitle(QCoreApplication.translate("MainWindow", u"Add", None))
        self.toolBar.setWindowTitle(QCoreApplication.translate("MainWindow", u"toolBar", None))
    # retranslateUi

