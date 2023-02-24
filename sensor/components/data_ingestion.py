import sys,os
import pandas as pd
from sensor.logger import logging
from sensor.exception import SensorException
from sensor import utils
from sklearn.model_selection import train_test_split
from sensor.entity import config_entity,artifact_entity
import numpy as np

class DataIngestion:
    def __init__(self,data_ingestion_config:config_entity.DataIngestionConfig):
        try:
            logging.info(f'{">>"*20} Data Ingestion {"<<"*20}')
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise SensorException(e, sys)
def initiate_data_ingestion(self)->artifact_entity.DataIngestionArtifact:
    try:
        logging.info("Exporting data into pandas dataframe")
        df:pd.DataFrame=utils.get_collection_as_dataframe(
            database_name=self.data_ingestion_config.database_name,
            collection_name=self.data_ingestion_config.collection_name)
        logging.info("Replacing NaN values")
        df.replace(to_replace='na',value=np.NaN,inplace=True)
        # Save data in feature store
        feature_store_dir=os.path.dirname(self.data_ingestion_config.feature_store_file_path)
        # make directory
        os.makedirs(feature_store_dir,exist_ok=True)

        logging.info("Saving Dataframe to Feature Store")
        #Save df to feature store folder
        df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,index =False,header=True)
        
        
        logging.info("Splitting the dataset")
        train_df,test_df = train_test_split(df,test_size=self.data_ingestion_config.test_size,random_state=42)
        
        logging.info("Create directory if not avaible")
        dataset_dir=os.path.dirname(self.data_ingestion_config.train_file_path)
        os.makedirs(dataset_dir,exist_ok=True)
        logging.info("Save df to feature store folder")
            #Save df to feature store folder

        train_df.to_csv(path_or_buf=self.data_ingestion_config.train_file_path,index=False,header=True)
        test_df.to_csv(path_or_buf=self.data_ingestion_config.test_file_path,index=False,header=True)
            
            #Prepare artifact
        data_ingestion_artifact = artifact_entity.DataIngestionArtifact(
                feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                train_file_path=self.data_ingestion_config.train_file_path, 
                test_file_path=self.data_ingestion_config.test_file_path)

        logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
        return data_ingestion_artifact
    except Exception as e:
        raise SensorException(e, sys)



    

