"""
Builds native html and css files for website:
* html files are built from .shtml fragments
* a main.css file is compiled from .scss fragments

When run from the command line:
* Legal commands are 'all', 'css', and 'html'.
* 'all' runs both 'css' and 'html'.
* Running build.py without a command defaults to 'all'.
* Any other command yields an error.

When imported as a module:
* The 'main' function can be run with arguments as above.
* Helper functions also exist for each piece of functionality above.
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
	for filename in os.listdir(HTML_FRAGMENT_DIR):
		if not filename.startswith(HTML_FRAGMENT_EXCLUDE_PREFIX):
			with open(os.path.join(HTML_FRAGMENT_DIR, filename), 'r') as readfile:
				contents = do_ssi(readfile.read())

			with open(filename.replace('.shtml', '.html'), 'w') as outfile:
				outfile.write(contents)


def do_ssi(contents):
	newline_pattern = re.compile('\n+')
	pattern = re.compile(HTML_FRAGMENT_REGEX)
	contents = pattern.sub(replace_with_shtml, contents)
	return newline_pattern.sub('\n', contents)


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
		return do_ssi(subfile.read())


def trim_css(css_string):
	lines = []

	for line in css_string.splitlines():
		lines.append(line.strip())

	return '\n'.join(lines)


if __name__ == '__main__':
	main(sys.argv[1:])
