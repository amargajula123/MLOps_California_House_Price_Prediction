import os
from datetime import datetime


# ROOT_DIR = os.getcwd() # D:\ML_Projects\MLOps_California_House_Price_Prediction\housing\constant #os.getcwd() # to get current/root working directrory
# print(ROOT_DIR)
def get_current_time_stamp():
    return f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"

   
ROOT_DIR = os.getcwd()  #to get current working directory
CONFIG_DIR = "config"
CONFIG_FILE_NAME = "config.yaml"
CONFIG_FILE_PATH = os.path.join(ROOT_DIR,CONFIG_DIR,CONFIG_FILE_NAME)

# print(CONFIG_FILE_PATH)

CURRENT_TIME_STAMP = get_current_time_stamp()


# Training pipeline related variable
TRAINING_PIPELINE_CONFIG_KEY = "training_pipeline_config"
TRAINING_PIPELINE_ARTIFACT_DIR_KEY = "artifact_dir" 
TRAINING_PIPELINE_NAME_KEY = "pipeline_name"


# Data Ingestion related variable

# "data_ingestion" for creating one folder inside that this bellow operations 
# like donload exctract will be done

DATA_INGESTION_CONFIG_KEY = "data_ingestion_config"
DATA_INGESTION_ARTIFACT_DIR = "data_ingestion" # aftifact_dir
DATA_INGESTION_DOWNLOAD_URL_KEY = "dataset_download_url"
DATA_INGESTION_RAW_DATA_DIR_KEY = "raw_data_dir"
DATA_INGESTION_TGZ_DOWNLOAD_DIR_KEY = "tgz_download_dir"
DATA_INGESTION_INGESTED_DIR_NAME_KEY = "ingested_dir"
DATA_INGESTION_TRAIN_DIR_KEY = "ingested_train_dir"
DATA_INGESTION_TEST_DIR_KEY = "ingested_test_dir"

# Data Validation related variables
DATA_VALIDATION_CONFIG_KEY = "data_validation_config"
DATA_VALIDATION_SCHEMA_FILE_NAME_KEY = "schema_file_name"
DATA_VALIDATION_SCHEMA_DIR_KEY = "schema_dir"
DATA_VALIDATION_ARTIFACT_DIR_NAME = "data_validation" # aftifact_dir
DATA_VALIDATION_REPORT_FILE_NAME_KEY= "report_file_name"
DATA_VALIDATION_REPORT_PAGE_FILE_NAME_KEY="report_page_file_name"


# Data Transformaion related variables
DATA_TRANSFORMATION_ARTIFACT_DIR = "data_transformation" # aftifact_dir
DATA_TRANSFORMATION_CONFIG_KEY = "data_transformation_config"
DATA_TRANSFORMATION_ADD_BEDROOM_PER_ROOM_KEY = "add_bedroom_per_room"
DATA_TRANSFORMATION_DIR_NAME_KEY = "transformed_dir"
DATA_TRANSFORMATION_TRAIN_DIR_NAME_KEY= "transformed_train_dir"
DATA_TRANSFORMATION_TEST_DIR_NAME_KEY= "transformed_test_dir"
DATA_TRANSFORMATION_PREPROCESSING_DIR_KEY = "preprocessing_dir"
DATA_TRANSFORMATION_PREPROCESSED_FILE_NAME_KEY = "preprocessed_object_file_name"

TARGET_COLUMN_KEY="target_column"

# data_transformation_config:
#   add_bedroom_per_room: true  # addition columns creation doene based on datset if add_bedroom_per_room = True
#   transformed_dir: transformed_data # transformed_data means if we applied "Feature Engineering" on my dataset that that will be store here
#   transformed_train_dir: train # transformed_train_dir
#   transformed_test_dir: test  # transformed_test_dir
#   preprocessing_dir: preprocessed  # for storing picle file into any Dir so that "preprocessed" is a Dir
#   preprocessed_object_file_name: preprocessed.pkl  # preprocessed.pkl file 


# Data transformation related variables for shema dataset
COLUMN_TOTAL_ROOMS = "total_rooms"
COLUMN_POPULATION = "population"
COLUMN_HOUSEHOLDS = "households"
COLUMN_TOTAL_BEDROOM = "total_bedrooms"
DATASET_SCHEMA_COLUMNS_KEY=  "columns"

NUMERICAL_COLUMN_KEY="numerical_columns"
CATEGORICAL_COLUMN_KEY = "categorical_columns"

TARGET_COLUMN_KEY="target_column"
