from housing.pipeline.pipeline import Pipeline
from housing.exception import HousingException
from housing.logger import logging
from housing.config.configuration import Configuration
import os


# ✅ Force early import of Plotly and IPython to avoid shutdown errors
import plotly.io as pio
import IPython.core.display  # Force import so it's not delayed
pio.renderers.default = "svg"  # or 'browser' or 'notebook' based on your use case



def main():
    try:
        config_path = os.path.join("config", "config.yaml")
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        pipeline.start()
        logging.info("main function execution completed")
    except Exception as e:
        logging.error(f"{e}")
        print(e)

if __name__ == "__main__":
    main()

# def main():
#     try:

#         config_file_path = os.path.join("config","config.yaml")
#         pipeline = Pipeline(config=Configuration(config_file_path=config_file_path))
#         pipeline.start() # this start function will actually call run() internally
#         logging.info("main function execution completed")

        
#     except Exception as e:
#             logging.error(f"Error is  ={e} ")
#             print("exception = ",e)
    

# if __name__=="__main__":
#     main()

