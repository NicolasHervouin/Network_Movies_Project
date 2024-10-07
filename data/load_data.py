import pandas as pd
import networkx as nx
import plotly.io as pio

def load_movies_data():
    df1 = pd.read_csv('data/amazon_prime_titles.csv') 
    df2 = pd.read_csv('data/disney_plus_titles.csv') 
    df3 = pd.read_csv('data/netflix_titles.csv') 
    
    df = pd.concat([df1, df2, df3], ignore_index=True)
    df = df[(df['release_year'] >= 2000) & (df['release_year'] <= 2005)]

    return df

def load_graph_data():
    return nx.read_graphml("data/movies_actors_graph.graphml")

def load_graph_data2():
    return nx.read_graphml("data/movies_actors_graph2.graphml")

def load_graph_data3():
    return pio.read_json("data/figure.json")