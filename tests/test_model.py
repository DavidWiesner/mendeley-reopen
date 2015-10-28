from mendeleyreopen.model import Document, Session

__author__ = 'david'

import unittest


class MyTestCase(unittest.TestCase):
	def test_document_uri_none(self):
		doc = Document()
		self.assertIsNone(doc.get_uri())
		doc = Document("uuid")
		self.assertEqual(Document._base_uri % "uuid", doc.get_uri())
		doc = Document("uuid", "remoteuuid")
		self.assertEqual(Document._base_uri % "remoteuuid", doc.get_uri())
		doc = Document(None, "remoteuuid")
		self.assertEqual(Document._base_uri % "remoteuuid", doc.get_uri())

	def test_add_doc(self):
		session = Session()
		uuid = 'uuid'
		doc = Document(uuid)

		session.add_document(doc)
		session.add_document(doc)

		self.assertIn(doc, session.documents)
		self.assertEqual(1, len(session.documents), "test: added only once")
		self.assertEqual(1, session.size, "test: added only once")

	def test_mark_closed(self):
		session = Session()
		doc = Document('deluuid')

		session.mark_closed(doc)
		session.add_document(doc)
		session.add_document(Document("uuid"))

		self.assertNotIn(doc, session.documents)

	def test_session_empty(self):
		doc = Document("uuid")
		session = Session()

		self.assertTrue(session.is_empty())

		session.add_document(doc)

		self.assertFalse(session.is_empty())

if __name__ == '__main__':
	unittest.main()
