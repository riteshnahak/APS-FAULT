import os,sys
from datetime import datetime
from sensor.exception import SensorException
from sensor.logger import logging

FILE_NAME='sensor.csv'
TRAIN_FILE_NAME='train.csv'
TEST_FILE_NAME='test.csv'

class TrainingPipelineConfig:
    def __init__(self):
        try:
            self.artifacts_dir=os.path.join(os.getcwd(),'artifacts',f"{datetime.now().strftime('%m%d%Y__%H%M%S')}")
        except Exception as e:
            raise SensorException(e, sys)

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        try:
            self.database_name='aps'
            self.collection_name='sensor'
            self.data_ingestion_dir=os.path.join(training_pipeline_config.artifacts_dir,'data ingestion')
            self.feature_store_file_path=os.path.join(self.data_ingestion_dir,'feature store',FILE_NAME)
            self.train_file_path=os.path.join(self.data_ingestion_dir,'dataset',TRAIN_FILE_NAME)
            self.test_file_path=os.path.join(self.data_ingestion_dir,'dataset',TEST_FILE_NAME)
            self.test_size=0.2
        except Exception as e:
            raise SensorException(e, sys)
