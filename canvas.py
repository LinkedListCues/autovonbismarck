import requests, os, shutil, zipfile, io, json

class CanvasConfig(object):
	"""Container class for Canvas configuration.
	Holds information like your API key as well as your course number."""
	def __init__(self, filename):
		super(CanvasConfig, self).__init__()

		with open(filename, 'r') as json_file:
			self._json = json.load(json_file)

		self.api_key = self._json['canvas_key']
		self.mstest_path = self._json['test_path']
		self.msbuild_path = self._json['build_path']
		self.total_tests = self._json['total_tests']

		self.course_id = self._json['course_id']
		self.assignment_id = self._json['assignment_id']
		self.base_url = self._json['base_url']

		self.payload = {'per_page':'100', 'access_token': self.api_key}


	def MakeURL(self, *argv):
		return self.base_url + '/'.join([str(arg) for arg in argv])

	def GetSubmissionsURL(self):
		return self.MakeURL(
			'courses', self.course_id,
			'assignments', self.assignment_id,
			'submissions')

	def GetNetid(self, user_id):
		url = self.MakeURL(
			'courses', self.course_id,
			'users', user_id)
		return self.GetJSON(url)['login_id']

	def GetJSON(self, URL, page=1):
		self.payload['page'] = str(page)
		r = requests.get(URL, params=self.payload)
		self.payload['page'] = str(1)
		return r.json()



class CanvasElement(object):
	"""A base class for things that use the Canvas config of a particular course."""
	def __init__(self, config):
		super(CanvasElement, self).__init__()
		self.config = config


class SubmissionFetcher(CanvasElement):
	"""Gets all of the submissions for a given assignment.
	Makes an instance of the Submission class for each one."""
	def __init__(self, config):
		super(SubmissionFetcher, self).__init__(config)
		self.submissions = {}

	def FetchSubmissions(self):
		print('Downloading all submissions...')
		url = self.config.GetSubmissionsURL()
		page = 1
		count = 0
		# iterate over all of the pages, stopping when the json is empty
		while(True):
			json = self.config.GetJSON(url, page)
			if not json: break
			for item in json:
				netid = self.config.GetNetid(json['user_id'])
				sub = Submission(item)
				self.submissions[sub.submission_id] = sub
			page += 1


class Submission(object):
	"""Container class for holding submission information, including id,
	seconds_late, and the directory in which the relevant files are stored"""
	def __init__(self, json):
		super(Submission, self, netid).__init__()
		self._json = json
		self.submission_id = str(json['id'])
		self.user_id = str(json['user_id'])
		self.netid = netid
		self.seconds_late = json['seconds_late']

		self.directory = os.path.join('./sandbox/submissions', self.submission_id)
		self.comment_file = os.path.join('./results', self.submission_id + '_output')
		self.invalid = False
		
		self.grade = -1
		self.late_penalty = 0

		self.submitted = 'attachments' in json
		if (self.submitted):
			self.attachment_urls = [att['url'] for att in json['attachments']]

	def UploadResults(self, config):
		assert self.grade >= 0, 'Grade never set for: ' + self.submission_id
		# url = "https://canvas.northwestern.edu/api/v1/courses/72859/assignments/458956/submissions/9941"
		# with open(self.comment_file, 'r') as comment_contents:
		# 	comments = '\n'.join(comment_contents.readlines())
		# r = requests.put(url, params={ 'access_token': config.api_key, 'comment[text_comment]': comments, 'submission[posted_grade]': self.grade })


class Preparer(CanvasElement):
	"""
	Container class for pointers to the submissions directory.
	Handles the running of unit tests and making the results textfile.
	"""
	def __init__(self, config, submission, directory='sandbox/submissions'):
		super(Preparer, self).__init__(config)
		self.submission = submission
		self.directory_name = directory
		self.path = os.path.join(self.directory_name, str(self.submission.submission_id))

	def MakeDirectory(self):
		if not os.path.exists(self.path):
			os.makedirs(self.path)
		assert False, 'Asked to make a directory, but we already had one.'
	
	def DownloadSubmission(self):
		if not self.submission.submitted: return
		url = self.submission.attachment_urls[0]
		file = requests.get(url, stream=True)
		zipname = str(self.submission.submission_id) + '_zip.zip'
		self.zippath = os.path.join(self.path, zipname)

		with open(self.zippath, 'wb') as zp:
			zp.write(file.content)
		print('Wrote zip file to: ' + self.zippath)


	def UnzipSubmission(self):
		if not self.submission.submitted: return
		respath = self.zippath.split('.')[0]
		with open (self.zippath, 'rb') as zp:
			z = zipfile.ZipFile(zp)
			z.extractall(respath)
		# z = zipfile.ZipFile(io.BytesIO(file.content))
		# z.extractall(self.path)
		# print('Extracted file to: ' + self.path)

	def Prepare(self):
		print('Preparing submission for:\t' + str(self.submission.submission_id))
		if os.path.exists(self.path): return # assume correct production on previous runs
		
		self.MakeDirectory()
		self.DownloadSubmission()
		self.UnzipSubmission()


		
# overlord
# class submission

import requests
from canvas import CanvasElement

class AssignmentsFetcher(CanvasElement):
	"""Fetches a list of all assignments. Prints their names and ids.
	Useful for when you want to change configurations."""
	def __init__(self, config):
		super(AssignmentsFetcher, self).__init__(config)

	def PrintAll(self):
		url = self.config.base_url + 'courses/72859/assignments/'
		results = []
		maxwidth = 0
		
		r = requests.get(url, params=self.config.payload)
		for assignment in r.json():
			name = assignment['name']
			ident = assignment['id']
			maxwidth = max(maxwidth, len(name))
			results.append((name, ident))

		for result in results:
			name = str(result[0])
			name += ' ' * (maxwidth - len(name))
			ident = str(result[1])
			print('Name:\t' + name + '\tID:\t' + ident)