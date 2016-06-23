"""
Builds native html and css files for website:
* html files are built from fragments
* css files are compiled from .scss
"""

# not OOTB: requires 'pip install libsass'
import libsass
import sys


def all():
	build_css()
	build_html()


def build_css():
	# TODO


def build_html():
	# TODO


def main(arguments):
	if not arguments or arguments[0] == 'all':
		all()
	elif arguments[0] == 'css':
		build_css()
	elif arguments[0] == 'html':
		build_html()
	else:
		print('Invalid command: ' + str(arguments))

if __name__ == "__main__":
	main(sys.argv[1:])

