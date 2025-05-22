import os
import sys

from housing.exception import HousingException
from housing.util.util import load_object

import pandas as pd


class HousingData:

    def __init__(self,
                 longitude: float,
                 latitude: float,
                 housing_median_age: float,
                 total_rooms: float,
                 total_bedrooms: float,
                 population: float,
                 households: float,
                 median_income: float,
                 ocean_proximity: str,
                 median_house_value: float = None
                 ):
        try:
            self.longitude = longitude
            self.latitude = latitude
            self.housing_median_age = housing_median_age
            self.total_rooms = total_rooms
            self.total_bedrooms = total_bedrooms
            self.population = population
            self.households = households
            self.median_income = median_income
            self.ocean_proximity = ocean_proximity
            self.median_house_value = median_house_value
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_housing_input_data_frame(self)->pd.DataFrame:
        """
        This funtion will take all the housing data values except "median_house_value"
        and gives you the DataFrame
        """

        try:
            housing_input_dict = self.get_housing_data_as_dict()
            return pd.DataFrame(housing_input_dict)
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_housing_data_as_dict(self):
        """
        This function takes the "housing_data" and give you 
        the "housing_data" as a dictionary
        """
        try:
            input_data = {
                "longitude": [self.longitude],
                "latitude": [self.latitude],
                "housing_median_age": [self.housing_median_age],
                "total_rooms": [self.total_rooms],
                "total_bedrooms": [self.total_bedrooms],
                "population": [self.population],
                "households": [self.households],
                "median_income": [self.median_income],
                "ocean_proximity": [self.ocean_proximity]}
            return input_data
        except Exception as e:
            raise HousingException(e, sys)


class HousingPredictor:
    """
    This HousingPredictor will look for the save_models and it will filter the
    saved_model like latest folder it will select and based on that folder location
    it will load the new trained model file and based on that Prediction will be happen
    """

    def __init__(self, model_dir: str):  # here its asking for the dir which is "Saved_model" dir
        try:
            self.model_dir = model_dir
        except Exception as e:
            raise HousingException(e, sys) from e

    def get_latest_model_path(self):
        """ 
        This function will help you to get latest model file path from
        "Saved_models" Directory so that we can loaad the latest model
        and do the prdiction 
        """
        try:
            folder_name = list(map(int, os.listdir(self.model_dir)))
            latest_model_dir = os.path.join(self.model_dir, f"{max(folder_name)}")
            file_name = os.listdir(latest_model_dir)[0]
            latest_model_path = os.path.join(latest_model_dir, file_name)
            return latest_model_path
        except Exception as e:
            raise HousingException(e, sys) from e

    def predict(self, X):
        """
        This Fuction will helps you to Predict the "Median House Value" 
        it takes : input futures of housing data 
        """
        try:
            model_path = self.get_latest_model_path()
            model = load_object(file_path=model_path)
            median_house_value = model.predict(X)
            return median_house_value
        except Exception as e:
            raise HousingException(e, sys) from e
