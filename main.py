import requests, json, os, gc, shutil, pickle, csv, random
from tester import TestRunner
from grader import Grader
from canvas import *
from pprint import pprint
import argparse

# yay, magic constants
SANDBOX_DIR='./sandbox'
INFO_DIR=SANDBOX_DIR+'/info'
SUBMISSIONS_DIR=SANDBOX_DIR+'/submissions'
TESTBED_DIR=SANDBOX_DIR+'/testbed'
RESULTS_DIR=SANDBOX_DIR+'/results'


# if __name__ == '__main__':
# 	config = CanvasConfig('config.json')

# 	# download everyone
# 	submissions = LoadRoster(config)
# 	submissions_count = str(len(submissions))

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

def CleanAll():
	print('Deleting all of ' + SANDBOX_DIR)
	shutil.rmtree(SANDBOX_DIR)
def MakeAll():
	print('Remaking ' + SANDBOX_DIR, ', ' + INFO_DIR + ', and ' + SUBMISSIONS_DIR)
	os.makedirs(INFO_DIR, exist_ok=True)
	os.makedirs(SUBMISSIONS_DIR, exist_ok=True)
	os.makedirs(TESTBED_DIR, exist_ok=True)
	print()

def LoadConfig(config_file):
	print('Loading config from ' + config_file)
	with open(config_file,'r') as json_file:
		output = json.load(json_file)
		config = CanvasConfig(output)
	pprint(output)
	print()
	return config

def LoadRoster(config, goal_path):
	if os.path.isfile(goal_path):
		print('Unpickling roster from ' + goal_path)
		with open(goal_path, 'rb') as pickle_file:
			submissions = pickle.load(pickle_file)
	else:
		print('Making roster and pickling to ' + goal_path)
		fetcher = SubmissionFetcher(config)
		fetcher.FetchSubmissions()
		submissions = fetcher.submissions
		with open(goal_path, 'wb') as pickle_file:
			pickle.dump(submissions, pickle_file)

	return submissions

def PrepareSubmissions(config, submissions, no_zip):
	count = str(len(submissions))
	for ind, submission in enumerate(submissions.values()):
		print(str(ind + 1) + '\tof  ' + count)
		prep = Preparer(config, submission, SUBMISSIONS_DIR)
		prep.Prepare(no_zip)

def CalculateLatePenalties(submissions):
	print('Calculating late penalties\n')
	# allow for off by two errors, because we don't trust python
	# also, just give everyone the goddamn extension, because we get things like 197/208 students going for it anyway
	for submission in submissions.values():
		hours_late = int(submission.seconds_late) / 3600
		if hours_late <= 50: continue
		submission.late_penalty = 0.3 if hours_late <= 170 else 1

def RunAllTests(config, submissions):
	tester = TestRunner(config)
	count = str(len(submissions))
	for ind, submission in enumerate(submissions.values()):
		print(str(ind + 1) + ' of ' + count) 
		tester.Run(submission)

def GradeSubmissions(config, submissions):
	grader = Grader()
	for submission in submissions.values(): grader.Grade(submission)

def UploadResults(submissions, comments):
	for submission in submissions.values(): submission.Upload(comments)

def Run(args):
	if not os.path.isdir(INFO_DIR) or not os.path.isdir(SUBMISSIONS_DIR):
		MakeAll()
	if args.clean:
		CleanAll()
		MakeAll()
		return

	config = LoadConfig(args.config)
	submissions = LoadRoster(config, INFO_DIR+'/students.pickle')
	PrepareSubmissions(config, submissions, args.single_file)
	CalculateLatePenalties(submissions)
	RunAllTests(config, submissions)
	GradeSubmissions(config, submissions)
	UploadResults(submissions, args.comments)


parser = argparse.ArgumentParser(description='Download, build, test, and grade studnets\' C# submissions. Made for EECS 214.')

parser.add_argument(
	'--config',
	type=str,
	nargs=1,
	help='The .json file to use as a configuration for this run. Defaults to "./config.json."',
	default='./config.json')

parser.add_argument(
	'--clean',
	action='store_const',
	const=True, default=False,
	help='Clear out everything in the sandbox directory, then rebuild it from scratch.')

parser.add_argument(
	'--single-file',
	action='store_const',
	const=True,default=False,
	help='Used for when the users submit only a single .cs file. Skips the unzipping step.')

parser.add_argument(
	'--test',
	type=bool,
	help='Do a dry run of the process. Run every step except uploading. Print out the results at the end.',
	default=False)

parser.add_argument(
	'--comments',
	action='store_const',
	const=True, default=False,
	help='Add comments to the upload. Used in the final steps')


args = parser.parse_args()
Run(args)