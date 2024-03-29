# coding: utf-8
import sys
import pickle
from collections import defaultdict

import urwid
import mwparserfromhell as mwparser

from repl import REPL

DUMP_FILENAME = 'TEMP-E20131002.tsv'


class SearchEngine(object):
	def __init__(self):
		self.db = defaultdict(lambda: [])

	def parseln(self, line):
		"""Parse a line from the tsv file."""
		tabs = line.split('\t')

		#parsed_defn = mwparser.parse(tabs[3][2:]) # [2:] to remove "# "
		parsed_defn = tabs[3]

		# tabs[0] is the language, "English"; we don't need it
		result = {
			'expression': tabs[1], #eg: cat
			'type': tabs[2], #eg: Noun
			'definition': parsed_defn #eg: "virtual feline of the interwebs"
		}
		return result

	def load(self, filename):
		with open(filename, 'r') as f:
			for line in f:
				try:
					parsed_line = self.parseln(line)
					expr = parsed_line['expression']
					self.db[expr].append(parsed_line)
				except Exception, e:
					print '[!] Failed to parse line: "{}"\nReason: {}'.format(line, str(e))

	def search(self, expr):
		return self.db[expr]

def format_results(results):
	tab = '  '

	if len(results) == 0:
		return '\n{}{}\n'.format(tab, 'No results.')

	arr = []
	expr = results[0]['expression']
	num_results = len(results)
	arr.append('\n{}"{}" ~ {} results\n'.format(tab, expr, num_results))
	for result in results:
		defn = result['definition'].strip()
		sect = result['type'].strip()
		arr.append('{}({}) {}'.format(tab, sect, defn))
	arr.append('')

	return '\n'.join(arr)

def display_results(results):
	print format_results(results)

def main_repl(engine):
	"""
	Simple REPL-like search.
	"""

	repl = REPL(lambda s: display_results(engine.search(s)))
	repl.start()

def main_insta(engine):
	"""
	Instant 'as-you-type' search.
	"""
	palette = [('I say', 'default,bold', 'default', 'bold'),]
	ask = urwid.Edit(('I say', u"Search: "))
	reply = urwid.Text(u"")
	button = urwid.Button(u'Exit')
	div = urwid.Divider()
	pile = urwid.Pile([ask, div, reply, div, button])
	top = urwid.Filler(pile, valign='top')

	def on_ask_change(edit, new_edit_text):
	    if len(new_edit_text) == 0:
	    	reply.set_text(('I say', 'Hey! Just start typing to get some answers.'))
	    	return

	    reply.set_text(('I say', u"Searching...\n")) 
	    results = engine.search(new_edit_text)
	    if len(results) > 0:
	    	reply.set_text(('I say', format_results(results)))
	    else:
	    	reply.set_text(('I say', u'No results for "{}"'.format(new_edit_text)))


	def on_exit_clicked(button):
	    raise urwid.ExitMainLoop()

	urwid.connect_signal(ask, 'change', on_ask_change)
	urwid.connect_signal(button, 'click', on_exit_clicked)

	urwid.MainLoop(top, palette).run()


if __name__ == '__main__':
	print 'def 0.0.1 (alpha ver., released Oct 12 2013)\n'

	if len(sys.argv) == 3:
		if sys.argv[1] == 'add':
			print 'Adding database "{}", please wait... '.format(sys.argv[2])
			SearchEngine.add(sys.argv[2]) #'TEMP-E20131002.tsv'
			print 'DB added successfully.'
	elif len(sys.argv) == 2:
		engine = SearchEngine()
		engine.load(DUMP_FILENAME)

		if sys.argv[1] == 'repl':
			main_repl(engine)
		else:
			main_insta(engine)

		print 'Unloading DB and terminating...'
	else:
		print 'Wrong number of arguments!'
