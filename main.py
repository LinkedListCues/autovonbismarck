import requests, json, os, gc, shutil, pprint, pickle
from tester import TestRunner
from grader import Grader
from canvas import *


def MakeRoster():
	results = {}
	paths = os.listdir('./sandbox/submissions/')[:1]
	for directory in paths:
		submission = Submission(directory)
		results[directory] = submission
	return results


def LoadRoster(goal_path='./sandbox/info/students.pickle'):
	if os.path.isfile(goal_path):
		print('Unpickling roster.')
		with open(goal_path, 'rb') as pickle_file:
			submissions = pickle.load(pickle_file)
	else:
		print('Making roster and pickling.')
		submissions = MakeRoster()
		with open(goal_path, 'wb') as pickle_file:
			pickle.dump(submissions, pickle_file)

	return submissions


if __name__ == '__main__':
	config = CanvasConfig('config.json')
	tester = TestRunner(config, 'Assignment1.dll', 'QueueTests.dll')
	grader = Grader(config)

	# download everyone
	submissions = LoadRoster()

	# build and test
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
	
	# calculate late penalties for everyone
	for submission in submissions.values():
		continue

	# calculate grades
	for submission in submissions.values():
		print('Grading all submissions...')
		grader.Grade(submission)

	# upload grades and comments
	for submission in submissions.values():
		submission.UploadResults(config)