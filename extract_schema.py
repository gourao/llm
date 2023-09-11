# Extract the schema from a JSON document
import json
import os
import sys

# Read the JSON file
path = sys.argv[1]
if path == "":
	print("Missing document path")
	exit()

# For Schema
with open(path, 'r') as json_file:
	json_data = json.load(json_file)

def merge_schemas(schema_list):
    unified_schema = {}
    
    for schema in schema_list:
        if isinstance(schema, dict):
            for key, value in schema.items():
                if key not in unified_schema:
                    unified_schema[key] = value
                elif isinstance(value, dict):
                    unified_schema[key] = merge_schemas([unified_schema[key], value])
        elif isinstance(schema, list):
            if len(schema) > 0 and all(isinstance(item, dict) for item in schema):
                unified_schema = merge_schemas([unified_schema] + schema)
    
    return unified_schema

def extract_schema(data):
    if isinstance(data, dict):
        schema = {}
        for key, value in data.items():
            schema[key] = extract_schema(value)
        return schema
    elif isinstance(data, list):
        schema_list = [extract_schema(item) for item in data]
        return merge_schemas(schema_list)
    else:
        return type(data).__name__

schema = extract_schema(json_data)

# Print the extracted schema as JSON for better visualization
print(json.dumps(schema, indent=2))

#print(json.dumps(schema, separators=(',', ':')))
