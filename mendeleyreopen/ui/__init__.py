from .mainwindow import Ui_MainWindow
from PyQt4 import QtGui


class Main(QtGui.QMainWindow):
	def __init__(self, main_view=None):
		QtGui.QMainWindow.__init__(self)
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.ui.menubar.hide()
		if main_view is not None:
			self.ui.defaultViewText.hide()
			self.ui.verticalLayout.addWidget(main_view)
