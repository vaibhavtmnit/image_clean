# import the necessary packages
from requests import exceptions
import pandas as pd
import argparse
import requests
import cv2
import os
print("Doing something")
image_categories = ['fort & palaces']


OUTPUT_PATH = '/Users/vaibhavthakur/PycharmProjects/Image Treatment/Image dataset'

API_KEY = "ce9cae8772564a45a6c64bfae0b49a61"
MAX_RESULTS = 300
GROUP_SIZE = 50
# set the endpoint API URL
URL = "https://api.cognitive.microsoft.com/bing/v7.0/images/search"

EXCEPTIONS = set([IOError, FileNotFoundError,
	exceptions.RequestException, exceptions.HTTPError,
	exceptions.ConnectionError, exceptions.Timeout])
faulty = []
# store the search term in a convenience variable then set the
# headers and search parameters
for term in image_categories:
	os.mkdir(os.path.join(OUTPUT_PATH,term))
	print(term)
	headers = {"Ocp-Apim-Subscription-Key": API_KEY}
	params = {"q": term, "offset": 0, "count": GROUP_SIZE}
	# make the search
	print("[INFO] searching Bing API for '{}'".format(term))
	search = requests.get(URL, headers=headers, params=params)
	search.raise_for_status()
	# grab the results from the search, including the total number of
	# estimated results returned by the Bing API
	results = search.json()
	estNumResults = min(results["totalEstimatedMatches"], MAX_RESULTS)
	print("[INFO] {} total results for '{}'".format(estNumResults,
	term))
	# initialize the total number of images downloaded thus far
	total = 0

	for offset in range(0, estNumResults, GROUP_SIZE):
		# update the search parameters using the current offset, then
		# make the request to fetch the results
		print("[INFO] making request for group {}-{} of {}...".format(
			offset, offset + GROUP_SIZE, estNumResults))
		params["offset"] = offset
		search = requests.get(URL, headers=headers, params=params)
		search.raise_for_status()
		results = search.json()
		print("[INFO] saving images for group {}-{} of {}...".format(
			offset, offset + GROUP_SIZE, estNumResults))
		# loop over the results
		for v in results["value"]:
			# try to download the image
			try:
				# make a request to download the image
				print("[INFO] fetching: {}".format(v["contentUrl"]))
				r = requests.get(v["contentUrl"], timeout=30)

				# build the path to the output image
				ext = v["contentUrl"][v["contentUrl"].rfind("."):]

				p = os.path.join(OUTPUT_PATH,term, "{}{}".format(
					str(total).zfill(8), ext))
				print(p)
				# write the image to disk
				f = open(p, "wb")
				f.write(r.content)
				f.close()
			# catch any errors that would not unable us to download the
			# image
			except Exception as e:
				# check to see if our exception is in our list of
				# exceptions to check for
				if type(e) in EXCEPTIONS:
					print("[INFO] skipping: {}".format(v["contentUrl"]))
					continue
				# try to load the image from disk
			image = cv2.imread(p)
			# if the image is `None` then we could not properly load the
			# image from disk (so it should be ignored)
			if image is None:
					faulty.append(term+"_"+str(total))
					continue
			# update the counter
			total += 1

df = pd.DataFrame({'faulty':faulty})
df.to_csv('faulty_images.csv')