class Grader(object):
	"""Grades stuff. Go, 'Cats."""
	def __init__(self):
		super(Grader, self).__init__()

	def Grade(self, submission):
		if submission.invalid:
			submission.grade = 0
			return

		comment_file = submission.comment_file
		# self.CleanResults(comment_file)
		grade = self.CalculateResults(comment_file)
		submission.grade = int((1.0 - submission.late_penalty) * grade)


	# TODO this feels shitty [at least the shittiness is well-hidden - Ethan]
	def CalculateResults(self, comment_file):
		passed = failed = 0
		in_error = False
		with open(comment_file, 'r') as stream:
			lines = [line.strip() for line in stream.readlines()]
		for line in lines:
			if line.startswith('Correctas'): passed += 1
			elif line.startswith('Con error'): failed += 1

		total = float(passed + failed)
		value = passed / total
		value = int(100.0 * value)
		return value