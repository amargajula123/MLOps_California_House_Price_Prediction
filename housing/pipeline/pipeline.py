from housing.config.configuration import Configuration
from housing.exception import HousingException
from housing.logger import logging

from housing.entity.config_entity import DataIngestionConfig,ModelTrainerConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,\
    DataTransformationArtifact,ModelTrainerArtifact
from housing.component.data_ingestion import DataIngestion
from housing.component.data_validation import DataValidation
from housing.component.data_transformation import DataTransformation
from housing.component.model_trainer import ModelTrainer
import os,sys

class Pipeline:

    def __init__(self,config: Configuration = Configuration()) -> None:
        try:
            self.config=config
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact)\
        -> DataValidationArtifact:
        try:
            data_validation = DataValidation(data_validation_config=self.config.get_data_validation_config(),
                                             data_ingestion_artifact=data_ingestion_artifact
            )# data_ingestion_artifact -> its like "input", from where i get "train" data for validate it
            return data_validation.initiate_data_validation()
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def start_data_transformation(self,
                                  data_ingestion_artifact: DataIngestionArtifact,
                                  data_validation_artifact: DataValidationArtifact
                                  ) -> DataTransformationArtifact:
        try:
            data_transformation = DataTransformation(
                data_transformation_config=self.config.get_data_transformation_config(),
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_artifact=data_validation_artifact
            )
            return data_transformation.initiate_data_transformation()
        except Exception as e:
            raise HousingException(e, sys)
        
    def start_model_trainer(self,data_transformation_artifaact: DataTransformationArtifact):
        try:
            model_trainer = ModelTrainer(
                model_trainer_config=self.config.get_model_trainer_config(),
                data_transformation_artifact=data_transformation_artifaact
            )
            return model_trainer.initiate_model_trainer()
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def start_model_evaluation(self):
        try:
            pass
        except Exception as e:
            raise HousingException(e, sys) from e
    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise HousingException(e, sys) from e
        
    def run_pipeline(self):
        try:
            # we are checking the pipeline is running or not if running_status = True. we are restricting
            # another pipeline is get started. so we know as we create "Thread class" if we initilize the
            # object of Thread class it will work for one time only. if we use againg we need to initialize
            # the object of Thread class again so here instead of creating object we just checking what the status of pipeline
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact,
                                                                          data_validation_artifact=data_validation_artifact)
        except Exception as e:
            raise HousingException(e, sys) from e
