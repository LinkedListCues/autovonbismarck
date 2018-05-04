import requests, json, os, gc
from pprint import pprint
from tester import TestRunner

# set up configuration
# get all of the submissions as json
# 	try to serialize things out so that we don't have to do this bit too often
#	set up student representations
# iterate over each submission, running the test framework and recording the results
# collate all of the results
# generate grades and comments for each student
# 	late penalties; extensions
# upload grades and comments for each student

class CanvasConfig(object):
	"""Container class for the configuration. Holds a bunch of the important
	stuff that needs to be passed around."""
	def __init__(self, filename):
		super(CanvasConfig, self).__init__()
		with open(filename, 'r') as json_file:
			self._json = json.load(json_file)

		self.mstest_path = self._json['test_path']
		assert self.mstest_path, 'Missing MSTest.exe path.'
		self.msbuild_path = self._json['build_path']
		assert self.msbuild_path, 'Missing MSBuild.exe path.'

class Submission(object):
	"""Container class for holding submission information, including id,
	seconds_late, and the directory in which the relevant files are stored"""
	def __init__(self, spoof):
		super(Submission, self).__init__()
		self.submission_id = spoof
		self.directory = os.path.join('./test', spoof)

		self.success = True
		self.explanation = ''
		self.comment = ''

	def UpdateExplanation(self, result):
		self.success = result[0]
		self.explanation = result[1]

	def SetComment(self, comment):
		self.comment = comment


def MaybeDownloadAll():
	if not DOWNLOAD_ALL: return
	print('Downloading all projects...')


def MakeRoster():
	results = {}
	paths = os.listdir('./test/')
	for directory in paths:
		submission = Submission(directory)
		results[directory] = submission
	return results


def MaybeBuildAll(submissions):
	if not BUILD_ALL: return
	print('Building all projects...')
	count = str(len(submissions))
	ind = 0
	for submission in submissions.values():
		ind += 1
		print(submission.submission_id + ' - ' + str(ind) + '\tof  ' + count, end=' ')
		result = tester.BuildStudentDLL(submission.directory, submission.submission_id)
		
		if not result[0]:
			submission.UpdateExplanation(result)
			print(result[1])
		else: print()

		
def MaybeRunTests(submissions):
	if not RUN_TESTS: return
	print('Running all tests...')
	count = str(len(submissions))
	ind = 0
	for submission in submissions.values():
		if not submission.success: continue # already failed

		ind += 1
		print(submission.submission_id + ' - ' + str(ind) + '\tof  ' + count, end=' ')
		result = tester.RunTests(submission)
		
		if not result[0]:
			submission.UpdateExplanation(result)
			print(result[1])
		else: print()


BUILD_ALL = False
RUN_TESTS = True
if __name__ == '__main__':
	config = CanvasConfig('config.json')
	tester = TestRunner(config, 'Assignment1.dll', 'QueueTests.dll')

	submissions = MakeRoster()
	
	count = str(len(submissions))
	ind = 0
	for submission in submissions.values():
		ind += 1
		print(submission.submission_id + ' - ' + str(ind) + '\tof  ' + count, end=' ')

		# build it
		result = tester.BuildStudentDLL(submission.directory, submission.submission_id)
		if not result[0]:
			submission.UpdateExplanation(result)
			print(result[1])
		else: print()
		
		# test it
		if not submission.success: continue # already failed
		result = tester.RunTests(submission)
		if not result[0]:
			submission.UpdateExplanation(result)
			print(result[1])
			continue

		

	# MaybeBuildAll(submissions)
	# gc.collect()
	# MaybeRunTests(submissions)
	# gc.collect()

	# tester.RunTests(submission)
	# overlord = Overlord(config)
	# overlord.PrepareSubmissions()
	# overlord.PrepareTestables()
	# overlord.RunTests()