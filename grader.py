class Grader(object):
	"""Grades stuff. Go, 'Cats."""
	def __init__(self, config):
		super(Grader, self).__init__()
		self._config = config
		self._total_tests = config.total_tests

	def Grade(self, submission, late_penalty=0):
		if submission.invalid:
			submission.grade = 0
			return

		comment_file = submission.comment_file
		self.CleanResults(comment_file)
		grade = self.CalculateResults(comment_file)
		submission.grade = (1.0 - late_penalty) * grade
		
	
	def CleanResults(self, comment_file):
		# TODO this is stinky
		with open(comment_file, 'r') as stream:
			lines = [line for line in stream.readlines()]
			lines = lines[3:]
			lines = lines[:-2]

		with open(comment_file, 'w') as stream:
			for line in lines:
				stream.write(line)


	# TODO this feels shitty [at least the shittiness is well-hidden - Ethan]
	def CalculateResults(self, comment_file):
		with open(comment_file, 'r') as stream:
			lines = [line.strip() for line in stream.readlines()]
			split_point = 0
			for i, line in enumerate(lines):
				if 'Resumen' in line: split_point = i
			for line in lines[split_point:]:
				if 'Pasada' not in line: continue
				count = int(line.split()[1])

			total = int(lines[-1].split()[1])

			assert total == self._total_tests, 'Different count for total tests?!'

			return float(count) / float(total) * 100.0
