import os
import sys
import environ

from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate

env = environ.Env()
environ.Env.read_env()

# Load API key and document location
OPENAI_API_KEY = env('OPENAI_API_KEY')

if OPENAI_API_KEY == "":
	print("Missing OpenAPI key")
	exit()

print("Using OpenAPI with key ["+OPENAI_API_KEY+"]")

path = sys.argv[1]
if path == "":
	print("Missing document path")
	exit()

# Document loading
loader = DirectoryLoader(path, glob="*")
data = loader.load()

# Text splitting
text_splitter = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap = 0)
all_splits = text_splitter.split_documents(data)

# Create retriever
vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())

# Connect to LLM for generation
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(llm,retriever=vectorstore.as_retriever())

template = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Use three sentences maximum and keep the answer as concise as possible. 
Always say "thanks for asking!" at the end of the answer. 
{context}
Question: {question}
Helpful Answer:"""
QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

llm = ChatOpenAI(batch_size=5, model_name="gpt-3.5-turbo", temperature=0)
qa_chain = RetrievalQA.from_chain_type(
    llm,
    retriever=vectorstore.as_retriever(),
    chain_type_kwargs={"prompt": QA_CHAIN_PROMPT}
)

# prompt loop
def get_prompt():
	print("Type 'exit' to quit")

	while True:
		prompt = input("Enter a prompt: ")

		if prompt.lower() == 'exit':
			print('Exiting...')
			break
		else:
			try:
				result = qa_chain({"query": prompt})
				print(result["result"])
			except Exception as e:
				print(e)

get_prompt()
