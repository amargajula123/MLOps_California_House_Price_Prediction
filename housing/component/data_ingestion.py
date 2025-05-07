from housing.entity.config_entity import DataIngestionConfig
import sys
from housing.exception import HousingException
from housing.logger import logging

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            pass
        except Exception as e:
            raise HousingException(e,sys) from e