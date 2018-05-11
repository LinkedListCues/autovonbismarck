import subprocess, os, glob, shutil, pprint

TESTBED_PATH='./sandbox/testbed'
TRIE_PATH='./sandbox/testbed/Trie'
TRIETESTS_PATH='sandbox\\\\testbed\\\\TrieTests\\\\bin\\\\Debug\\\\netcoreapp2.0\\\\'

class TestRunner(object):
	"""Builds a student's project; then runs unit tests on it.
	Grading is handled elsewhere, though - nota bene."""

	def __init__(self, config):
		super(TestRunner, self).__init__()

		self._mstest = '"' + config.mstest_path + '"'
		self._msbuild = '"' + config.msbuild_path + '"'
		self._test_string = self._mstest + ' ' + TRIETESTS_PATH + 'TrieTests.dll'


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



	def Run(self, submission):
		print('Running tests for ' + str(submission.submission_id))
		search_directory = submission.directory
		# if len(os.listdir(search_directory)) == 0:
		# 	return self.MakeFailureExplanation(submission.submission_id, './results', 'Nothing submitted.')

		filename = os.path.join('./results', submission.submission_id + '_output')
		if os.path.exists(filename):
			print('Already run.')
			return # assume that we got it right the first time

		self.ClearFiles()
		self.CopyFiles(search_directory)
		self.BuildSolution()
		self.RunAllTests(filename)

	def ClearFiles(self):
		magic_dir =  TRIE_PATH
		files = os.listdir(magic_dir)
		for f in files:
			if f.endswith('.cs'): os.remove(os.path.join(magic_dir, f))

	# TODO fixme to be general
	def CopyFiles(self, search_directory):
		files = os.listdir(search_directory)
		for f in files:
			if f.endswith('.cs'):
				src = os.path.join(search_directory, f)
				dst = os.path.join(TRIE_PATH, f)
				shutil.copyfile(src, dst)

	def BuildSolution(self):
		# results = glob.glob(search_directory + '/**/*.csproj', recursive=True)
		query = os.path.join(TESTBED_PATH,'*.sln')
		results = glob.glob(query)
		target = None
		if results: target = results[0]  # here's hoping that they have only one .csproj

		if not target: return
		buildpath = self._msbuild + ' "' + target + '"'
		output = subprocess.Popen(buildpath, stdout=subprocess.PIPE, shell=True).stdout.read()


	def RunAllTests(self, filename):
		output = subprocess.Popen(self._test_string, stdout=subprocess.PIPE, shell=True).stdout.read()
		print('Writing output to file: ' + filename)
		with open(filename, 'wb') as output_file:
			output_file.write(output)
