"""
Builds native html and css files for website:
* html files are built from fragments
* css files are compiled from .scss
"""

import os
# not OOTB: requires 'pip install pyScss'
from scss.compiler import compile_string
import sys


CSS_OUTPUT_FILENAME = 'css/main.css'
CSS_INCLUDE_EXTENSIONS = ['.css', '.scss']
SCSS_DIR = 'css/scss'


def all():
	build_css()
	build_html()


def build_css():
	scss_fragments = []

	for filename in sorted(os.listdir(SCSS_DIR)):
		if any(filename.endswith(ext) for ext in CSS_INCLUDE_EXTENSIONS):
			with open(os.path.join(SCSS_DIR, filename), 'r') as readfile:
				scss_fragments.append(readfile.read())

	scss = '\n'.join(scss_fragments)

	css = compile_string(scss)

	with open(CSS_OUTPUT_FILENAME, 'w') as outfile:
		outfile.write(trim_css(css))


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


def trim_css(css_string):
	lines = []

	for line in css_string.splitlines():
		lines.append(line.strip())

	return '\n'.join(lines)


if __name__ == '__main__':
	main(sys.argv[1:])
