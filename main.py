import requests
from canvas import *

# set up configuration
# get all of the submissions as json
# 	try to serialize things out so that we don't have to do this bit too often
#	set up student representations
# iterate over each submission, running the test framework and recording the results
# collate all of the results
# generate grades and comments for each student
# 	late penalties; extensions
# upload grades and comments for each student


if __name__ == '__main__':
	config = CanvasConfig()
	overlord = Overlord(config)
	overlord.PrepareSubmissions()
	overlord.PrepareTestables()
	overlord.RunTests()
