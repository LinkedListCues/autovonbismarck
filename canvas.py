import requests, os, shutil, zipfile, io

class CanvasConfig(object):
	"""Container class for Canvas configuration.
	Holds information like your API key as well as your course number."""
	def __init__(self):
		super(CanvasConfig, self).__init__()

		self.course_id = '72859'
		self.assignment_id = '458956'
		self.base_url = 'https://canvas.northwestern.edu/api/v1/'

		self.payload = {'per_page':'100'}
		with open('secret', 'r') as secretfile:
			# TODO validation
			self.api_key = secretfile.readline().strip()
			self.payload['access_token'] = self.api_key

	def MakeURL(self, *argv):
		return self.base_url + '/'.join([str(arg) for arg in argv])

	def GetSubmissionsURL(self):
		return self.MakeURL(
			'courses', self.course_id,
			'assignments', self.assignment_id,
			'submissions')

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
		self.submissions = []

	def FetchSubmissions(self):
		url = self.config.GetSubmissionsURL()
		page = 1
		# iterate over all of the pages, stopping when the json is empty
		# is this a hack? hard to tell with python
		while(True):
			json = self.config.GetJSON(url, page)
			if not json: break
			for item in json:
				self.submissions.append(Submission(item)) # sorry about this
			page += 1


class Submission(object):
	"""
	Container class for submission information.
	Provides access to the name, id, download url, and timestamp.
	Also holds onto the raw json, in case that matters to you.
	"""
	def __init__(self, json):
		super(Submission, self).__init__()
		self.json = json
		self.ident = json['id']
		self.seconds_late = json['seconds_late']

		self.submitted = 'attachments' in json
		if (self.submitted):
			self.attachment_urls = [att['url'] for att in json['attachments']]


class Testable(CanvasElement):
	"""
	Container class for pointers to the submissions directory.
	Handles the running of unit tests and making the results textfile.
	"""
	def __init__(self, config, submission, clobber=False, directory='test'):
		super(Testable, self).__init__(config)
		self.submission = submission
		self.clobber = clobber
		self.directory_name = directory

	def MakeDirectory(self):
		self.path = os.path.join(self.directory_name, str(self.submission.ident))
		if not os.path.exists(self.path):
			os.makedirs(self.path)
			return

		if not self.clobber: return
		shutil.rmtree(self.path, ignore_errors=True)
		os.makedirs(self.path)
	
	def DownloadSubmission(self):
		if not self.submission.submitted: return
		url = self.submission.attachment_urls[0]
		file = requests.get(url, stream=True)
		zipname = str(self.submission.ident) + '_zip.zip'
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
		return

	def Prepare(self):
		print('Preparing submission for:\t' + str(self.submission.ident))
		self.MakeDirectory()
		self.DownloadSubmission()
		self.UnzipSubmission()

		
class Overlord(CanvasElement):
	"""docstring for Overlord"""
	def __init__(self, config):
		super(Overlord, self).__init__(config)
		self.submissions = SubmissionFetcher(config)
		self.testables = []

	def PrepareSubmissions(self):
		self.submissions.FetchSubmissions()

	def PrepareTestables(self):
		for sub in self.submissions.submissions:
			testable = Testable(self.config, sub, True)
			testable.Prepare()
			self.testables.append(testable)

	def RunTests(self):
		for test in self.testables:
			sub = test.submission
			ident = sub.ident
			submitted = sub.submitted
			print('ID:\t' + str(ident) + '\tSub:\t' + str(submitted))
			if not submitted: continue
			print('Running tests...')
			test.RunTests()
			print()


		
# overlord
# class submission