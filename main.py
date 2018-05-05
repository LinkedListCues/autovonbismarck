import requests, json, os, gc, shutil, pickle, csv, random
from tester import TestRunner
from grader import Grader
from canvas import *
from pprint import pprint


def LoadRoster(config, goal_path='./sandbox/info/students.pickle'):
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

	# dummy = []
	# for v in submissions.values():
	# 	dummy.append(v)
	# random.shuffle(dummy)
	# dummy = dummy[:2]
	# submissions = {}
	# for d in dummy:
	# 	submissions[d.submission_id] = d

	return submissions


if __name__ == '__main__':
	config = CanvasConfig('config.json')

	# url = "https://canvas.northwestern.edu/api/v1/courses/72859/assignments/458956/submissions/64485"
	# r = requests.put(url, params={ 'access_token': config.api_key, 'submission[posted_grade]': '90.0' } )
	# pprint(r.json())

	# download everyone
	submissions = LoadRoster(config)
	submissions_count = str(len(submissions))

	ind = 0
	for submission in submissions.values():
		ind += 1
		print(str(ind) + '\tof  ' + submissions_count)
		prep = Preparer(config, submission)
		prep.Prepare()
	gc.collect()

	# calculate late penalties for everyone
	print('Calculating late penalties...')
	extensions = []
	with open('./sandbox/info/extensions.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			netid = row[4]
			netid2 = row[5]
			if netid != netid2: continue
			extensions.append(netid)

	for submission in submissions.values():
		hours_late = int(submission.seconds_late) / 3600
		if hours_late <= 0: continue
		if hours_late <= 48 and submission.netid in extensions: continue
		submission.late_penalty = 0.3 if hours_late < 168 else 1

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

	# calculate grades
	grader = Grader(config)
	print('Grading all submissions...')
	for submission in submissions.values():
		grader.Grade(submission)

	# upload grades and comments
	for submission in submissions.values():
		submission.UploadResults(config)