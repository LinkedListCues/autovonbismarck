import requests, os, shutil, zipfile, io, json
from pprint import pprint

class CanvasConfig(object):
	"""Container class for Canvas configuration.
	Holds information like your API key as well as your course number."""
	def __init__(self, json):
		super(CanvasConfig, self).__init__()
		self._json=json

		secret_file = self._json['canvas_key_location']
		with open(secret_file, 'r') as secret:
			self.api_key = secret.readline().strip()

		self.mstest_path = self._json['test_path']
		self.msbuild_path = self._json['build_path']

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

	def GetUserURL(self):
		return self.MakeURL('courses', self.course_id, 'users')

	def GetUploadURL(self, user_id):
		return self.MakeURL(
			'courses', self.course_id,
			'assignments', self.assignment_id,
			'submissions', user_id)

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
		print('Fetching netids...')
		netids = {}
		url = self.config.GetUserURL()
		page = 1
		while(True):
			json = self.config.GetJSON(url, page)
			if not json: break
			for item in json:
				user = item['id']
				netids[user] = item['login_id']
			page += 1

		url = self.config.GetSubmissionsURL()
		page = 1

		print('Preparing roster...')
		# iterate over all of the pages, stopping when the json is empty
		while(True):
			json = self.config.GetJSON(url, page)
			if not json: break
			for item in json:
				user = item['user_id']
				sub = Submission(self.config, item, netids[user])
				self.submissions[sub.submission_id] = sub
			page += 1


# TODO so much clean up
class Submission(object):
	"""Container class for holding submission information, including id,
	seconds_late, and the directory in which the relevant files are stored"""
	def __init__(self, config, json, netid):
		super(Submission, self).__init__()
		self.config = config

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

	def UploadResults(self, config, no_comment=False):
		assert self.grade >= 0, 'Grade never set for: ' + self.submission_id
		print('Uploading result for ' + self.netid + ' Grade: ' + str(self.grade))
		
		# url = self.config.GetUploadURL(self.user_id)
		url = "https://canvas.northwestern.edu/api/v1/courses/72859/assignments/458956/submissions/" + self.user_id
		with open(self.comment_file, 'r') as comment_contents:
			comments = '\n'.join(comment_contents.readlines())
		
		payload = { 'access_token': config.api_key, 'subission[posted_grade]': self.grade }
		if not no_comment: payload['comment[text_comment]'] = comments

		r = requests.put(url, params=payload)


class Preparer(CanvasElement):
	"""
	Container class for pointers to the submissions directory.
	Handles the running of unit tests and making the results textfile.
	"""
	def __init__(self, config, submission, directory):
		super(Preparer, self).__init__(config)
		self.submission = submission
		self.directory_name = directory
		self.path = os.path.join(self.directory_name, str(self.submission.submission_id))

	def Prepare(self, no_zip=False):
		print('Preparing submission for:\t' + str(self.submission.submission_id))
		if os.path.exists(self.path): return # assume correct production on previous runs
		os.makedirs(self.path, exist_ok=True)

		self.DownloadSubmission(no_zip)
		if not no_zip: self.UnzipSubmission()

	
	def DownloadSubmission(self, no_zip):
		if not self.submission.submitted: return
		url = self.submission.attachment_urls[0]
		file = requests.get(url, stream=True)
		
		if no_zip:
			path_name = os.path.join(self.path, str(self.submission.submission_id + '.cs'))
			with open(path_name, 'wb') as path:
				path.write(file.content)
			print('Wrote to ' + path_name)
		else:
			zipname = str(self.submission.submission_id) + '.zip'
			self.zippath = os.path.join(self.path, zipname)

			with open(self.zippath, 'wb') as zp:
				zp.write(file.content)
			print('Wrote zip file to ' + self.zippath)


	def UnzipSubmission(self):
		if not self.submission.submitted: return
		respath = os.path.splitext(self.zippath)[0]
		print('Unzipping to ' + respath)
		with open (self.zippath, 'rb') as zp:
			z = zipfile.ZipFile(zp)
			z.extractall(respath)