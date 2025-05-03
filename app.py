from flask import Flask

app=Flask(__name__)

@app.route("/",methods=['GET','POST'])
def index():
    return "Practicing ML Project again"

if __name__=="__main__":
    app.run(debug=True)