from flask import Flask, jsonify, redirect, render_template, request
import pandas as pd

from utils import get_demographics, get_genres, get_num_episodes, get_score

app = Flask(__name__)
csv_name="static/csv/anime.csv"

@app.get("/")
def index():
    return redirect("/dashboard1")

@app.get("/dashboard1")
def dashboard1():
    args=request.args
    data=pd.read_csv(csv_name)

    filters=args.getlist("filters")
    
    #may change these 2 if I have time
    if "year" in filters:
        data=data.query(f"start_year=={args["year"]}")
    if "season" in filters:
        data=data.query(f"start_season=={args["season"]}")

    score=get_score(data)
    num_episodes=get_num_episodes(data)
    genres=get_genres(data)
    demographics=get_demographics(data)

    return render_template("dashboard1.html",dashboard_url="/dashboard1",score=score,num_episodes=num_episodes,genres=genres,demographics=demographics)

@app.get("/dashboard2")
def dashboard2():
    return render_template("dashboard2.html",dashboard_url="/dashboard2")

#return dashboard 1
@app.get("/api/dashboard1")
def dashboard1_graphs():
    args=request.args
    data=pd.read_csv(csv_name)
    
    #may change these 2 if I have time
    if "year" in args:
        data=data.query(f"start_year=={args["year"]}")
    if "season" in args:
        data=data.query(f"start_season=={args["season"]}")

    score=get_score(data)
    num_episodes=get_num_episodes(data)
    genres=get_genres(data)
    demographics=get_demographics(data)

    return jsonify({
        "score":score,
        "num_episodes":num_episodes,
        "genres":genres,
        "demographics":demographics
    })

@app.get("/api/score")
def score():
    args=request.args
    data=pd.read_csv(csv_name)
    
    #may change these 2 if I have time
    if "year" in args:
        data=data.query(f"start_year=={args["year"]}")
    if "season" in args:
        data=data.query(f"start_season=={args["season"]}")
    
    return jsonify(get_score(data))

@app.get("/api/episodes")
def episodes():
    args=request.args
    data=pd.read_csv(csv_name)
    
    #may change these 2 if I have time
    if "year" in args:
        data=data.query(f"start_year=={args['year']}")
    if "season" in args:
        data=data.query(f"start_season=={args['season']}")
    
    return jsonify(get_num_episodes(data))

@app.get("/api/genres")
def genres():
    args=request.args
    data=pd.read_csv(csv_name)
    
    #may change these 2 if I have time
    if "year" in args:
        data=data.query(f"start_year=={args['year']}")
    if "season" in args:
        data=data.query(f"start_season=={args['season']}")
    
    return jsonify(get_genres(data))

@app.get("/api/demographics")
def demographics():
    args=request.args
    data=pd.read_csv(csv_name)
    
    #may change these 2 if I have time
    if "year" in args:
        data=data.query(f"start_year=={args['year']}")
    if "season" in args:
        data=data.query(f"start_season=={args['season']}")
    
    return jsonify(get_demographics(data))