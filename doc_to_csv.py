#!/usr/bin/python3

from elasticsearch import Elasticsearch
from datetime import date
import pandas as pd
from os import getlogin, environ

todays_date = date.today().strftime("%Y.%m.%d")

SERVER_IP = environ.get("SERVER_IP")
client = Elasticsearch(f"http://{SERVER_IP}:9200")

indices_list = client.indices.get(index="*")

search_query = {
    "query": {
        "match_all": {}
    },
    "size": 1,  # Return only 1 result, change the number to see more results
    "sort": [
        {
            "@timestamp": {
                "order": "desc"
            }
        }
    ]
}

recent_index = []
for index in indices_list:
    if index[0] == '.' : continue
    if index.split('-')[-1] == todays_date: recent_index.append(index)
  

results = []
for index_name in recent_index:
    response = client.search(index=index_name, body=search_query)
  
    for doc in response["hits"]["hits"]:
        doc_id = doc["_id"]
        doc_msg = doc["_source"]["message"]
        doc_timestamp = doc["_source"]["@timestamp"]
        results.append({"INDEX NAME": index_name, "DOCUMENT ID": doc_id, "TIMESTAMP": doc_timestamp, "MESSAGE": doc_msg})
df = pd.DataFrame(results)

USER=getlogin()
csv_file_path = f"/home/{USER}/Documents/es_output.csv"

df.to_csv(csv_file_path, index=False)
print(f"Results have been written to {csv_file_path}")