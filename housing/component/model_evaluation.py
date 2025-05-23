from housing.logger import logging
from housing.exception import HousingException
from housing.entity.config_entity import ModelEvaluationConfig
from housing.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,ModelTrainerArtifact,ModelEvaluationArtifact
from housing.constant import *
import numpy as np
import os
import sys
from housing.util.util import write_yaml_file, read_yaml_file, load_object,load_data
from housing.entity.model_factory import evaluate_regression_model




class ModelEvaluation:

    def __init__(self, model_evaluation_config: ModelEvaluationConfig,
                 data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_artifact: DataValidationArtifact,
                 model_trainer_artifact: ModelTrainerArtifact):
        try:
            logging.info(f"{'=' * 30}Model Evaluation log started.{'=' * 30} ")
            self.model_evaluation_config = model_evaluation_config
            self.model_trainer_artifact = model_trainer_artifact
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_artifact = data_validation_artifact
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_best_model(self):
        try:
            model = None
            model_evaluation_file_path = self.model_evaluation_config.model_evaluation_file_path

            if not os.path.exists(model_evaluation_file_path):
                write_yaml_file(file_path=model_evaluation_file_path,
                                )
                return model
            model_eval_file_content = read_yaml_file(file_path=model_evaluation_file_path)
            model_eval_file_content = dict() if model_eval_file_content is None else model_eval_file_content

            if BEST_MODEL_KEY not in model_eval_file_content:
                return model

            model = load_object(file_path=model_eval_file_content[BEST_MODEL_KEY][MODEL_PATH_KEY])
            return model
        except Exception as e:
            raise HousingException(e, sys) from e

    def update_evaluation_report(self, model_evaluation_artifact: ModelEvaluationArtifact):
        """
        This update_evaluation_report() function going to call, When the 
        "New Training model" is better then the "Production Model" .

        Note : after Training the New Model only this function will call/execute, 
        """
        try:
            eval_file_path = self.model_evaluation_config.model_evaluation_file_path
            model_eval_content = read_yaml_file(file_path=eval_file_path)
            model_eval_content = dict() if model_eval_content is None else model_eval_content
            
            
            previous_best_model = None
            if BEST_MODEL_KEY in model_eval_content:
                previous_best_model = model_eval_content[BEST_MODEL_KEY]

            logging.info(f"Previous evaluation result: {model_eval_content}")
            eval_result = {
                BEST_MODEL_KEY: {
                    MODEL_PATH_KEY: model_evaluation_artifact.evaluated_model_path,  # evaluated_model_path = newly trained model file path
                }
            }

            if previous_best_model is not None:
                model_history = {self.model_evaluation_config.time_stamp: previous_best_model}
                if HISTORY_KEY not in model_eval_content:
                    history = {HISTORY_KEY: model_history}
                    eval_result.update(history)
                else:
                    model_eval_content[HISTORY_KEY].update(model_history)

            model_eval_content.update(eval_result)
            logging.info(f"Updated evaluation result:{model_eval_content}")
            write_yaml_file(file_path=eval_file_path, data=model_eval_content)

        except Exception as e:
            raise HousingException(e, sys) from e

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            trained_model_file_path = self.model_trainer_artifact.trained_model_file_path
            trained_model_object = load_object(file_path=trained_model_file_path)

            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path

            schema_file_path = self.data_validation_artifact.schema_file_path

            # we are reading 'raw splited data' from the "Data_Ingestion" statge, 
            train_dataframe = load_data(file_path=train_file_path,
                                                           schema_file_path=schema_file_path,
                                                           )
            test_dataframe = load_data(file_path=test_file_path,
                                                          schema_file_path=schema_file_path,
                                                          )
            schema_content = read_yaml_file(file_path=schema_file_path)
            target_column_name = schema_content[TARGET_COLUMN_KEY]

            # target_column
            logging.info(f"Converting target column into numpy array.")
            train_target_arr = np.array(train_dataframe[target_column_name])
            test_target_arr = np.array(test_dataframe[target_column_name])
            logging.info(f"Conversion completed target column into numpy array.")

            # dropping target column from the dataframe
            logging.info(f"Dropping target column from the dataframe.")
            train_dataframe.drop(target_column_name, axis=1, inplace=True)
            test_dataframe.drop(target_column_name, axis=1, inplace=True)
            logging.info(f"Dropping target column from the dataframe completed.")
 
            # from here we get the Best "Model" that is in the Production, why model object is 
            # need is thet we need to compare this "model" and "newly trained model object"
            model = self.get_best_model()

            if model is None:
                logging.info("Not found any existing model. Hence accepting trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model evaluation artifact {model_evaluation_artifact} created")
                return model_evaluation_artifact

            model_list = [model, trained_model_object] # production model object and new trained model object
            logging.info(f"Model__list = {model_list} ")

            metric_info_artifact = evaluate_regression_model(model_list=model_list,
                                                             X_train=train_dataframe,
                                                             y_train=train_target_arr,
                                                             X_test=test_dataframe,
                                                             y_test=test_target_arr,
                                                             base_accuracy=self.model_trainer_artifact.model_accuracy,
                                                             train_test_acc_threshold=self.model_trainer_artifact.train_test_acc_threshold
                                                              )
            logging.info(f"Model evaluation completed. model metric artifact: {metric_info_artifact}")


            # if from the comparision of both the regression models if none of the model is better
            # like if bothe the model are not better then base_accuracy (theshhold) then we abviously
            # get "None" 
            if metric_info_artifact is None:
                response = ModelEvaluationArtifact(is_model_accepted=False,
                                                   evaluated_model_path=trained_model_file_path
                                                   )
                logging.info(f"Both the models are not better then the base_accuracy: {response}")
                return response

            if metric_info_artifact.index_number == 1: # [model, trained_model_object] == [0,1] indexes
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=True)
                self.update_evaluation_report(model_evaluation_artifact)
                logging.info(f"Model accepted. Model evaluation artifact {model_evaluation_artifact} created")

            else:
                logging.info("Trained model is no better than existing model hence not accepting Trained model")
                model_evaluation_artifact = ModelEvaluationArtifact(evaluated_model_path=trained_model_file_path,
                                                                    is_model_accepted=False)
            return model_evaluation_artifact
        except Exception as e:
            raise HousingException(e, sys) from e

    def __del__(self):
        logging.info(f"{'=' * 20}Model Evaluation log completed.{'=' * 20} \n\n")


# In model evaluation phase, what we do is that we actually check if the is any model is
# available in the production. If it is available in the production, then what we actually
# do in the model evaluation phase is that we actually check the model that is in the
# production and newly trained model which is actually done after running the pipeline.
# So, by comparing these two models, like the model that is in the production and the newly 
# trained model, based on both comparison, which model is going to give me the best accuracy, 
# that will be actually going to select. The selected, the best accuracy model which means the
# newly trained model, what actually will be taken ,
#  if there is any no model available in the production then newly Trained model will get selected

# -----------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

        # from "model_evaluation.yaml" file we will get the best model location that is in the production
        # from the "model_trainer_artifact" we will get the best newly Trained model location

        # we compare this "production model" and "newly trained model" which ever is giving best accuracy 
        # will push that model into production and another will be make it as "history" this entire thing
        # will happen inside the "Model_Evalution.py" componenet sage,

# -----------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

