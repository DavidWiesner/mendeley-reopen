#!/usr/bin/python

from setuptools import setup

setup(name='mendeley-reopen',
      version='0.1.0',
      author='David Wiesner',
      packages=['mendeleyreopen', 'mendeleyreopen.ui'],
      license='GPLv3',
      install_requires=[
	      "appdirs",
#	      "pyqt4"
      ],
      data_files=[
	      ('share/applications', ['install/mendeley-reopen.desktop']),
      ],
      entry_points={
	      'gui_scripts': [
		      'mendeley-reopen = mendeleyreopen.__main__'
	      ]},
      )
