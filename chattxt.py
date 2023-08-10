# chatgpt.py
import os
import sys
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import DirectoryLoader

import environ
env = environ.Env()
environ.Env.read_env()

OPENAI_API_KEY = env('OPENAI_API_KEY')

if OPENAI_API_KEY == "":
	print("Missing OpenAPI key")
	exit()

print("Using OpenAPI with key ["+OPENAI_API_KEY+"]")


# 2: load your data document
#loader = TextLoader("data.txt")
#loader = DirectoryLoader("datasets/clinton", glob="*.csv")
#loader = DirectoryLoader("datasets/simple", glob="*.txt")
loader = DirectoryLoader("datasets/px", glob="*.pdf")

# 3: create an index
index = VectorstoreIndexCreator().from_loaders([loader])

# 4: get prompt specified via command line
#query = sys.argv[1]

# 5: query the index
# 6: output the response
#print(index.query(query))

def get_prompt():
	print("Type 'exit' to quit")

	while True:
		prompt = input("Enter a prompt: ")

		if prompt.lower() == 'exit':
			print('Exiting...')
			break
		else:
			try:
				print(index.query(prompt))
			except Exception as e:
				print(e)

get_prompt()
