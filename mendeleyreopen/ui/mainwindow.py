# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mendeleyreopen/ui/mainwindow.ui'
#
# Created: Wed Oct 28 13:53:08 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(782, 510)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("mendeleydesktop"))
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.defaultViewText = QtGui.QLabel(self.centralwidget)
        self.defaultViewText.setAlignment(QtCore.Qt.AlignCenter)
        self.defaultViewText.setObjectName(_fromUtf8("defaultViewText"))
        self.verticalLayout.addWidget(self.defaultViewText)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuMen = QtGui.QMenu(self.menubar)
        self.menuMen.setObjectName(_fromUtf8("menuMen"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionClose = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon.fromTheme(_fromUtf8("close"))
        self.actionClose.setIcon(icon)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.menuMen.addAction(self.actionClose)
        self.menubar.addAction(self.menuMen.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Mendeley Reopen", None))
        self.defaultViewText.setText(_translate("MainWindow", "No Sessions found", None))
        self.menuMen.setTitle(_translate("MainWindow", "&File", None))
        self.actionClose.setText(_translate("MainWindow", "&Close", None))
        self.actionClose.setShortcut(_translate("MainWindow", "Ctrl+Q", None))

