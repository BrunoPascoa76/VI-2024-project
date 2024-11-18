from ast import literal_eval
from collections import OrderedDict, defaultdict
from flask import Flask, jsonify, redirect, render_template, request
import pandas as pd

from utils import get_demographics, get_genres, get_num_episodes, get_score

app = Flask(__name__)
csv_name="static/csv/anime.csv"

@app.get("/")
def index():
    return redirect("/home")

@app.get("/home")
def home():
    args=request.args
    data=pd.read_csv(csv_name)


    years=sorted(data["start_year"].astype('Int64').dropna().unique().tolist())

    current_filters=dict()

    if "year" in args and args["year"]!="":
        data=data.query(f"start_year=={args['year']}")
        current_filters["year"]=args["year"]

    if "season" in args and args["season"]!="":
        data=data.query(f"start_season=='{args['season']}'")
        current_filters["season"]=int(args["season"])

    genres=[]
    genre_lists=data["genres"].apply(lambda l:literal_eval(l)).to_numpy().tolist()
    for genre_list in genre_lists:
        for genre in genre_list:
            genres.append(genre)

    demographics=[]
    demographics_lists=data["demographics"].apply(lambda l:literal_eval(l)).to_numpy().tolist()
    for demographics_list in demographics_lists:
        for demographic in demographics_list:
            demographics.append(demographic)


    return render_template(
        "homepage.html",
        years=years,genres=list(set(genres)),
        demographics=list(set(demographics)),
        filters=current_filters)

@app.get("/dashboard1")
def dashboard1():
    args=request.args
    data=pd.read_csv(csv_name)

    filters=args.getlist("filters")
    
    #may change these 2 if I have time
    if "year" in filters:
        data=data.query(f"start_year=={args["year"]}")
    if "season" in filters:
        data=data.query(f"start_season=='{args["season"]}'")

    score=get_score(data)
    num_episodes=get_num_episodes(data)
    genres=get_genres(data)
    demographics=get_demographics(data)

    years=data["start_year"].astype('Int64').dropna().unique().tolist()
    years=sorted(years)

    return render_template("dashboard1.html",dashboard_url="/dashboard1",years=years,score=score,num_episodes=num_episodes,genres=genres,demographics=demographics)

@app.get("/dashboard2")
def dashboard2():
    args=request.args
    data=pd.read_csv(csv_name)
    top_amount=10

    if "year" in args:
        data=data.query(f"start_year=='{args['year']}'")
    if "season" in args:
        data=data.query(f"start_season=='{args['season']}'")
    if "top_amount" in args:
        top_amount=int(args["top_amount"])

    data=data.dropna()
    top_anime=data.dropna().nlargest(top_amount, "score").sort_values("score",ascending=False).values.tolist()

    genres_score=defaultdict(int)
    genres_count=get_genres(data)
    idx=0
    for genre in data["genres"].apply(lambda l:literal_eval(l)).to_numpy().tolist():
        for g in genre:
            genres_score[g]+=data["score"].iloc[idx]
        idx+=1

    genres_score={k:v/genres_count[k] for k,v in genres_score.items()}
    df=pd.DataFrame(genres_score.items(),columns=["genre","score"])

    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    top_genres=df.dropna().nlargest(top_amount, "score").sort_values("score",ascending=False).to_numpy().tolist()#

    years=data["start_year"].astype('Int64').dropna().unique().tolist()
    years=sorted(years)

    return render_template("dashboard2.html",top_anime=top_anime,top_genres=top_genres,years=years,dashboard_url="/dashboard2")
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
        data=data.query(f"start_year=='{args["year"]}'")
    if "season" in args:
        data=data.query(f"start_season=='{args["season"]}'")
    
    return jsonify(get_score(data))

@app.get("/api/episodes")
def episodes():
    args=request.args
    data=pd.read_csv(csv_name)
    
    #may change these 2 if I have time
    if "year" in args:
        data=data.query(f"start_year=='{args['year']}'")
    if "season" in args:
        data=data.query(f"start_season=='{args['season']}'")
    
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

@app.get("/api/top_anime")
def top_anime():
    args=request.args
    data=pd.read_csv(csv_name)
    top_amount=10

    if "year" in args:
        data=data.query(f"start_year=={args['year']}")
    if "season" in args:
        data=data.query(f"start_season=={args['season']}")
    if "top_amount" in args:
        top_amount=int(args["top_amount"])

    data=data.dropna().nlargest(top_amount, "score").sort_values("score",ascending=False)
    return data.to_dict(orient="records")

@app.get("/api/top_genres")
def top_genres():
    args=request.args
    data=pd.read_csv(csv_name)
    top_amount=10

    if "year" in args:
        data=data.query(f"start_year=={args['year']}")
    if "season" in args:
        data=data.query(f"start_season=={args['season']}")
    if "top_amount" in args:
        top_amount=int(args["top_amount"])

    data=data.dropna()

    genres_score=defaultdict(int)
    genres_count=get_genres(data)
    idx=0
    for genre in data["genres"].apply(lambda l:literal_eval(l)).to_numpy().tolist():
        for g in genre:
            genres_score[g]+=data["score"].iloc[idx]
        idx+=1

    genres_score={k:v/genres_count[k] for k,v in genres_score.items()}
    df=pd.DataFrame(genres_score.items(),columns=["genre","score"])

    return df.nlargest(top_amount, "score").sort_values("score",ascending=False).to_dict(orient="records")

@app.get("/api/anime/<int:anime_id>/details")
def anime_details(anime_id):
    data=pd.read_csv(csv_name)
    result=data[data["anime_id"]==anime_id].to_dict(orient="records")[0]
    result.pop("Unnamed: 0")
    result["genres"] = literal_eval(result["genres"])
    result["demographics"] = literal_eval(result["demographics"])
    return result