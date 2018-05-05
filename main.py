import requests, json, os, gc, shutil, pprint, pickle
from tester import TestRunner
from grader import Grader
from canvas import *


def LoadRoster(goal_path='./sandbox/info/students.pickle'):
	if os.path.isfile(goal_path):
		print('Unpickling roster.')
		with open(goal_path, 'rb') as pickle_file:
			submissions = pickle.load(pickle_file)
	else:
		print('Making roster and pickling.')
		fetcher = SubmissionFetcher(config)
		fetcher.FetchSubmissions()
		submissions = fetcher.submissions
		with open(goal_path, 'wb') as pickle_file:
			pickle.dump(submissions, pickle_file)

	return submissions


if __name__ == '__main__':
	config = CanvasConfig('config.json')

	# download everyone
	submissions = LoadRoster()
	submissions_count = str(len(submissions))

	ind = 0
	for submission in submissions.values():
		ind += 1
		print(str(ind) + '\tof  ' + submissions_count)
		prep = Preparer(config, submission)
		prep.Prepare()
	gc.collect()


	# build and test
	tester = TestRunner(config, 'Assignment1.dll', 'QueueTests.dll')

	ind = 0
	for submission in submissions.values():
		ind += 1
		print(submission.submission_id + ' - ' + str(ind) + '\tof  ' + submissions_count)

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
	grader = Grader(config)
	for submission in submissions.values():
		print('Grading all submissions...')
		grader.Grade(submission)

	# upload grades and comments
	for submission in submissions.values():
		submission.UploadResults(config)