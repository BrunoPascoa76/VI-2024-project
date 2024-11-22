from ast import literal_eval
from collections import defaultdict,Counter


def get_score(data):
    return data["score"].dropna().to_numpy().tolist()

def get_num_episodes(data):
    return Counter(data["episodes"].astype('Int64').dropna().to_numpy().tolist())

def get_genres(data,metric="quantity"):
    if metric=="quantity": 
        return count_occurrences(data["genres"].apply(lambda l:literal_eval(l)).to_numpy().tolist())
    else:
        data["genres"]=data["genres"].apply(lambda l:literal_eval(l))
        return data.explode("genres").dropna().groupby("genres")[metric].mean().sort_values(ascending=False).to_dict()
    
def get_demographics(data,metric="quantity"):
    if metric=="quantity":
        return count_occurrences(data["demographics"].apply(lambda l:literal_eval(l)).to_numpy().tolist())
    else:
        data["demographics"]=data["demographics"].apply(lambda l:literal_eval(l))
        return data.explode("demographics").dropna().groupby("demographics")[metric].mean().sort_values(ascending=False).to_dict()

def count_occurrences(col):
    occurances=defaultdict(int)
    for lst in col:
        for entry in lst:
            occurances[entry]+=1

    return occurances