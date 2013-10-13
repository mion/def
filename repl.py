class REPL(object):
	def __init__(self, callback):
		self.callback = callback

	def start(self):
		print 'REPL starting: type Ctrl+D (EOF) to exit.\n'

		while True:
			try:
				input_str = raw_input('> ')
				self.callback(input_str)
			except EOFError:
				print 'EOF detected, exit!\n'
				return
