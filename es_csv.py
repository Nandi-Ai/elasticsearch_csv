#!/usr/bin/python3

from elasticsearch import Elasticsearch
from datetime import date
import pandas as pd
from os import getlogin

# Set today's date
todaysDate = date.today().strftime("%Y.%m.%d")

# Create an Elasticsearch client instance
client = Elasticsearch("http://80.2.67.1:9200")

# get all indices
indices_list = client.indices.get(index="*")


# Define the search query
search_query = {
    "query": {
        "match_all": {}  # Match all documents
    },
    "size": 1,  # Return only 1 results
    "sort": [
        {
            "@timestamp": {
                "order": "desc"  # Sort in descending order by the timestamp field
            }
        }
    ],
}

recent_index = []
for i in indices_list:
    if i.split('-')[-1] == todaysDate:
        recent_index.append(i)

# Execute the search query
results = []
for index_name in recent_index:
    try:
        response = client.search(index=index_name, body=search_query)
    
        for doc in response["hits"]["hits"]:
            doc_id = doc["_id"]
            doc_msg = doc["_source"]["message"]
            doc_timestamp = doc["_source"]["@timestamp"]
            results.append({"INDEX NAME": index_name, "DOCUMENT ID": doc_id, "TIMESTAMP" :doc_timestamp,"MESSAGE": doc_msg})
    except:
        print(f"{index_name} will generate an error, added to csv file and continuing to next index")
        results.append({"INDEX NAME": index_name,"DOCUMENT ID": '', "TIMESTAMP" :'', "MESSAGE": 'An Error occurred'})
        continue

# Create a DataFrame from the results
df = pd.DataFrame(results)

# Define the CSV file path
USER=getlogin()
csv_file_path = f"/home/{USER}/Documents/es_output.csv"

# Write the DataFrame to CSV
df.to_csv(csv_file_path, index=False)

# Print a success message
print(f"Results have been written to {csv_file_path}")
