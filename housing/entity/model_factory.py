from cmath import log
import importlib
from pyexpat import model
import numpy as np
import yaml
from housing.exception import HousingException
import os
import sys

from collections import namedtuple
from typing import List
from housing.logger import logging
from sklearn.metrics import r2_score,mean_squared_error
GRID_SEARCH_KEY = 'grid_search'
MODULE_KEY = 'module'
CLASS_KEY = 'class'
PARAM_KEY = 'params'
MODEL_SELECTION_KEY = 'model_selection'
SEARCH_PARAM_GRID_KEY = "search_param_grid"

InitializedModelDetail = namedtuple("InitializedModelDetail",["model_serial_number", 
                                                              "model", 
                                                              "param_grid_search", 
                                                              "model_name"])

GridSearchedBestModel = namedtuple("GridSearchedBestModel", ["model_serial_number",
                                                             "model",
                                                             "best_model",
                                                             "best_parameters",
                                                             "best_score",])

BestModel = namedtuple("BestModel", ["model_serial_number",
                                     "model",
                                     "best_model",
                                     "best_parameters",
                                     "best_score", ])

MetricInfoArtifact = namedtuple("MetricInfoArtifact",["model_name", 
                                                      "model_object",  # model_object is nuthong but trained model_object
                                                      "train_rmse", 
                                                      "test_rmse",
                                                      "train_mse", 
                                                      "test_mse",
                                                      "train_accuracy",
                                                      "test_accuracy", 
                                                      "model_accuracy", 
                                                      "index_number",
                                                      "train_test_acc_threshold"])


def evaluate_classification_model(model_list: list, X_train:np.ndarray, y_train:np.ndarray, X_test:np.ndarray, y_test:np.ndarray, base_accuracy:float=0.6)->MetricInfoArtifact:
    pass


def evaluate_regression_model(model_list: list, X_train:np.ndarray, y_train:np.ndarray, X_test:np.ndarray, y_test:np.ndarray, base_accuracy:float=0.6,train_test_acc_threshold:float=0.05) -> MetricInfoArtifact:
    """
    Description:
    This function compare multiple regression model return best model

    Params:
    model_list: List of model
    X_train: Training dataset input feature
    y_train: Training dataset target feature
    X_test: Testing dataset input feature
    y_test: Testing dataset input feature

    return
    It retured a named tuple
    
    MetricInfoArtifact = namedtuple("MetricInfo",
                                ["model_name", "model_object", "train_rmse", "test_rmse", "train_accuracy",
                                 "test_accuracy", "model_accuracy", "index_number"])

    """
    try:
        
    
        index_number = 0
        metric_info_artifact = None
        for model in model_list:
            model_name = str(model)  #getting model name based on model object
            logging.info(f"{'='*30}Started evaluating model: [{type(model).__name__}] {'='*30}")
            
            #Getting prediction for training and testing dataset
            y_train_pred = model.predict(X_train) 
            y_test_pred = model.predict(X_test)

            #Calculating r squared score on training and testing dataset
            train_acc = r2_score(y_train, y_train_pred)
            test_acc = r2_score(y_test, y_test_pred)

            #Calculating "mean squared error" on training and testing dataset
            train_mse = mean_squared_error(y_train, y_train_pred)
            test_mse = mean_squared_error(y_test, y_test_pred)
            
            #Calculating root mean squared error on training and testing dataset
            train_rmse = np.sqrt(mean_squared_error(y_train, y_train_pred))
            test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))


            # Calculating "harmonic mean" of train_accuracy and test_accuracy
            # in case of "harmonic mean" it give higher weightage to the lower accuracy
            # lower weightage to the higher accuracy.
            model_accuracy = (2 * (train_acc * test_acc)) / (train_acc + test_acc)
            diff_test_train_acc = abs(test_acc - train_acc)
            
            #logging all important metric
            logging.info(f"{'*'*30} Score {'*'*30}")
            logging.info(f"\t\tTrain Score\t\t\t\t Test Score\t\t\t\t Average Score")
            logging.info(f"{train_acc}\t\t {test_acc}\t\t{model_accuracy}")

            logging.info(f"{'*'*30} Loss {'*'*30}")
            logging.info(f"Difference b/w test & train accuracy: [{diff_test_train_acc}].") 

            if diff_test_train_acc > train_test_acc_threshold: # train_test_acc_threshold = 0.05:

                Info = f"""
                           Difference b/w test & train accuracy: [{diff_test_train_acc}] is greter then {train_test_acc_threshold}.
                           So we dont take this one, which accuracy is close to 0.05 will take that as best Model With respect to 
                           any ML algorithm/Model ex:-(LinearRgression) the Train and Test accuracy diffrence is grater then {train_test_acc_threshold}
                           so we can not accept becoze it could be 'Overfitting' or 'Underfiting' Models not the 'Generalised Models'"""
                logging.info(Info)

            logging.info(f"Train root mean squared error: [{train_rmse}].")
            logging.info(f"Test root mean squared error: [{test_rmse}].")


            #if model accuracy is greater than base accuracy and train and test score is within certain thershold
            #we will accept that model as accepted model
            if model_accuracy >= base_accuracy and diff_test_train_acc < train_test_acc_threshold:
                logging.info(f" my BASE ACCURACY = [{base_accuracy}]\n\n")
                base_accuracy = model_accuracy
                logging.info(f" now BASE ACCURACY is bcome = [{base_accuracy}]\n\n")
                metric_info_artifact = MetricInfoArtifact(  model_name=model_name,
                                                            model_object=model,
                                                            train_mse=train_mse,
                                                            test_mse=test_mse,
                                                            train_rmse=train_rmse,
                                                            test_rmse=test_rmse,
                                                            train_accuracy=train_acc,
                                                            test_accuracy=test_acc,
                                                            model_accuracy=model_accuracy,
                                                            index_number=index_number,
                                                            train_test_acc_threshold=train_test_acc_threshold)

                logging.info(f"Acceptable Model Found -> {metric_info_artifact}.")
                
            index_number += 1

        if metric_info_artifact is None:
            logging.info(f"No model found with higher accuracy than base accuracy")
        return metric_info_artifact
    except Exception as e:
        raise HousingException(e, sys) from e


