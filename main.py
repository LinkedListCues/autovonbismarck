import requests, json, os, gc, shutil
from pprint import pprint
from tester import TestRunner
from grader import Grader

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
		self.total_tests = self._json['total_tests']

class Submission(object):
	"""Container class for holding submission information, including id,
	seconds_late, and the directory in which the relevant files are stored"""
	def __init__(self, spoof):
		super(Submission, self).__init__()
		self.submission_id = spoof
		self.directory = os.path.join('./test', spoof)
		self.comment_file = os.path.join('./results', spoof + '_output')
		self.invalid = False
		self.grade = 0


def MakeRoster():
	results = {}
	paths = os.listdir('./test/')[:10]
	for directory in paths:
		submission = Submission(directory)
		results[directory] = submission
	return results


if __name__ == '__main__':
	config = CanvasConfig('config.json')
	tester = TestRunner(config, 'Assignment1.dll', 'QueueTests.dll')
	grader = Grader(config)

	submissions = MakeRoster()
	
	count = str(len(submissions))
	ind = 0
	for submission in submissions.values():
		ind += 1
		print(submission.submission_id + ' - ' + str(ind) + '\tof  ' + count)

		# build it
		result = tester.BuildStudentDLL(submission.directory, submission.submission_id)
		if not result[0]:
			submission.invalid = True
			continue # bail out
		
		# test it
		result = tester.RunTests(submission)
		if not result[0]: 
			submission.invalid = True
			continue # bail out

	for submission in submissions.values():
		grader.Grade(submission)
		print(submission.grade)


	# tester.RunTests(submission)
	# overlord = Overlord(config)
	# overlord.PrepareSubmissions()
	# overlord.PrepareTestables()
	# overlord.RunTests()