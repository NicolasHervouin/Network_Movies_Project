from dash import html, dcc, callback, Output, Input, register_page
from utils.graph_utils import draw_interactive_sub_graph_with_legend, get_all_adj_nodes
from data.load_data import load_movies_data, load_graph_data, load_graph_data2
import plotly.graph_objs as go

# Register this page
register_page(__name__, path="/page3")

# Load movie data and graph data
titles_df = load_movies_data()
G_movies_actors = load_graph_data()
G = load_graph_data2()

film1 = load_movies_data().iloc[0]['title']
film2 = load_movies_data().iloc[-1]['title']

# Create options for the dropdowns
film_titles_options = [{'label': str(title), 'value': str(title)} for title in titles_df['title'].dropna().tolist()]

# Layout for Page 3
layout = html.Div([
    html.H2("DashBoard 3: Network between 2 Movies"),
    
    # Dropdown for selecting the first movie
    html.Div([
        dcc.Dropdown(
            id='movie-1-dropdown',
            options=film_titles_options,
            value=film1,
            placeholder='Select the first movie',
            style={'width': '45%', 'display': 'inline-block', 'margin-right': '10px'}
        ),
        
        # Dropdown for selecting the second movie
        dcc.Dropdown(
            id='movie-2-dropdown',
            options=film_titles_options,
            value=film2,
            placeholder='Select the second movie',
            style={'width': '45%', 'display': 'inline-block'}
        ),
    ], style={'text-align': 'center', 'margin-bottom': '20px'}),
    
    # Graph display area
    dcc.Graph(id='movie-network-graph', style={'height': '80vh'})
])

# Callback to update the graph based on selected movies
@callback(
    Output('movie-network-graph', 'figure'),
    [Input('movie-1-dropdown', 'value'), Input('movie-2-dropdown', 'value')]
)
def update_movie_network_graph(movie1, movie2):
    # Si pas de films sélectionnés, ne rien afficher
    if not movie1 or not movie2:
        return go.Figure()

    # List of selected movies
    list_in = [movie1, movie2]

    # Check if both movies exist in the graph
    if all(film in G.nodes() for film in list_in):
        # Get the subgraph for the selected movies and their connections
        sub_graph = get_all_adj_nodes(list_in, G)

        # If the subgraph contains nodes, render the graph
        if len(sub_graph) > 1:
            fig = draw_interactive_sub_graph_with_legend(sub_graph, list_in, G)
            return fig
        else:
            return go.Figure()  # Return an empty figure if no connections found
    else:
        return go.Figure().add_annotation(text="No connections found between the selected movies.",
                           xref="paper", yref="paper", showarrow=False, 
                           font=dict(size=16, color="red"), x=0.5, y=0.5)
