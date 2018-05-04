import requests, json
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
	def __init__(self):
		super(Submission, self).__init__()
		self.submission_id = '12546345'
		self.directory = './12546345'


if __name__ == '__main__':
	submission = Submission()

	config = CanvasConfig('config.json')
	tester = TestRunner(config, 'Assignment1.dll', 'QueueTests.dll')
	tester.RunTests(submission)
	# overlord = Overlord(config)
	# overlord.PrepareSubmissions()
	# overlord.PrepareTestables()
	# overlord.RunTests()