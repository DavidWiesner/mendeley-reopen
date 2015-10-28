__author__ = 'David Wiesner'


class Session:
	def __init__(self, ended=None, documents=None, started=None):
		self.started = started
		self.documents = [] if documents is None else documents
		self.ended = ended
		self._mark_closed = {}
		self._mark_added = {}

	def is_empty(self):
		return len(self.documents) == 0

	def add_document(self, document):
		if document.uuid not in self._mark_closed and document.uuid not in self._mark_added:
			self._mark_added[document.uuid] = 1
			return self.documents.append(document)

	def mark_closed(self, uuid_or_document):
		if isinstance(uuid_or_document, Document):
			self._mark_closed[uuid_or_document.uuid] = 1
		else:
			self._mark_closed[uuid_or_document] = 1

	@property
	def size(self):
		return len(self.documents)


class Document:
	_base_uri = 'mendeley://library/document/%s'

	def __init__(self, uuid=None, remote_uuid=None, title=None, access=None, filehash=None):
		super().__init__()
		self.uuid = uuid
		self.remote_uuid = remote_uuid
		self.title = title
		self.access = access
		self.filehash = filehash

	def get_uri(self):
		uuid = self.remote_uuid if self.remote_uuid is not None else self.uuid
		return self._base_uri % uuid if uuid is not None else None

	def __hash__(self):
		return hash(self.uuid)

	def __str__(self):
		return "Document<%s,%s,%s,%s>" % (self.uuid, self.remote_uuid, self.title, self.access)
