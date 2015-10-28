from PyQt4 import QtCore, QtGui
from mendeleyreopen.model import Document
from mendeleyreopen.model import Session

QtCore.Signal = QtCore.pyqtSignal
from ..utils import *


class FocusFilter(QtCore.QObject):
	def __init__(self, table):
		QtCore.QObject.__init__(self)
		self.table = table

	def eventFilter(self, widget, event):
		index = self.table.indexAt(widget.pos())
		if event.type() == QtCore.QEvent.FocusIn:
			print("FocusIn", widget)
			if index.isValid():
				self.table.selectRow(index.row())
			return False
		else:
			return QtCore.QObject.eventFilter(self, widget, event)


class FilesTable(QtGui.QTableWidget):
	def __init__(self, sessions: "List[Session]", *args):
		self.eventFilter = FocusFilter(self)
		cols = 3
		sum_docs = [x.size for x in sessions]
		rows = sum(sum_docs) + len(sessions)

		self.row_index = self._build_row_index(sessions)

		QtGui.QTableWidget.__init__(self, rows, cols, *args)
		self.sessions = sessions
		self.setMinimumWidth(600)
		self.setMinimumHeight(400)
		self.set_data()

		h = self.horizontalHeader()
		h.setStretchLastSection(False)
		self.resizeColumnToContents(1)
		self.resizeColumnToContents(2)
		h.setResizeMode(0, QtGui.QHeaderView.Stretch)
		h.setResizeMode(1, QtGui.QHeaderView.Fixed)
		h.setResizeMode(2, QtGui.QHeaderView.Fixed)

		v = self.verticalHeader()
		v.setVisible(False)
		v.setDefaultSectionSize(v.fontMetrics().height() * 2.5)

		self.setShowGrid(False)

		self.setEditTriggers(QtGui.QTableWidget.NoEditTriggers)
		self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
		self.setSelectionBehavior(QtGui.QTableView.SelectRows)
		self.setFocusPolicy(QtCore.Qt.NoFocus)

	@staticmethod
	def _build_row_index(sessions):
		row_index = []
		for n, session in enumerate(sessions):
			row_index.append((n, None))
			for m, doc in enumerate(session.documents):
				row_index.append((n, m))
		return row_index

	def open_clicked(self, item):
		button = self.sender()
		index = self.indexAt(button.pos())
		if index.isValid():
			self.selectRow(index.row())
			doc = self.get_doc_by_row(index.row())
			if doc is not None:
				fileopen(doc.get_uri())

	def get_doc_by_row(self, row) -> "Document":
		if row > len(self.row_index):
			return None
		index = self.row_index[row]
		if index[1] is None:
			return None
		return self.sessions[index[0]].documents[index[1]]

	def set_data(self):
		self.installEventFilter(self.eventFilter)
		count = 0
		for session in self.sessions:
			self.add_row(++count, session.ended, None, None)
			count += 1
			for doc in session.documents:
				self.add_row(++count, doc.access, doc.title, doc.get_uri())
				count += 1

			self.setHorizontalHeaderLabels(["Title", "", ""])

	def add_row(self, n, datetime, title, uri):
		title_text = QtGui.QTableWidgetItem(title if title is not None else "Mendeley closed")
		date_text = QtGui.QTableWidgetItem(datetime)
		title_text.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
		date_text.setTextAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignTop)
		self.setItem(n, 0, title_text)
		self.setItem(n, 1, date_text)
		if uri is not None:
			button = QtGui.QPushButton("Open in Mendeley", parent=self)
			button.clicked.connect(self.open_clicked)
		else:
			button = QtGui.QPushButton("", parent=self)
			button.setFlat(True)
		button.setAutoDefault(True)
		button.installEventFilter(self.eventFilter)
		self.setCellWidget(n, 2, button)
