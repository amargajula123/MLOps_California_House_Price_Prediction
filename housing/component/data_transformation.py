from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig,DataTransformationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
import os,sys

class DataTransformation:


    def __init__(self,data_transformation_config:DataTransformationConfig,
                      data_ingestion_artifact:DataIngestionArtifact,
                      data_validation_artifact:DataValidationArtifact
    ):# data_ingestion_artifact ->its like "input" from where i get "train " for validate
      # data_validation_artifact ->its also like "input" from where i get "shema file path" for transfor it
        
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact

        except Exception as e:
            raise HousingException(os,sys) from e
        
        

    def ac(self):
        try:
            transformed_train_file_path = None
            transformed_test_file_path = None
            preprocessed_object_file_path=None
            data_transformation_artifact = DataTransformationArtifact(is_transformed=is_transformed,
                                                                        message='ok',
                                                                        transformed_train_file_path=transformed_train_file_path,
                                                                        transformed_test_file_path=transformed_test_file_path,
                                                                        preprocessed_object_file_path=preprocessed_object_file_path)
        except Exception as e:
            raise HousingException(os,sys) from e
        