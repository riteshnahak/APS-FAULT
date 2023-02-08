import pymongo
import pandas as pd
from dataclasses import dataclass
import os
import json
# we connectinng with mongo db and making our url store in .env for safety

@dataclass

class EnvironmentVariable():
    mango_db_url:str=os.getenv("MONGO_DB_URL")
    aws_access_key_id:str=os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key:str=os.getenv("AWS_SECRET_ACCESS_KEY")

env_var=EnvironmentVariable()
mongo_client=pymongo.MongoClient(env_var.mango_db_url)
TARGET_COLUMN = "class"