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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLabel,
    QMainWindow, QMenu, QMenuBar, QSizePolicy,
    QStackedWidget, QStatusBar, QTreeView, QWidget)

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

        self.gridLayout.addWidget(self.atlasTree, 0, 0, 1, 1)

        self.detailsPanelStack = QStackedWidget(self.widget)
        self.detailsPanelStack.setObjectName(u"detailsPanelStack")
        self.bomDetailPanel = QWidget()
        self.bomDetailPanel.setObjectName(u"bomDetailPanel")
        self.gridLayout1 = QGridLayout(self.bomDetailPanel)
        self.gridLayout1.setObjectName(u"gridLayout1")
        self.label = QLabel(self.bomDetailPanel)
        self.label.setObjectName(u"label")

        self.gridLayout1.addWidget(self.label, 0, 0, 1, 1)

        self.detailsPanelStack.addWidget(self.bomDetailPanel)

        self.gridLayout.addWidget(self.detailsPanelStack, 0, 1, 1, 1)

        self.gridLayout.setColumnStretch(1, 1)
        MainWindow.setCentralWidget(self.widget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.actionNew = QAction(self.menubar)
        self.actionNew.setObjectName(u"actionNew")
        self.actionOpen = QAction(self.menubar)
        self.actionOpen.setObjectName(u"actionOpen")
        self.actionSave = QAction(self.menubar)
        self.actionSave.setObjectName(u"actionSave")
        self.actionExit = QAction(self.menubar)
        self.actionExit.setObjectName(u"actionExit")
        self.fileMenu = QMenu(self.menubar)
        self.fileMenu.setObjectName(u"fileMenu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.fileMenu.menuAction())
        self.fileMenu.addAction(self.actionNew)
        self.fileMenu.addAction(self.actionOpen)
        self.fileMenu.addAction(self.actionSave)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.actionExit)

        self.retranslateUi(MainWindow)
        self.actionNew.triggered.connect(MainWindow.new)
        self.actionOpen.triggered.connect(MainWindow.open)
        self.atlasTree.clicked.connect(MainWindow.tree_selection_changed)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Memory Atlas Editor", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Name:", None))
        self.actionNew.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.actionOpen.setText(QCoreApplication.translate("MainWindow", u"Open", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"Save", None))
        self.actionExit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.fileMenu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
    # retranslateUi

