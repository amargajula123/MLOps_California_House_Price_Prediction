from flask import Flask
from housing.logger import logging

#deploy
app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    logging.info("we are testing logging module")
    return "Practicing ML Project again"

if __name__=="__main__":
    app.run(debug=True)