import os,sys
import pandas as pd
from sensor.exception import SensorException
from sensor.logger import logging
from sensor.config import mongo_client
import yaml

def get_collection_as_dataframe(database_name:str,collection_name:str):
    '''
    Description: This function return collection as dataframe
    =========================================================
    Params:
    database_name: database name
    collection_name: collection name
    =========================================================
    return Pandas dataframe of a collection
    '''
    try:

        logging.info(f"Reading data from database  :{database_name}  and collection :{collection_name}")
        df=pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f'Found columns {df.columns}')
        if "_id" in df.columns:
            logging.info('Dropping column: _id ')
            df.drop("_id",axis=1)
            logging.info(f"Rows and Column in dataframe is {df.shape}")
        return df        
    except Exception as e:
        raise SensorException(e, sys)

def write_yaml_file(file_path,data:dict):
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    except Exception as e:
        raise SensorException(e, sys)



def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    try:
        logging.info(f"columns to convert:{df.columns}")
        for column in df.columns:
            if column not in exclude_columns:
                df[column]=df[column].astype('float')
        logging.info(f"columns converted to float")
        return df
    except Exception as e:
        raise e


    except Exception as e:
        raise e



