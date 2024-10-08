from dash import html, register_page

register_page(__name__, "/")

# Layout for the home page
layout = html.Div([
    html.H2("Projet d'Analyse des réseaux sociaux", style={'text-align': 'center'}),
    html.P("This project explores various network structures, including full network views, movie networks, and more.", 
           style={'text-align': 'center', 'font-family': 'Arial, sans-serif'}),
])
