from dash import html, dcc, register_page
from utils.graph_utils import draw_interactive_graph_with_focus
from data.load_data import load_graph_data, load_graph_data3

# Register this page
register_page(__name__, path="/page1")

# Load the graph data (or any other data relevant to this page)
G_movies_actors = load_graph_data()
figure = load_graph_data3()

# Page 1 layout with Tabs for Graph 1 and Graph 2
layout = html.Div([
    html.H2("DashBoard 1: Network for 2000 to 2005 movies"),
    
    dcc.Tabs([
        dcc.Tab(label='Graph 1: Interactive Movie-Actor Network', children=[
            dcc.Graph(
                id='graph1-page1',
                figure=draw_interactive_graph_with_focus(G_movies_actors)
            ),
            html.Div("The graph visualizes the relationships between movies and actors (Graph 1).")
        ]),
        
        dcc.Tab(label='Graph 2: Static Movie Network', children=[
            dcc.Graph(
                id='graph2-page1',
                figure=figure
            ),
            html.Div("This graph visualizes another aspect of the movie network (Graph 2).")
        ])
    ])
])
