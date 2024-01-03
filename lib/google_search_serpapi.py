import serpapi
import os

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

print(result["related_questions"]) # Get all the related questions
