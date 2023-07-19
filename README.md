
# Export recent documents of indices to CSV 
This python script will create a CSV file containing 4 colums:

INDEX NAME, DOCUMENT ID, TIMESTAMP, MESSAGE
###
#### Pandas, and Elasticsearch python modules are required to run the script 
##### Install  requirements.txt

`pip install -r requirements.txt`

#### Set the server ip address as an enviroment variable
`export SERVER_IP=<ip address>`


#### run the commands to create the file
```
python3 doc_to_csv.py
```

The file is exported to the **Documents** directory and is called **es_output.csv**
