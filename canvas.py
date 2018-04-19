import requests

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
		
class Overlord(CanvasElement):
	"""docstring for Overlord"""
	def __init__(self, config):
		super(Overlord, self).__init__(config)
		self.submissions = SubmissionFetcher(config)

	def PrepareSubmissions(self):
		self.submissions.FetchSubmissions()
		for sub in self.submissions.submissions :
			print('ID:\t' + str(sub.ident) + '\tSubmitted:\t' + str(sub.submitted))
		
# overlord
# class submission