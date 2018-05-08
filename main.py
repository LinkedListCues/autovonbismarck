import requests, json, os, gc, shutil, pickle, csv, random
from tester import TestRunner
from grader import Grader
from canvas import *
from pprint import pprint
import argparse


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

	return submissions

def CalculateLatePenalties():
	print('Calculating late penalties...')
	extensions = []
	with open('./sandbox/info/extensions.csv') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			netid = row[4].lower()
			netid2 = row[5].lower()
			if netid != netid2: continue
			extensions.append(netid.lower)

	# allow for off by two errors, because we don't trust python
	for submission in submissions.values():
		hours_late = int(submission.seconds_late) / 3600
		if hours_late <= 2: continue
		if hours_late <= 50 and submission.netid in extensions: continue
		submission.late_penalty = 0.3 if hours_late <= 170 else 1


# if __name__ == '__main__':
# 	config = CanvasConfig('config.json')

# 	# download everyone
# 	submissions = LoadRoster(config)
# 	submissions_count = str(len(submissions))

# 	ind = 0
# 	for submission in submissions.values():
# 		ind += 1
# 		print(str(ind) + '\tof  ' + submissions_count)
# 		prep = Preparer(config, submission)
# 		prep.Prepare()
# 	gc.collect()

# 	# calculate late penalties for everyone
# 	CalculateLatePenalties()

# 	# build and test
# 	tester = TestRunner(config, 'Assignment1.dll', 'QueueTests.dll')

# 	ind = 0
# 	for submission in submissions.values():
# 		ind += 1
# 		print(submission.submission_id + ' - ' + str(ind) + '\tof  ' + submissions_count)

# 		# build it
# 		result = tester.BuildStudentDLL(submission.directory, submission.submission_id)
# 		if not result[0]:
# 			submission.invalid = True
# 			continue # bail out
		
# 		# test it
# 		result = tester.RunTests(submission)
# 		if not result[0]: 
# 			submission.invalid = True
# 			continue # bail out

# 	# calculate grades
# 	grader = Grader(config)
# 	print('Grading all submissions...')
# 	for submission in submissions.values():
# 		grader.Grade(submission)

# 	# upload grades and comments
# 	for submission in submissions.values():
# 		submission.UploadResults(config)

def LoadConfig(config_file):
	print('Loading config from ' + config_file + '...')
	with open(config_file,'r') as json_file:
		output = json.load(json_file)
		config = CanvasConfig(output)
	pprint(output)

		
def Run(args):
	if args.clean:
		return

	LoadConfig(args.config)


parser = argparse.ArgumentParser(description='Download, build, test, and grade studnets\' C# submissions. Made for EECS 214.')
parser.add_argument(
	'--config',
	type=str,
	nargs=1,
	help='The .json file to use as a configuration for this run. Defaults to "./config.json."',
	default='./config.json')

parser.add_argument(
	'--test',
	type=bool,
	nargs=1,
	help='Do a dry run of the process. Run every step except uploading. Print out the results at the end.',
	default=False)

parser.add_argument(
	'--clean',
	type=bool,
	nargs=1,
	help='Clear out everything in the sandbox directory, then rebuild it from scratch.',
	default=False)

args = parser.parse_args()
Run(args)