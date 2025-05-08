from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging

def main():
    try:
        logging.info(f"{'='*10}Pipeline is Started{'='*10} \n")
        pipeline = Pipeline()
        pipeline.run_pipeline()
        logging.info(f"{'='*10}Pipeline is completed.{'='*10} \n")
    except Exception as e:
            logging.error(f"Error is  ={e} ")
            print("exception = ",e)
    

if __name__=="__main__":
    main()

