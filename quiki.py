# coding: utf-8
import sys

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
	for result in results:
		print '-', result['definition'].strip()

def main():
	puts = sys.stdout.write

	puts('Loading search engine, please wait... ')
	engine = SearchEngine()
	engine.load('TEMP-E20131002.tsv')
	puts('done.\n')

	repl = REPL(engine.search, display_results)
	repl.start()


if __name__ == '__main__':
	main()
