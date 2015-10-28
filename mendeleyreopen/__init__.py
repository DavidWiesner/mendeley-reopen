from .ui import Main
from .ui.table import *
from .db import *
from .utils import *


def main_ui():
	mendeley_database = find_mendeley_db_file()

	if not os.path.isfile(mendeley_database):
		sys.stderr.write('File "%s" does not exist\n' % mendeley_database)
		exit(1)
	main_view = None
	app = QtGui.QApplication(sys.argv)
	with MendeleyDB(mendeley_database) as mendeley_db:
		sessions = mendeley_db.get_last_opened_sessions()
		main_view = FilesTable(sessions)

	window = Main(main_view)
	window.show()
	sys.exit(app.exec_())


def main_no_ui():
	mendeley_database = find_mendeley_db_file()

	if not os.path.isfile(mendeley_database):
		sys.stderr.write('File "%s" does not exist\n' % mendeley_database)
		exit(1)
	
	with MendeleyDB(mendeley_database) as mendeley_db:
		sessions = mendeley_db.get_last_opened_sessions()
		if len(sessions) == 0:
			sys.stderr.write('No Session found in "%s"\n' % mendeley_database)
			exit(0)

		print("%d opened Files found to open" % sessions[0].size)
		for doc in sessions[0].documents:
			input("press enter to open '%s': " % doc.title)
			fileopen(doc.get_uri())

if __name__ == '__main__':
	main_ui()
