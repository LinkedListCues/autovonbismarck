import requests

class CanvasElement(object):
	"""A base class for things that use the Canvas config of a particular course."""
	def __init__(self, config):
		super(CanvasElement, self).__init__()
		self.config = config
		

# assignment getter
class AssignmentsFetcher(CanvasElement):
	"""Fetches a list of all assignments. Prints their names and ids.
	Useful for when you want to change configurations."""
	def __init__(self, config):
		super(AssignmentsFetcher, self).__init__(config)

	def PrintAll(self):
		url = 'https://canvas.northwestern.edu/api/v1/courses/72859/assignments/'
		r = requests.get(url, params=self.config.payload)
		json = r.json()
		results = []
		for assignment in json:
			results.append((assignment['name'], assignment['id']))
		for result in results:
			print('Name:\t' + str(result[0]) + '\tID:\t' + str(result[1]))

# overlord
# class submission