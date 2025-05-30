from housing.logger import logging
from housing.exception import HousingException
from housing.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact 
from housing.entity.config_entity import ModelPusherConfig
import os, sys
import shutil


class ModelPusher:

    def __init__(self, model_pusher_config: ModelPusherConfig,
                 model_evaluation_artifact: ModelEvaluationArtifact  
                 ):# model_evaluation_artifact for "evaluated_model_path" which is newly trainer model
        try:
            logging.info(f"{'=' * 30}Model Pusher log started.{'=' * 30} ")
            self.model_pusher_config = model_pusher_config
            self.model_evaluation_artifact = model_evaluation_artifact

        except Exception as e:
            raise HousingException(e, sys) from e

    def export_model(self) -> ModelPusherArtifact:
        try:
            evaluated_model_file_path = self.model_evaluation_artifact.evaluated_model_path # newly trained best model file path
            export_dir = self.model_pusher_config.export_dir_path #till the time stamp folder
            model_file_name = os.path.basename(evaluated_model_file_path) # model.pkl
            export_model_file_path = os.path.join(export_dir, model_file_name)
            logging.info(f"Exporting model file: [{export_model_file_path}]")
            os.makedirs(export_dir, exist_ok=True)

            # copying data 
            shutil.copy(src=evaluated_model_file_path, dst=export_model_file_path)
            #we can call a function to save model to Azure blob storage/ google cloud strorage / s3 bucket

            logging.info(
                f"Trained model: {evaluated_model_file_path} is copied in export dir:[{export_model_file_path}]")

            model_pusher_artifact = ModelPusherArtifact(is_model_pusher=True,
                                                        export_model_file_path=export_model_file_path
                                                        )
            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            return model_pusher_artifact
        except Exception as e:
            raise HousingException(e, sys) from e

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            return self.export_model()
        except Exception as e:
            raise HousingException(e, sys) from e

    def __del__(self):
        logging.info(f"{'=' * 20}Model Pusher log completed.{'=' * 20}")


# model pusher component will take the newly trained model / best performing Model and it will 
# push that model into Saved_Model_directory, or there is also one onther scenario to push that
# model into the cloud,

        # def upload_trained_modele_file_to_the_cloud(self):
        # """
        # this fuction will helps you to save
        # your trained model file to the cloud.
        # """
        # try:
        #     pass
        # except Exception as e:
        #     raise HousingException(e,sys) from e