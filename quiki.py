# coding: utf-8
import sys
import urwid


class SearchEngine(object):
	def __init__(self):
		self.db = {}

	def parse_line(self, line):
		parts = line.split('\t')
		result = {
			'expression': parts[1],
			'section': parts[2],
			'definition': parts[3]
		}
		return result

	def load(self, filename):
		parseln = self.parse_line

		with open(filename, 'r') as f:
			for line in f:
				parsed_line = parseln(line)
				expr = parsed_line['expression']
				if expr in self.db:
					self.db[expr].append(parsed_line)
				else:
					self.db[expr] = [parsed_line]

	def search(self, expr):
		return self.db[expr] if expr in self.db else []


class REPL(object):
	def __init__(self, input_cb, output_cb):
		self.input_cb = input_cb
		self.output_cb = output_cb

	def start(self):
		print 'REPL starting: type Ctrl+D (EOF) to exit.\n'

		while True:
			try:
				input_str = raw_input('> ')
				out = self.input_cb(input_str)
				self.output_cb(out)
			except EOFError:
				print 'EOF detected. Terminating...\n'
				return


def display_results(results):
	tab = '  '

	if len(results) == 0:
		print '\n', tab, 'Sorry, no results :(\n'
		return

	expr = results[0]['expression']
	num_results = len(results)
	print '\n{}"{}" ~ {} results\n'.format(tab, expr, num_results)
	for result in results:
		defn = result['definition'].strip()
		sect = result['section'].strip()
		print '{}({}) {}'.format(tab, sect.lower(), defn)
	print ''

def main_simple():
	"""
	Simple 'REPL-like' search.
	"""
	puts = sys.stdout.write

	puts('Loading search engine, please wait... ')
	engine = SearchEngine()
	engine.load('TEMP-E20131002.tsv')
	puts('done.\n')

	repl = REPL(engine.search, display_results)
	repl.start()

def main_insta():
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
	    reply.set_text(('I say', u"Please wait...\n")) 
	    reply.set_text(('I say', u"Nice to meet you, %s" % new_edit_text))

	def on_exit_clicked(button):
	    raise urwid.ExitMainLoop()

	urwid.connect_signal(ask, 'change', on_ask_change)
	urwid.connect_signal(button, 'click', on_exit_clicked)

	urwid.MainLoop(top, palette).run()


if __name__ == '__main__':
	if len(sys.argv) == 2:
		if sys.argv[1] == 'simple':
			main_simple()
		else:
			main_insta()
	else:
		print 'Wrong number of arguments!'
