import sys,os
import pandas as pd
import numpy as np
from sensor.entity import config_entity,artifact_entity
from sensor.exception import SensorException
from sensor.logger import logging
from typing import Optional
from xgboost import XGBClassifier
from sensor import utils
from sklearn.metrics import f1_score

class ModelTrainer:
    def __init__(self,model_trainer_config:config_entity.ModelTrainerConfig,
                        data_transformation_artifact:artifact_entity.DataTransformationArtifact
                ):
        try:
            logging.info(f"{'>>'*20} Model Trainer {'<<'*20}")
            self.model_trainer_config=model_trainer_config
            self.data_transformation_artifact=data_transformation_artifact

        except Exception as e:
            raise SensorException(e, sys)
    
    def train_model(self,x,y):
        try:
            xgb_clf=XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise SensorException(e, sys)

    def initiate_model_trainer(self):
        try:
            logging.info("loading numpy training and test array")
            train_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr=utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)

            logging.info('Splitting data into train and test')
            x_train,y_train=train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test=test_arr[:,:-1],test_arr[:,-1]

            logging.info('Training the model')
            model=self.train_model(x=x_train, y=y_train)

            logging.info("Calculating F1 train score")
            yhat_train=model.predict(x_train)
            f1_train_score=f1_score(y_true=y_train,y_pred=yhat_train)
            logging.info("Calculating F1 test score")
            yhat_test=model.predict(x_test)
            f1_test_score=f1_score(y_true=y_test,y_pred=yhat_test)

            logging.info(f"Training Score : {f1_train_score} Test Score : {f1_test_score}")
            logging.info("Checking model is underfitting or not")
            if f1_test_score < self.model_trainer_config.expected_score:
                raise Exception(f"Model is not able to give you \
                    expected accuracy : {self.model_trainer_config.expected_score}")

            logging.info("Checking model is overfitting or not")
            diff=abs(f1_train_score-f1_test_score)
            if diff > self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")

            # Save the trained Model
            logging.info("Saving the training model")
            utils.save_object(file_path=self.model_trainer_config.model_path, obj=model)

            # Prepare artifact
            logging.info("Prepare Modeltrainer artifact")
            model_trainer_artifact=artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
                                 f1_train_score=f1_train_score, f1_test_score=f1_test_score)
            logging.info(f"Model Trainer Artifact : {model_trainer_artifact}")
            return model_trainer_artifact

        except Exception as e:
            raise SensorException(e, sys)
        