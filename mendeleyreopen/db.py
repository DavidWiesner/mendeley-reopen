#!/usr/bin/env python2.7
from mendeleyreopen.model import Session, Document
import sqlite3


class MendeleyDB(object):
	select_events = """Select DATETIME(l.timestamp, 'unixepoch'), l.type, a.value,
					d.title, d.uuid, r.remoteUuid, f.localUrl
				FROM EventAttributes as a
				LEFT JOIN EventLog as l ON (a.eventId=l.id)
				LEFT JOIN Files as f ON(a.value = f.hash)
				LEFT JOIN DocumentFiles as df ON(a.value = df.hash)
				LEFT JOIN Documents as d ON (d.id = df.documentId)
				LEFT JOIN RemoteDocuments as r ON (df.documentId = r.documentId)
				WHERE a.attribute in ("FileHash", "WindowSize")
					AND l.type IN ("SwitchToPdfInternalViewer", "ClosePdfInternalViewer", "CloseApplication")
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

	@staticmethod
	def _build_sessions(cursor) -> "List[Session]":
		sessions = []
		current_session = None
		for (datetime, action, value, title, uuid, remoteUuid, fileuri) in cursor:
			if 'CloseApplication' in action:
				if current_session is not None and not current_session.is_empty():
					sessions.append(current_session)
				current_session = Session(datetime)
			elif current_session is not None:
				if 'SwitchToPdfInternalViewer' in action:
					doc = Document(uuid, remoteUuid, title, datetime, fileuri)
					current_session.add_document(doc)
				elif 'ClosePdfInternalViewer' in action:
					current_session.mark_closed(uuid)
		if current_session is not None and not current_session.is_empty():
			sessions.append(current_session)
		return sessions

	def get_last_opened_sessions(self):
		cursor = self.execute(self.select_events)
		return self._build_sessions(cursor)
