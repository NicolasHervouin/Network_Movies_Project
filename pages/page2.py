from dash import html, dcc, callback, Output, Input, State, register_page
from utils.image_utils import get_first_google_image
from utils.graph_utils import draw_interactive_graph_with_focus
from data.load_data import load_movies_data, load_graph_data2
import plotly.graph_objs as go
from utils.graph_utils import get_recommendation

# Register the page for multi-page navigation
register_page(__name__, path="/page2")

# Load movie data and graph data
titles_df = load_movies_data()
G_movies_actors = load_graph_data2()

# Create the options for the dropdown menu
film_titles_options = [{'label': str(title), 'value': str(title)} for title in titles_df['title'].dropna().tolist()]

# Define a default film
default_film = film_titles_options[0]['value'] if film_titles_options else None

# Layout for Page 2
layout = html.Div([
    html.H2("DashBoard 2 : 1st degree network of a movie"),

    # Dropdown to select a movie
    html.Div([
        dcc.Dropdown(
            id='film-dropdown-page2',
            options=film_titles_options,
            value=default_film,
            placeholder='Sélectionnez un film',
            style={'width': '80%', 'font-family': 'Arial, sans-serif'}
        ),
        html.Button('Rechercher', id='search-button-page2', n_clicks=0, style={
            'background-color': '#27AE60', 'color': 'white', 'border': 'none', 'padding': '10px 20px', 
            'border-radius': '5px', 'font-family': 'Arial, sans-serif', 'cursor': 'pointer',
            'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.3)', 'margin-left': '10px'
        })
    ], style={
        'background-color': '#F7F9F9', 'color': 'black', 'width': '100%', 'height': '10vh', 
        'margin-bottom': '5px', 'border-radius': '10px', 
        'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.5)', 'padding': '10px', 
        'font-family': 'Arial, sans-serif', 'display': 'flex', 'align-items': 'center'
    }),

    # Container for image and graph side by side
    html.Div([
        # Poster display (Block 2) with reduced size
        html.Div([
            html.Img(id='film-poster-page2', src='', style={'width': '50%', 'height': '100%', 'border-radius': '10px'})
        ], style={
            'background-color': '#ECF0F1', 'color': 'black', 'width': '30%', 'height': '30vh', 
            'margin-bottom': '5px', 'border-radius': '10px', 'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.5)',
            'text-align': 'center', 'display': 'inline-block', 'vertical-align': 'top'
        }),

        # Graph showing the movie network (Block 3)
        html.Div([
            dcc.Graph(id='interactive-graph-page2', style={'height': '30vh', 'width': '100%'})
        ], style={'display': 'inline-block', 'vertical-align': 'top', 'width': '68%'})
    ], style={'display': 'flex', 'justify-content': 'space-between'}),

    html.Div([
    # Movie details (Block 6)
    html.Div(id='film-details-page2', style={
        'background-color': '#3498DB', 'color': 'white', 'width': '48%', 'height': '32vh', 
        'margin-bottom': '5px', 'border-radius': '10px', 'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.5)', 
        'padding': '10px', 'font-family': 'Arial, sans-serif', 'overflow-y': 'auto', 'display': 'inline-block'
    }),
    
    # Movie recommendations (Block 7)
    html.Div(id='film-recommendations', style={
        'background-color': '#8498CB', 'color': 'white', 'width': '48%', 'height': '32vh', 
        'margin-bottom': '5px', 'border-radius': '10px', 'box-shadow': '2px 2px 5px rgba(0, 0, 0, 0.5)', 
        'padding': '10px', 'font-family': 'Arial, sans-serif', 'overflow-y': 'auto', 'display': 'inline-block',
        'margin-left': '2%'
    })
    ], style={'display': 'flex', 'justify-content': 'space-between'}),
])

# Callback to update the poster, movie details, and the graph
@callback(
    [Output('film-poster-page2', 'src'),
     Output('film-details-page2', 'children'),
     Output('interactive-graph-page2', 'figure'),
     Output('film-recommendations', 'children')],
    [Input('search-button-page2', 'n_clicks')],
    [State('film-dropdown-page2', 'value')]
)

def update_image_details_and_graph(n_clicks, selected_film):
    if n_clicks > 0 or selected_film:
        # Fetch image
        image_url = get_first_google_image(selected_film)

        # Fetch film details
        film_info = titles_df[titles_df['title'] == selected_film].iloc[0]
        film_details = html.Div([
            html.P(f"Titre: {film_info['title']}", style={'font-weight': 'bold'}),
            html.P(f"Réalisateur: {film_info['director']}"),
            html.P(f"Distribution: {film_info['cast']}"),
            html.P(f"Pays: {film_info['country']}"),
            html.P(f"Année de sortie: {film_info['release_year']}"),
            html.P(f"Durée: {film_info['duration']}"),
            html.P(f"Genre: {film_info['listed_in']}"),
            html.P(f"Description: {film_info['description']}")
        ], style={'font-family': 'Arial, sans-serif'})

        # Create subgraph for the movie and its connected nodes (actors, other movies)
        neighbors = list(G_movies_actors.neighbors(selected_film)) if selected_film in G_movies_actors else []
        subgraph = G_movies_actors.subgraph([selected_film] + neighbors)
        graph_figure = draw_interactive_graph_with_focus(subgraph, focus=selected_film)

        # Get recommendations as DataFrame
        film_reco = get_recommendation(selected_film, G_movies_actors, titles_df)
        
        # Take the first 5 rows of the DataFrame
        film_reco_top5 = film_reco.head(5)
        
        # Convert the DataFrame rows to Dash components (html.Table or html.Div)
        table_header = [
            html.Thead(html.Tr([html.Th(col) for col in film_reco_top5.columns]))
        ]
        table_body = [
            html.Tbody([
                html.Tr([html.Td(film_reco_top5.iloc[i][col]) for col in film_reco_top5.columns])
                for i in range(len(film_reco_top5))
            ])
        ]
        film_reco_table = html.Table(table_header + table_body, style={'width': '100%', 'font-family': 'Arial, sans-serif'})

        return image_url, film_details, graph_figure, film_reco_table

    return '', '', go.Figure(), html.P("No recommendations available")


