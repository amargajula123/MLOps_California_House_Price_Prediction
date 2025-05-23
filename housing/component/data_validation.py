from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import DataValidationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

import os,sys
import pandas  as pd
import json


# from evidently.report import Report
# from evidently.metrics import DatasetDriftMetric

# from evidently.model_profile import Profile
# from evidently.model_profile.sections import DataDriftProfileSection

# from evidently.dashboard import Dashboard
# from evidently.dashboard.tabs import DataDriftTab

import webbrowser
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

from housing.exception import HousingException 





class DataValidation:
    

    def __init__(self, data_validation_config:DataValidationConfig,
                       data_ingestion_artifact:DataIngestionArtifact
                ): # data_ingestion_artifact -> its like "input" from where i get "train" data for validate it
        try:
            logging.info(f"{'='*20}Data Valdaition log started.{'='*20} ")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise HousingException(e,sys) from e


    def get_train_and_test_df(self):
        try:
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            return train_df,test_df
        except Exception as e:
            raise HousingException(e,sys) from e


    def is_train_test_file_exists(self)->bool:
        try:
            logging.info("Checking if training and test file is available")
            is_train_file_exist = False
            is_test_file_exist = False

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            is_train_file_exist = os.path.exists(train_file_path)
            is_test_file_exist = os.path.exists(test_file_path)

            is_available =  is_train_file_exist and is_test_file_exist

            logging.info(f"Is train and test file exists?-> {is_available}")
            
            if not is_available:
                training_file = self.data_ingestion_artifact.train_file_path
                testing_file = self.data_ingestion_artifact.test_file_path
                message=f"Training file: {training_file} or Testing file: {testing_file}" \
                    "is not present"
                logging.info(f"File not found Message = [{message}]")
                raise Exception(message)

            return is_available
        except Exception as e:
            raise HousingException(e,sys) from e
        
    def validate_dataset_schema(self)->bool:
        try:
            validation_status = False
            # task to do validate training and testing dataset using schema file
            # 1. Number of Column
            # 2. Check the value of "ocean proximity" 
            # acceptable values :-    
            #     <1H OCEAN
            #     INLAND
            #     ISLAND
            #     NEAR BAY
            #     NEAR OCEAN
            # 3. Check column names
            validation_status = True
            return validation_status 
        except Exception as e:
            raise HousingException(e,sys) from e


    def get_and_save_data_drift_report(self):
        """
        Generates a JSON data drift report and saves it.
        """
        try:
            # Create a detailed data drift report
            report = Report(metrics=[DataDriftPreset()])

            # Load train and test datasets
            train_df, test_df = self.get_train_and_test_df()

            # Run the report
            report.run(reference_data=train_df, current_data=test_df)

            # Convert report to JSON
            report_json = report.as_dict()

            # Save the report as a JSON file
            report_file_path = self.data_validation_config.report_file_path
            os.makedirs(os.path.dirname(report_file_path), exist_ok=True)
            with open(report_file_path, "w") as report_file:
                json.dump(report_json, report_file, indent=6)

            return report_json

        except Exception as e:
            raise HousingException(e) from e
        
    def save_data_drift_report_page(self):
        """
        Generates and saves a dataset drift 
        report as an HTML file with column-wise drift graphs.
        """
        try:
            # Create a detailed drift report with graphs
            report = Report(metrics=[DataDriftPreset()])

            # Load train and test datasets
            train_df, test_df = self.get_train_and_test_df()

            # Run the report
            report.run(reference_data=train_df, current_data=test_df)

            # Save the report as an HTML file
            report_page_file_path = self.data_validation_config.report_page_file_path
            os.makedirs(os.path.dirname(report_page_file_path), exist_ok=True)
            report.save_html(report_page_file_path)

        except Exception as e:
            raise HousingException(e) from e
    
        
    def is_data_drift_found(self)->bool:
        try:
            report = self.get_and_save_data_drift_report()
            self.save_data_drift_report_page()
            return True
        except Exception as e:
            raise HousingException(e,sys) from e

    def initiate_data_validation(self)->DataValidationArtifact :
        try:
            self.is_train_test_file_exists()
            self.validate_dataset_schema()
            self.is_data_drift_found()

            data_validation_artifact = DataValidationArtifact(
                schema_file_path=self.data_validation_config.schema_file_path,
                report_file_path=self.data_validation_config.report_file_path,
                report_page_file_path=self.data_validation_config.report_page_file_path,
                is_validated=True,
                message="Data Validation performed successully.",
                evidently_github="https://github.com/evidentlyai/evidently/tree/main/src/evidently/legacy"
            )
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact
        except Exception as e:
            raise HousingException(e,sys) from e


    def __del__(self):
        logging.info(f"{'='*20}Data Valdaition log completed.{'='*20} \n\n")



