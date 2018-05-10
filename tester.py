import subprocess, os, glob, shutil

class TestRunner(object):
	"""Builds a student's project; then runs unit tests on it.
	Grading is handled elsewhere, though - nota bene."""

	def __init__(self, config, assignment_dll, test_dll):
		super(TestRunner, self).__init__()

		self._mstest = '"' + config.mstest_path + '"'  # this is kind of yikes, but, sigh
		self._msbuild = '"' + config.msbuild_path + '"'

		self._assignment_dll = assignment_dll
		self._test_dll = test_dll

		self._test_string = self._mstest + ' ' + self._test_dll


	def RunTests(self, submission):
		result = self.PrepareStudentDLL(submission, self._assignment_dll)
		if not result[0]: return result

		os.chdir('./sandbox')

		print('Running unit tests for submission: \t' + submission.submission_id)
		output = subprocess.Popen(self._test_string, stdout=subprocess.PIPE, shell=True).stdout.read()

		self.ExportOutput(submission.submission_id, output, '../results')
		os.chdir('./..')

		return (True, None)


	def ExportOutput(self, submission_id, output, target_directory, as_string=False):
		filename = os.path.join(target_directory, submission_id + '_output')
		print('Writing output for ' + submission_id + ' to file: ' + filename)
		if as_string:
			with open(filename, 'w') as output_file:
				output_file.write(output)
		else:
			with open(filename, 'wb') as output_file:
				output_file.write(output)

			


	# TODO this needs clean-up hard to follow
	# uses functions with hella side effects
	def BuildStudentDLL(self, search_directory, submission_id):
		if len(os.listdir(search_directory)) == 0:
			return self.MakeFailureExplanation(submission_id, './results', 'Nothing submitted.')

		results = glob.glob(search_directory + '/**/*.csproj', recursive=True)
		
		# TODO useful checks?
		target = None
		if results: target = results[0]  # here's hoping that they have only one .csproj

		if not target:
			return self.MakeFailureExplanation(submission_id, './results', 'No .csproj file found in your directory.')

		buildpath = self._msbuild + ' "' + target + '"'
		output = subprocess.Popen(buildpath, stdout=subprocess.PIPE, shell=True).stdout.read()

		output = str(output)
		if '0 Errores' not in output: # TODO lol hard-coded
			return self.MakeFailureExplanation(submission_id, './results', 'Project compiled with errors.')

		return (True, None)


	def PrepareStudentDLL(self, submission, assignment, sandbox_dir='sandbox/'):
		goal_path = os.path.join(sandbox_dir, assignment)
		# if os.path.isfile(goal_path): os.remove(goal_path)

		path = self.FindAssignmentDLLPath(submission.directory, assignment)
		if not path:
			return self.MakeFailureExplanation(submission.submission_id, './results', 'No assignment dll of the appropriate name found after build')

		shutil.copy(path, goal_path)
		return (True, None)

	
	def FindAssignmentDLLPath(self, directory, assignment_name):
		results = glob.glob(directory + '/**/' + assignment_name, recursive=True)
		if results: return results[0]
		return None

	def MakeFailureExplanation(self, submission_id, output_directory, explanation_string):
		self.ExportOutput(submission_id, explanation_string, output_directory, True)
		return (False, explanation_string)