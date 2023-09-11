import pymongo

import os
import sys

mongo_uri = sys.argv[1]
if mongo_uri == "":
	print("Missing MongoDB URI")
	exit()

print("Using :", mongo_uri)

try:
	# Connect to MongoDB
	client = pymongo.MongoClient(mongo_uri)
	
	# Replace 'your_database' with the name of your database
	db = client.your_database

	# List all available databases
	database_names = client.list_database_names()

	# Print the list of database names
	for db_name in database_names:
		print("Database:", db_name)

	# Get a list of collection names in the database
	collection_names = db.list_collection_names()

	if collection_names:
		print("Collections in the database:")
		for collection in collection_names:
			print(collection)
	else:
		print("No collections found in the database.")

except Exception as e:
	print(f"An error occurred: {e}")

finally:
	# Close the MongoDB connection when done
	client.close()

