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