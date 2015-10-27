#!/usr/bin/env python2.7
from argparse import ArgumentParser
import os
import sys
import urllib
from itertools import ifilter
try:
	import sqlite3
except:
	from pysqlite2 import dbapi2 as sqlite3

import subprocess
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def main(argv=sys.argv):
	mendeley_database = find_mendeley_db_file()

	if not os.path.isfile(mendeley_database):
		sys.stderr.write('File "%s" does not exist\n' % mendeley_database)
		exit(1)
	
	with MendeleyDB(mendeley_database) as mendeley_db:
		openedFiles = mendeley_db.get_last_opened_files()
		print("%d opened Files found to open" % len(openedFiles))
		app = QApplication(argv)
		table = FilesTable(openedFiles)
		table.show()
		sys.exit(app.exec_())
		for (uri, title) in openedFiles:
			print(uri)
			name = raw_input("press enter to open '%s': " % title) 
			fileopen(uri)

def find_mendeley_db_file():
	import glob
	from appdirs import user_data_dir
	dataDir = os.path.join(user_data_dir("data"), 'Mendeley Ltd.', "Mendeley Desktop")
	files = glob.glob(dataDir+'/*@www.mendeley.com.sqlite')
	return files[0] if len(files) > 0 else None

def fileopen(filepath):
	import subprocess, os
	if sys.platform.startswith('darwin'):
		subprocess.call(('open', filepath))
	elif os.name == 'nt':
		os.startfile(filepath)
	elif os.name == 'posix':
		FNULL = open(os.devnull, 'w')
		subprocess.call(['xdg-open', filepath], stdout=FNULL, stderr=subprocess.STDOUT)


class FocusFilter(QObject):
	def __init__(self, table):
		QObject.__init__(self)
		self.table=table
	def eventFilter(self, widget, event):
		index = self.table.indexAt(widget.pos())
		if event.type() == QEvent.FocusIn:
			print("FocusIn", widget)
			if index.isValid():
				self.table.selectRow(index.row())
			return False
		else:
			return QObject.eventFilter(self, widget, event)

class FilesTable(QTableWidget):
	def __init__(self, data, *args):
		cols=len(data[0])
		QTableWidget.__init__(self, len(data), cols,*args)
		self.data = data
		self.setMinimumWidth(600)
		self.setMinimumHeight(400)
		self.setmydata()
		
		h = self.horizontalHeader()
		h.setStretchLastSection(False)
		#self.resizeRowsToContents()
		self.resizeColumnToContents(1)
		self.resizeColumnToContents(2)
		h.setResizeMode(0, QHeaderView.Stretch)
		h.setResizeMode(1, QHeaderView.Fixed)
		h.setResizeMode(2, QHeaderView.Fixed)
		
		v = self.verticalHeader()
		v.setVisible(False)
		v.setDefaultSectionSize(v.fontMetrics().height()*2.5)
		
		self.setShowGrid(False)
		#self.setStyleSheet("QHeaderView{margin:5px;}");
		
		self.setEditTriggers( QTableWidget.NoEditTriggers )
		self.setSelectionMode(QAbstractItemView.SingleSelection)
		self.setSelectionBehavior(QTableView.SelectRows)
		self.setFocusPolicy(Qt.NoFocus)
		
	def openClicked(self, item):
		button = self.sender()
		index = self.indexAt(button.pos())
		if index.isValid():
			self.selectRow(index.row())
			row = self.data[index.row()]
			fileopen(row[0])
		
	def setmydata(self):
		horHeaders = []
		self.eventFilter=FocusFilter(self)
		self.installEventFilter(self.eventFilter)

		for n, (uri, title, datetime) in enumerate(self.data):
			titleText = QTableWidgetItem(title if title is not None else "Mendeley closed")
			dateText = QTableWidgetItem(datetime)
			titleText.setTextAlignment(Qt.AlignLeading|Qt.AlignTop )
			dateText.setTextAlignment(Qt.AlignLeading|Qt.AlignTop )
			self.setItem(n, 0, titleText)
			self.setItem(n, 1, dateText)
			if uri is not None:
				button = QPushButton("Open in Mendeley", parent=self)
				button.clicked.connect(self.openClicked)
			else:
				button = QPushButton("", parent=self)
				button.setFlat(True)
			button.setAutoDefault(True)
			button.installEventFilter(self.eventFilter)				
			self.setCellWidget(n, 2, button)
		self.setHorizontalHeaderLabels(["Title", "", ""])
	
class MendeleyDB(object):
	select_events="""Select DATETIME(l.timestamp, 'unixepoch'), l.type, d.title, a.value, r.remoteUuid, f.localUrl
				FROM EventAttributes as a
				LEFT JOIN EventLog as l ON (a.eventId=l.id)
				LEFT JOIN Files as f ON(a.value = f.hash)
				LEFT JOIN DocumentFiles as df ON(a.value = df.hash)
				LEFT JOIN Documents as d ON (d.id = df.documentId)
				LEFT JOIN RemoteDocuments as r ON (df.documentId = r.documentId)
				WHERE a.attribute in ("FileHash", "WindowSize") AND l.type IN ("SwitchToPdfInternalViewer", "ClosePdfInternalViewer", "CloseApplication")
				ORDER BY l.timestamp DESC
				"""
	def __init__(self, path):
		self.path = path
	def __enter__(self):
		self.connection = sqlite3.connect(self.path)
		self.cursor = self.connection.cursor()
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		self.connection.commit()
		self.cursor.close()
		
	def execute(self, statement, values=()):
		return self.cursor.execute(statement, values)
	
	def get_last_opened_files(self):
		finalClose=False
		nillValues=(None, None, None)
		openedFiles=[]
		closedFilesHashes=[]
		openedFilesHashes=[]
		for (datetime, action, title, value, uuid, fileuri) in self.execute(self.select_events):
			path=urllib.unquote(fileuri.encode('utf-8')) if fileuri is not None else ""#.decode('utf-8')
			print((datetime, action, title, value, uuid))
			if uuid is not None:
				uri='mendeley://library/document/'+uuid
			else:
				uri=None
			if finalClose and u'CloseApplication' in action:
#				break
				if len(openedFiles) == 0 or openedFiles[-1][0] != None:
					openedFiles.append((None,None, datetime))
			elif u'CloseApplication' in action:
				finalClose = True
				if len(openedFiles) == 0 or openedFiles[-1][0] != None:
					openedFiles.append((None,None, datetime))
			elif finalClose:
				if u'SwitchToPdfInternalViewer' in action and value not in closedFilesHashes and value not in openedFilesHashes:
					openedFiles.append((uri, title, datetime))
					openedFilesHashes.append(value)
				elif u'ClosePdfInternalViewer' in action:
					closedFilesHashes.append(value)
		if len(openedFiles) > 0 and openedFiles[-1][0] == None:
			del openedFiles[-1]
		return openedFiles


if __name__ == '__main__':
	main(sys.argv)