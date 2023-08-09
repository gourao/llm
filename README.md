# Open Source Q&A engine for SQL databases

This is a Database Overlay for SQL databases that provides a generative interface to the structured data.

It interfaces with LLMs such as Llama2 or GPT-4

## Setup
pip3 install unstructured==0.5.6

pip3 install langchain openai

## Testing
Make sure you have a POSTGRES database running locally with the following config:

```
User: postgres
Password: 1234
Database Name: findb
Port: 6666
```

Or you can change the connection string in `chatdb.py`

This will work with any database schema and content.

```
export OPENAI_API_KEY=YOUR_KEY
python3 chatdb.py
```

