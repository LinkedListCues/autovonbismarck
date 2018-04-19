import requests

class CanvasConfig(object):
	"""Container class for Canvas configuration.
	Holds information like your API key as well as your course number."""
	def __init__(self):
		super(CanvasConfig, self).__init__()

		self.course_id = '72859'
		self.assignment_id = '458956'
		self.base_url = 'https://canvas.northwestern.edu/api/v1/'

		self.payload = {'per_page':'99'}
		with open('secret', 'r') as secretfile:
			# TODO validation
			self.api_key = secretfile.readline().strip()
			self.payload['access_token'] = self.api_key
		

	# def MakeURL(self, **args):



class CanvasElement(object):
	"""A base class for things that use the Canvas config of a particular course."""
	def __init__(self, config):
		super(CanvasElement, self).__init__()
		self.config = config
		

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

# overlord
# class submission