# legacy methods
#-------------------------------------------------------------------------------------------


# report = Report(metrics=[DatasetDriftMetric()])

    # def get_and_save_data_drift_report(self):
    #     try:
    #         profile = Profile(section=[DataDriftProfileSection()])

    #         # Load train and test datasets
    #         train_df, test_df = self.get_train_and_test_df()

    #         # Calculate the profile
    #         profile.calculate(train_df,test_df)

    #         report = json.load(profile.json()) # its going to return json object so i get like dictionary formate data


    #         report_file_path = self.data_validation_config.report_file_path
    #         report_dir = os.path.dirname(report_file_path)
    #         os.makedirs(report_dir,exist_ok=True)

    #         #Save the report as a JSON file
    #         with open(report_file_path,"w") as report_file:
    #             json.dump(report,report_file,indent=6)
    #         return report

    #     except Exception as e:
    #         raise HousingException(e,sys) from e
        
    # def save_data_drift_report_page(self):
    #     """
    #     Generates and saves a dataset drift 
    #     report as an HTML file with column-wise drift graphs.
    #     """
    #     try:
    #         dashboard = Dashboard(tabs=[DataDriftTab()])

    #         # Load train and test datasets
    #         train_df, test_df = self.get_train_and_test_df()

    #         # Calculate the profile
    #         dashboard.calculate(train_df,test_df)

    #         report_page_file_path = self.data_validation_config.report_page_file_path
    #         report_page_dir = os.path.dirname(report_page_file_path) # givinh till the directory/folder name
    #         os.makedirs(report_page_dir,exist_ok=True)
            
    #         # saving dashboard page
    #         dashboard.save(report_page_file_path)

    #     except Exception as e:
    #         raise HousingException(e,sys) from e



   

    # def get_and_save_data_drift_report(self):
    #     """
    #     Generates a JSON data "drift report" and saves it.
    #     """
    #     try:
    #         # Create a detailed data drift report
    #         report = Report(metrics=[DataDriftPreset()])

    #         # Load train and test datasets
    #         train_df, test_df = self.get_train_and_test_df()

    #         # Run the report
    #         report.run(reference_data=train_df, current_data=test_df)

    #         # Convert report to JSON
    #         report_json = report.as_dict()

    #         # Save the report as a JSON file
    #         report_file_path = self.data_validation_config.report_file_path

    #         os.makedirs(os.path.dirname(report_file_path), exist_ok=True)
    #         with open(report_file_path, "w") as report_file:
    #             json.dump(report_json, report_file, indent=6)

    #         return report_json

    #     except Exception as e:
    #         raise HousingException(e) from e
        
    # def save_data_drift_report_page(self):
    #     """
    #     Generates and saves a dataset drift 
    #     report as an HTML file with column-wise drift graphs.
    #     """
    #     try:
    #         # Create a detailed drift report with graphs
    #         report = Report(metrics=[DataDriftPreset()])

    #         # Load train and test datasets
    #         train_df, test_df = self.get_train_and_test_df()

    #         # Run the report
    #         report.run(reference_data=train_df, current_data=test_df)

    #         # Save the report as an HTML file
    #         report_page_file_path = self.data_validation_config.report_page_file_path
    #         os.makedirs(os.path.dirname(report_page_file_path), exist_ok=True)
    #         report.save_html(report_page_file_path)

    #     except Exception as e:
    #         raise HousingException(e) from e

    #-------------------------------------------------------------------------------------------