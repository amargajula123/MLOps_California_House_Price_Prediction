from flask import Flask
from housing.logger import logging
import sys
from housing.exception import HousingException

#deploy
app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    try:
        raise Exception("we are testing our custome Exception")
    except Exception as e:
        housing = HousingException(e,sys)
        logging.info(housing.error_message)
        logging.info("we are testing logging module")

    return "Practicing ML Project again "

if __name__=="__main__":
    app.run(debug=True)