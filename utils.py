from ast import literal_eval
from collections import defaultdict,Counter


def get_score(data):
    return data["score"].dropna().to_numpy().tolist()

def get_num_episodes(data):
    return Counter(data["episodes"].astype('Int64').dropna().to_numpy().tolist())

def get_genres(data):
    return count_occurrences(data["genres"].apply(lambda l:literal_eval(l)).to_numpy().tolist())
    
def get_demographics(data):
    return count_occurrences(data["demographics"].apply(lambda l:literal_eval(l)).to_numpy().tolist())

def count_occurrences(col):
    occurances=defaultdict(int)
    for lst in col:
        for entry in lst:
            occurances[entry]+=1

    return occurances