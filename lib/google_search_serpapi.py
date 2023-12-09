# Not using it, as they wanted phone verification done.

import os
import serpapi
import csv

from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('SERPAPI_KEY')

client = serpapi.Client(api_key=api_key)
result = client.search(
	q="Retrieval Augumented Generation RAG",
	engine="google",
	location="Austin, Texas",
	hl="en",
	gl="us",
)

print(result)
print(result['organic_results'])
print(result["search_information"]["total_results"]) # Get number of results available
print(result["related_questions"]) # Get all the related questions


organic_results = result["organic_results"]
with open('output.csv', 'w', newline='') as csvfile:
	csv_writer = csv.writer(csvfile)

	# Write the headers
	csv_writer.writerow(["Title", "Link", "Snippet"])

	# Write the data
	for result in organic_results:
		csv_writer.writerow([result["title"], result["link"], result["snippet"]])


print('Done writing to CSV file.')
