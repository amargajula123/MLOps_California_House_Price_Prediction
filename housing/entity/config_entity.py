from collections import namedtuple

DataIngestionConfig = namedtuple("DataIngestionConfig",["dataset_download_url",
                                                        "tgz_download_dir",
                                                        "raw_data_dir",
                                                        "ingested_train_dir",
                                                        "ingested_test_dir"])

DataValidationConfig = namedtuple("DataValidationConfig",["schema_file_path"
                                                          ,"report_file_path"
                                                          ,"report_page_file_path"])



DataTransformationConfig = namedtuple("DataTransformationConfig", ["add_bedroom_per_room",
                                                                   "transformed_train_dir",
                                                                   "transformed_test_dir",
                                                                   "preprocessed_object_file_path"])

                            # preprocessed_object_file_path = pickle file path, means pickle object of "feature engineering" 



ModelTrainerConfig = namedtuple("ModelTrainerConfig", ["trained_model_file_path",
                                                       "base_accuracy",
                                                       "model_config_file_path"])

# trained_model_file_path : if we train our model we have to export that into pickle file that location
# we specify at  trained_model_file_path
# trained_model_file_path  == "pickle file" of trained model location

# base_accuracy : if my model is not giving  beter then "base_accuracy" then i will not use my model accuracy
# if my model accuracy is better then "base_accuracy" then i will 



ModelEvaluationConfig = namedtuple("ModelEvaluationConfig", ["model_evaluation_file_path",
                                                             "time_stamp"])

# all the model information will store in this file path : model_evaluation_file_path
# in model evaluation we evaluate our model with the test dataset at the same time we compare
# all the model with the Best_Model

# time_stamp : when you compare your model with the base_model  at what time it actually done that will store

ModelPusherConfig = namedtuple("ModelPusherConfig", ["export_dir_path"])

# ModelPusherConfig : export_dir_path : push the model if you come to know model is better then all base models

TrainingPipelineConfig = namedtuple("TrainingPipelineConfig", ["artifact_dir"])