def get_sample_model_config_yaml_file(export_dir: str):
    try:
        model_config = {
            GRID_SEARCH_KEY: {
                MODULE_KEY: "sklearn.model_selection",
                CLASS_KEY: "GridSearchCV",
                PARAM_KEY: {
                    "cv": 3,
                    "verbose": 1
                }

            },
            MODEL_SELECTION_KEY: {
                "module_0": {
                    MODULE_KEY: "module_of_model",
                    CLASS_KEY: "ModelClassName",
                    PARAM_KEY:
                        {"param_name1": "value1",
                         "param_name2": "value2",
                         },
                    SEARCH_PARAM_GRID_KEY: {
                        "param_name": ['param_value_1', 'param_value_2']
                    }

                },
            }
        }
        os.makedirs(export_dir, exist_ok=True)
        export_file_path = os.path.join(export_dir, "model.yaml")
        with open(export_file_path, 'w') as file:
            yaml.dump(model_config, file)
        return export_file_path
    except Exception as e:
        raise HousingException(e, sys)


class ModelFactory:
    def __init__(self, model_config_path: str = None,):
        try:
            self.config: dict = ModelFactory.read_params(model_config_path)

            self.grid_search_cv_module: str = self.config[GRID_SEARCH_KEY][MODULE_KEY]
            self.grid_search_class_name: str = self.config[GRID_SEARCH_KEY][CLASS_KEY]
            self.grid_search_property_data: dict = dict(self.config[GRID_SEARCH_KEY][PARAM_KEY])

            self.models_initialization_config: dict = dict(self.config[MODEL_SELECTION_KEY])

            self.initialized_model_list = None
            self.grid_searched_best_model_list = None

        except Exception as e:
            raise HousingException(e, sys) from e

    @staticmethod
    def update_property_of_class(instance_ref:object, property_data: dict):
        """ 
        initialize parameters of Modules 
        """
        try:
            if not isinstance(property_data, dict):
                raise Exception(f"'property_data' parameter required to dictionary, {property_data} its not a dictionary")
            print(f"property_data format -> {property_data}")
            for key, value in property_data.items():
                logging.info(f"Executing:$ {str(instance_ref)}.{key}={value}")
                setattr(instance_ref, key, value) # setattr(LinearRegression, fit_intercept=True)
                # setattr is responsible for if you want to set dynamically the parameters of any ML model class
                # you can use "setattr" function {check the notebook inside imporli_setattribt.ipynb there explained 
                # "setattr" fun similar
            return instance_ref
        except Exception as e:
            raise HousingException(e, sys) from e

    @staticmethod
    def read_params(config_path: str) -> dict:
        """
        read the yaml file and returns 
        the yamle file as dictionary
        """
        try:
            with open(config_path) as yaml_file:
                config:dict = yaml.safe_load(yaml_file)
            return config
        except Exception as e:
            raise HousingException(e, sys) from e
        

    @staticmethod
    def class_for_name(module_name:str, class_name:str):
        """
        "class_for_name" is responsible for importing "modules" like ex 
        {sklearn.linear_model import LinearRegression}
                        or
        {from sklearn.model_selection import GridSearchCV } ... etc ...
        """
        try:
            # load the module, will raise ImportError if module cannot be loaded
            module = importlib.import_module(module_name)
            # get the class, will raise AttributeError if class cannot be found
            logging.info(f"Executing command: from {module} import {class_name}")
            class_ref = getattr(module, class_name) # this getattr fun will give you refference to the imported class that we want
            return class_ref
        except Exception as e:
            raise HousingException(e, sys) from e

    def execute_grid_search_operation(self, initialized_model: InitializedModelDetail, 
                                      input_feature,
                                      output_feature) -> GridSearchedBestModel:
        """
        excute_grid_search_operation(): function will perform paramter search operation and
        it will return you the best optimistic  model with best paramter:
        estimator: Model object
        param_grid: dictionary of paramter to perform search operation
        input_feature: your all input features
        output_feature: Target/Dependent features
        ================================================================================
        return: Function will return GridSearchOperation object
        """
        try:
            # instantiating GridSearchCV class
            
           # here "class_for_name" is responsible for importing "class: GridSearchCV & module: sklearn.model_selection"
           #  like ex {from sklearn.model_selection import GridSearchCV }
            grid_search_cv_ref = ModelFactory.class_for_name(module_name=self.grid_search_cv_module,
                                                             class_name=self.grid_search_class_name
                                                             )

            grid_search_cv = grid_search_cv_ref(estimator=initialized_model.model, 
                                                param_grid=initialized_model.param_grid_search) 
            
            #logging.info(f"grid_search_cv(estimator=,param_grid= ) = [{grid_search_cv}]")
            
            grid_search_cv = ModelFactory.update_property_of_class(instance_ref=grid_search_cv,
                                                                   property_data=self.grid_search_property_data)

            
            logging.info(f"All models and parameters and GridSearchCV parameters are set now FIT the DATASET\n\n")
            message = f'{"="* 30} f"Training [ {type(initialized_model.model).__name__} ] Started" {"="*30}'
            logging.info(f"message = {message}")
            grid_search_cv.fit(input_feature, output_feature)
            message = f'{"="* 30} f"Training [ {type(initialized_model.model).__name__} ] completed." {"="*30}'
            logging.info(message)

            grid_searched_best_model = GridSearchedBestModel(model_serial_number=initialized_model.model_serial_number,
                                                             model=initialized_model.model,
                                                             best_model=grid_search_cv.best_estimator_,
                                                             best_parameters=grid_search_cv.best_params_,
                                                             best_score=grid_search_cv.best_score_
                                                             )
            
            return grid_searched_best_model
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_initialized_model_list(self) -> List[InitializedModelDetail]:
        """
        This function will return a list of model details.
        return List[ModelDetail]
        """
        try:
            initialized_model_list = []
            for model_serial_number in self.models_initialization_config.keys():

                model_initialization_config = self.models_initialization_config[model_serial_number]
        # "class_for_name" is responsible for importing "Models" like ex {sklearn.linear_model import LinearRegression}
                model_obj_ref = ModelFactory.class_for_name(module_name=model_initialization_config[MODULE_KEY],
                                                            class_name=model_initialization_config[CLASS_KEY]
                                                            )
                model = model_obj_ref() # model is nothing but object of the Class. ex like {model = LinearRegression()}
                
                if PARAM_KEY in model_initialization_config:
                    model_obj_property_data = dict(model_initialization_config[PARAM_KEY])
                    model = ModelFactory.update_property_of_class(instance_ref=model, # model  = LinearRegression()
                                                                  property_data=model_obj_property_data) # param_grid_search {fit_intercept :True}

                param_grid_search = model_initialization_config[SEARCH_PARAM_GRID_KEY]
                model_name = f"{model_initialization_config[MODULE_KEY]}.{model_initialization_config[CLASS_KEY]}"

                model_initialization_config = InitializedModelDetail(model_serial_number=model_serial_number,
                                                                     model=model,
                                                                     param_grid_search=param_grid_search,
                                                                     model_name=model_name
                                                                     )

                initialized_model_list.append(model_initialization_config)

            self.initialized_model_list = initialized_model_list
            return self.initialized_model_list
        except Exception as e:
            raise HousingException(e, sys) from e

    def initiate_best_parameter_search_for_initialized_model(self, 
                                                             initialized_model: InitializedModelDetail,
                                                             input_feature,
                                                             output_feature) -> GridSearchedBestModel:
        """
        initiate_best_model_parameter_search(): function will perform paramter search operation and
        it will return you the best optimistic  model with best paramter:
        estimator: Model object
        param_grid: dictionary of paramter to perform search operation
        input_feature: your all input features
        output_feature: Target/Dependent features
        ================================================================================
        return: Function will return a GridSearchOperation
        """
        try:
            return self.execute_grid_search_operation(initialized_model=initialized_model,
                                                      input_feature=input_feature,
                                                      output_feature=output_feature)
        except Exception as e:
            raise HousingException(e, sys) from e

    def initiate_best_parameter_search_for_initialized_models(self,
                                                              initialized_model_list: List[InitializedModelDetail],
                                                              input_feature,
                                                              output_feature) -> List[GridSearchedBestModel]:
        """
        This functon is only for more then 1 model (2 ,3 4 .... models) to search 
        GridSearch best parameters, search for initialised models
        """

        try:
            self.grid_searched_best_model_list = []
            for initialized_model_list in initialized_model_list:
                grid_searched_best_model = self.initiate_best_parameter_search_for_initialized_model(
                    initialized_model=initialized_model_list,
                    input_feature=input_feature,
                    output_feature=output_feature
                )
                self.grid_searched_best_model_list.append(grid_searched_best_model)
            return self.grid_searched_best_model_list
        except Exception as e:
            raise HousingException(e, sys) from e

    @staticmethod
    def get_model_detail(model_details: List[InitializedModelDetail],
                         model_serial_number: str) -> InitializedModelDetail:
        """
        This function return ModelDetail
        """
        try:
            for model_data in model_details:
                if model_data.model_serial_number == model_serial_number:
                    return model_data
        except Exception as e:
            raise HousingException(e, sys) from e

    @staticmethod
    def get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list: List[GridSearchedBestModel],
                                                          base_accuracy=0.6
                                                          ) -> BestModel:
        """
        After the GridSearch for every model it will compare the best parameters and score
        based on that it will give the best_model after GridSearch,
        """
        try:
            best_model = None
            for grid_searched_best_model in grid_searched_best_model_list:
                if base_accuracy < grid_searched_best_model.best_score:
                    logging.info(f"Acceptable model found:{grid_searched_best_model}")
                    base_accuracy = grid_searched_best_model.best_score

                    best_model = grid_searched_best_model
            if not best_model:
                raise Exception(f"None of Model has 'base accuracy': {base_accuracy}")
            logging.info(f"Best model: {best_model}")
            return best_model
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_best_model(self, X, y,base_accuracy:float=0.6) -> BestModel:
        """
        this get_best_model function will work on Training dataset 
        inside this function we have functions like 
        1. get_initialized_model_list()
        2. initiate_best_parameter_search_for_initialized_models( take 3 parameters:1 initialized_model_list
                                                                                    2 input_feature
                                                                                    3 output_feature )

        3 . get_best_model_from_grid_searched_best_model_list( take 2 parameters  : 1 grid_searched_best_model_list
                                                                                    2 base_accuracy=base_accuracy )
        """
        try:
            logging.info("Started Initializing model from config file -> { model.yaml }")
            initialized_model_list = self.get_initialized_model_list() 
            logging.info(f"Initialized model list: {initialized_model_list} lennght = {len(initialized_model_list)}")

            grid_searched_best_model_list = self.initiate_best_parameter_search_for_initialized_models(
                                                 initialized_model_list=initialized_model_list,
                                                 input_feature=X,
                                                 output_feature=y
                                                )
            return ModelFactory.get_best_model_from_grid_searched_best_model_list(grid_searched_best_model_list,
                                                                                  base_accuracy=base_accuracy)
        except Exception as e:
            raise HousingException(e, sys)  

            
   
