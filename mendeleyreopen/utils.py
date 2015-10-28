import subprocess
import os
import sys


def find_mendeley_db_file():
	import glob
	from appdirs import user_data_dir
	data_dir = os.path.join(user_data_dir("data"), 'Mendeley Ltd.', "Mendeley Desktop")
	files = glob.glob(data_dir + '/*@www.mendeley.com.sqlite')
	return files[0] if len(files) > 0 else None


def fileopen(filepath):
	if sys.platform.startswith('darwin'):
		subprocess.call(('open', filepath))
	elif os.name == 'nt':
		os.startfile(filepath)
	elif os.name == 'posix':
		fnull = open(os.devnull, 'w')
		subprocess.call(['xdg-open', filepath], stdout=fnull, stderr=subprocess.STDOUT)
