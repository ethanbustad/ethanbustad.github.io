"""
Builds native html and css files for website:
* html files are built from fragments
* css files are compiled from .scss
"""

import os
import re
# not OOTB: requires 'pip install pyScss'
from scss.compiler import compile_string
import sys


CSS_FRAGMENT_DIR = 'css/scss'
CSS_INCLUDE_EXTENSIONS = ['.css', '.scss']
CSS_OUTPUT_FILENAME = 'css/main.css'
HTML_FRAGMENT_DIR = 'html'
HTML_FRAGMENT_EXCLUDE_PREFIX = '_'
HTML_FRAGMENT_REGEX = '<!--#include virtual="(.+?)" -->'


def all():
	build_css()
	build_html()


def build_css():
	scss_fragments = []

	for filename in sorted(os.listdir(CSS_FRAGMENT_DIR)):
		if any(filename.endswith(ext) for ext in CSS_INCLUDE_EXTENSIONS):
			with open(os.path.join(CSS_FRAGMENT_DIR, filename), 'r') as readfile:
				scss_fragments.append(readfile.read())

	scss = '\n'.join(scss_fragments)

	css = compile_string(scss)

	with open(CSS_OUTPUT_FILENAME, 'w') as outfile:
		outfile.write(trim_css(css))


def build_html():
	pattern = re.compile(HTML_FRAGMENT_REGEX)
	newline_pattern = re.compile('\n+')

	for filename in os.listdir(HTML_FRAGMENT_DIR):
		if not filename.startswith(HTML_FRAGMENT_EXCLUDE_PREFIX):
			with open(os.path.join(HTML_FRAGMENT_DIR, filename), 'r') as readfile:
				contents = pattern.sub(replace_with_shtml, readfile.read())

			contents = newline_pattern.sub('\n', contents)

			outfilename = filename.replace('.shtml', '.html')

			with open(outfilename, 'w') as outfile:
				outfile.write(contents)


def main(arguments):
	if not arguments or arguments[0] == 'all':
		all()
	elif arguments[0] == 'css':
		build_css()
	elif arguments[0] == 'html':
		build_html()
	else:
		print('Invalid command: ' + str(arguments))


def replace_with_shtml(match):
	subfilename = match.group(1)

	with open(os.path.join(HTML_FRAGMENT_DIR, subfilename), 'r') as subfile:
		return subfile.read()


def trim_css(css_string):
	lines = []

	for line in css_string.splitlines():
		lines.append(line.strip())

	return '\n'.join(lines)


if __name__ == '__main__':
	main(sys.argv[1:])
