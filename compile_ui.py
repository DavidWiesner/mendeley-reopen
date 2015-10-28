#!/usr/bin/env python2.7
from glob import glob
import os

from PyQt4.uic import compileUi


def ui():
	for uifile in glob("mendeleyreopen/ui/*.ui"):
		pyfile = os.path.splitext(uifile)[0] + ".py"
		# if outdated(pyfile, uifile):
		print(uifile)
		pyfile = open(pyfile, "wt", encoding="utf-8")
		uifile = open(uifile, "rt", encoding="utf-8")
		compileUi(uifile, pyfile, from_imports=True)


if __name__ == "__main__":
	ui()

