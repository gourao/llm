import os
import sys
import environ

import pymongo

from langchain import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


env = environ.Env()
environ.Env.read_env()

API_KEY = env('OPENAI_API_KEY')

if API_KEY == "":
	print("Missing OpenAPI key")
	exit()

mongo_uri = sys.argv[1]
if mongo_uri == "":
	print("Missing MongoDB URI")
	exit()

db_name = sys.argv[2]
if db_name == "":
	print("Missing DB")
	exit()

collection_name = sys.argv[3]
if collection_name == "":
	print("Missing Collection")
	exit()

print("Using :", mongo_uri, ":", "["+db_name+"]")

# setup llm
llm = ChatOpenAI(model_name="gpt-3.5-turbo",
	temperature=0.7,
	max_tokens=1024,
	openai_api_key=API_KEY)

# Create prompt chain
QUERY = """
Using the Schema Below, create a syntactically correct NoSQL query to run.  The following first has the schema followed by a question to ask on a database given that schema.

Schema: {schema}

Question: {question}
"""

prompt = PromptTemplate(
    input_variables=["schema", "question"],
    template="""Using the Schema Below, create a syntactically correct NoSQL query to run.  The following first has the schema followed by a question to ask on a database given that schema.
				Schema: {schema}
				Question: {question}
			"""
)

chain = LLMChain(llm=llm, prompt=prompt)

def chatmongo(collection):
	print("Type 'exit' to quit")

	while True:
		prompt = input("Enter a prompt: ")

		if prompt.lower() == 'exit':
			print('Exiting...')
			break
		else:
			print(chain.run({
				'schema': "{\"id\": \"str\"}", 
				'question': "how do I find all ids"
				}))

try:
	# Connect to MongoDB
	client = pymongo.MongoClient(mongo_uri)

	# List all available databases
	database_names = client.list_database_names()

	# Print the list of database names
	for name in database_names:
		print("Database:", name)

	db = client[db_name]

	# Get a list of collection names in the database
	collection_names = db.list_collection_names()

	if collection_names:
		print("Collections in the database:")
		for collection in collection_names:
			print(collection)

		# Add data to first collection
		collection = db.collections[collection_name]
		print("Entering NeuBird session with ", collection)

		chatmongo(collection)

	else:
		print("No collections found in the database.")

except Exception as e:
	print(f"An error occurred: {e}")

finally:
	# Close the MongoDB connection when done
	client.close()

