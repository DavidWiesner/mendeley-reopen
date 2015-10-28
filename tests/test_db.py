import time

from mendeleyreopen import find_mendeley_db_file
from mendeleyreopen.db import MendeleyDB

__author__ = 'david'

import unittest


class MyTestCase(unittest.TestCase):
	def test_local(self):
		mendeley_database = find_mendeley_db_file()
		with MendeleyDB(mendeley_database) as mendeley_db:
			sessions = mendeley_db.get_last_opened_sessions()
			self.assertLess(0, len(sessions))
			for session in sessions:
				print(session)
				for doc in session.documents:
					print(doc)

	def test_ignore_last_closed(self):
		cursor = []
		self._addClosedDoc(cursor, "ignore close")
		self._addOpenedDoc(cursor, "ignore_open")
		self._addClosedRow(cursor)

		sessions = MendeleyDB._build_sessions(cursor)
		self.assertEqual(0, len(sessions))

		self._addClosedDoc(cursor, "close")
		self._addOpenedDoc(cursor, "open")

		sessions = MendeleyDB._build_sessions(cursor)
		self.assertEqual(1, len(sessions))

	def test_ignore_empty_closed_sessions(self):
		cursor = []
		self._addOpenedDoc(cursor, "ignore_open")
		self._addClosedRow(cursor)
		self._addClosedDoc(cursor, "ignore close")
		self._addClosedRow(cursor)
		self._addClosedRow(cursor)

		sessions = MendeleyDB._build_sessions(cursor)
		self.assertEqual(0, len(sessions))

	def test_add_twice(self):
		cursor = []
		self._addClosedRow(cursor)
		self._addOpenedDoc(cursor, "open")
		self._addOpenedDoc(cursor, "open")
		self._addClosedRow(cursor)
		self._addClosedRow(cursor)

		sessions = MendeleyDB._build_sessions(cursor)
		self.assertEqual(1, len(sessions))
		self.assertEqual(1, len(sessions[0].documents))

	def test_ignore_closed_doc(self):
		cursor = []
		self._addClosedRow(cursor)
		self._addClosedDoc(cursor, "closed_uuid")
		self._addOpenedDoc(cursor, "closed_uuid")
		self._addOpenedDoc(cursor, "uuid")

		sessions = MendeleyDB._build_sessions(cursor)

		self.assertEqual(1, len(sessions))
		self.assertEqual(1, sessions[0].size)
		self.assertEqual("uuid", list(sessions[0].documents)[0].uuid)

	def test_multi_session(self):
		cursor = []
		self._addClosedRow(cursor)
		self._addClosedDoc(cursor, "closed_uuid")
		self._addOpenedDoc(cursor, "closed_uuid")
		self._addOpenedDoc(cursor, "uuid")
		self._addClosedRow(cursor)
		self._addOpenedDoc(cursor, "closed_uuid")
		self._addOpenedDoc(cursor, "uuid")
		self._addOpenedDoc(cursor, "another_uuid")

		sessions = MendeleyDB._build_sessions(cursor)

		self.assertEqual(2, len(sessions))
		self.assertEqual(1, sessions[0].size)
		self.assertEqual(3, sessions[1].size)
		self.assertEqual("uuid", list(sessions[0].documents)[0].uuid)

	def _addClosedRow(self, cursor):
		cursor.append(self._create_row(time.time(), 'CloseApplication'))

	def _addClosedDoc(self, cursor, uuid, title=None):
		cursor.append(self._create_row(time.time(), 'ClosePdfInternalViewer', uuid, title, uuid))

	def _addOpenedDoc(self, cursor, uuid, title=None):
		cursor.append(self._create_row(time.time(), 'SwitchToPdfInternalViewer', uuid, title, uuid))

	def _create_row(self, datetime=None, action=None, value=None, title=None, uuid=None, remote_uuid=None, fileuri=None):
		return datetime, action, value, title, uuid, remote_uuid, fileuri


if __name__ == '__main__':
	unittest.main()
