from ast import literal_eval
import pandas as pd

def load_dataset():
    return pd.read_csv("static/csv/anime.csv")

def select(df,columns):
    return df.illoc[columns]

def filter(df,query):
    return df.query(query)

def sort(df,sort_cols):
    return df.sort_by(by=sort_cols)

def explode(df,col_name):
    return df.explode(col_name)

def unstringify(df,col_name):
    df[col_name]=df[col_name].apply(literal_eval)

def count(df,col_name):
    return df[col_name].value_counts()

def set