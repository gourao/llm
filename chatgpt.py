# chatgpt.py
import os
import sys
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import DirectoryLoader

# 1: add API key as environment variable
#API_KEY = env('OPENAI_API_KEY')
os.environ["OPENAI_API_KEY"] = "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"

# 2: load your data document
#loader = TextLoader("data.txt")
#loader = DirectoryLoader("datasets/clinton", glob="*.csv")
#loader = DirectoryLoader("datasets/simple", glob="*.txt")
loader = DirectoryLoader("datasets/px", glob="*.pdf")

# 3: create an index
index = VectorstoreIndexCreator().from_loaders([loader])

# 4: get prompt specified via command line
query = sys.argv[1]

# 5: query the index
# 6: output the response
print(index.query(query))
