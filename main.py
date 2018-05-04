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

def MaybeDownloadAll():
	if not DOWNLOAD_ALL: return
	print('Downloading all projects...')

def MaybeBuildAll():
	if not BUILD_ALL: return
	print('Building all projects...')
	paths = os.listdir('./test/')
	count = str(len(paths))
	ind = 0
	for directory in paths:
		ind += 1
		submission = Submission(directory)
		print(submission.submission_id + ' - ' + str(ind) + '\tof\t' + count, end=' ')
		tester.BuildStudentDLL(submission.directory, submission.submission_id)
		print()
		
def MaybeRunTests():
	if not RUN_TESTS: return
	print('Running all tests...')
	paths = os.listdir('./test/')
	count = str(len(paths))
	ind = 0
	for directory in paths:
		ind += 1
		print(str(ind) + '\tof\t'+ count, end=' ')
		submission = Submission(directory)
		tester.RunTests(submission)

BUILD_ALL = True
RUN_TESTS = False
if __name__ == '__main__':
	config = CanvasConfig('config.json')
	tester = TestRunner(config, 'Assignment1.dll', 'QueueTests.dll')

	MaybeBuildAll()
	gc.collect()
	

	# tester.RunTests(submission)
	# overlord = Overlord(config)
	# overlord.PrepareSubmissions()
	# overlord.PrepareTestables()
	# overlord.RunTests()