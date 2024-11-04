from flask import Flask, request

from utils import load_dataset

app = Flask(__name__)

#return dashboard 1
@app.route("/")
def home():
    args=request.json
    data=load_dataset()
    
    if "year" in args:
        data=filter(data,f"year=={args["year"]}")