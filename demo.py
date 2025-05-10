from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
def main():
    try:

        # +++++++++get_data_validation_config() Check++++++++++
        # data_validation_config = Configuration().get_data_validation_config()
        # print(data_validation_config)
        # +++++++++get_data_validation_config() Done++++++++++

        # +++++++++get_data_ingestion_config() Check++++++++++
        #data_ingestion_config = Configuration().get_data_ingestion_config()
        #print(data_ingestion_config)
        # +++++++++get_data_ingestion_config() Done++++++++++



        logging.info(f"{'='*10}Pipeline is Started{'='*10} \n")
        pipeline = Pipeline()
        pipeline.run_pipeline()
        logging.info(f"{'='*10}Pipeline is completed.{'='*10} \n")
    except Exception as e:
            logging.error(f"Error is  ={e} ")
            print("exception = ",e)
    

if __name__=="__main__":
    main()

