# This will creat connection our environment with mongodb and will store csv data 
# after converting to json

import json
import pymongo
import pandas as pd

from sensor.config import mongo_client

DATA_FILE_PATH="/config/workspace/aps_failure_training_set1.csv"
DATABASE_NAME="aps"
COLLECTION_NAME="sensor"

if __name__=="__main__":
    
    df=pd.read_csv(DATA_FILE_PATH)
    print(f"Rows and columns are : {df.shape}")
#Reset the indexes.
    df.reset_index(drop=True,inplace=True)
#converting df to json file after transposing it and stored the values as a list.
    json_record=list(json.loads(df.T.to_json()).values())
    print(json_record[0])
# Create connection that how u wnat to store in mongodb.
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)

# Print statements are not mandetory i am using it for my convience of checking whether the code run
#up to this or not