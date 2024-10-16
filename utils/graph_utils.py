import networkx as nx
import plotly.graph_objs as go
import pandas as pd
import math as math

def draw_interactive_graph_with_focus(G, focus=None):
    pos = nx.spring_layout(G)
    x_nodes = [pos[node][0] for node in G.nodes()]
    y_nodes = [pos[node][1] for node in G.nodes()]

    x_edges = []
    y_edges = []
    for edge in G.edges():
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]

    edge_trace = go.Scatter(
        x=x_edges, y=y_edges,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    node_trace = go.Scatter(
        x=x_nodes, y=y_nodes,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='YlGnBu',
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
        )
    )

    node_adjacencies = []
    node_text = []
    for node in G.nodes():
        node_adjacencies.append(len(list(G.neighbors(node))))
        node_text.append(f'{node} - {len(list(G.neighbors(node)))} connections')

    node_trace.marker.color = node_adjacencies
    node_trace.text = node_text

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title=f'Graph with Focus on {focus}' if focus else 'Graph',
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False),
                        yaxis=dict(showgrid=False, zeroline=False))
                    )

    return fig

def get_all_adj_nodes(list_in,G):
    """
    Crée un ensemble contenant les nœuds d'entrée et tous leurs voisins dans le graphe G.
    
    Paramètres:
    - list_in: Une liste de nœuds (films, acteurs, etc.) pour lesquels on souhaite récupérer les voisins.
    
    Retour:
    - Une liste de tous les nœuds adjacents aux nœuds d'entrée dans le graphe.
    """
    sub_graph = set()  # Ensemble pour stocker les nœuds du sous-graphe
    
    for m in list_in:
        sub_graph.add(m)  # Ajouter le nœud initial
        # Ajouter tous les voisins du nœud (adjacents dans le graphe)
        for e in G.neighbors(m):
            sub_graph.add(e)
    
    # Retourner une liste des nœuds du sous-graphe
    return list(sub_graph)

def draw_interactive_sub_graph_with_legend(sub_graph, list_in, G):
    """
    Dessine un sous-graphe interactif en utilisant Plotly avec différentes couleurs pour les types de nœuds et ajoute une légende.
    
    Paramètres:
    - sub_graph: Liste des nœuds à inclure dans le sous-graphe.
    - list_in: Liste des nœuds principaux utilisés pour générer le sous-graphe (pour le titre dynamique).
    """
    # Extraire le sous-graphe du graphe global G
    subgraph = G.subgraph(sub_graph)
    
    # Générer une disposition des nœuds (positions des nœuds)
    pos = nx.spring_layout(subgraph, k=0.15, iterations=20)
    
    # Initialisation des listes pour les coordonnées des nœuds et des arêtes
    x_edges, y_edges = [], []
    
    # Remplir les coordonnées des arêtes
    for edge in subgraph.edges():
        x_edges += [pos[edge[0]][0], pos[edge[1]][0], None]
        y_edges += [pos[edge[0]][1], pos[edge[1]][1], None]
    
    # Tracer les arêtes
    edge_trace = go.Scatter(
        x=x_edges, y=y_edges,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    # Initialisation des listes de données pour les différentes catégories de nœuds
    categories = {
        "MOVIE": {"x": [], "y": [], "color": 'blue', "text": [], "name": "Film"},
        "PERSON": {"x": [], "y": [], "color": 'red', "text": [], "name": "Acteur / Réalisateur"},
        "CAT": {"x": [], "y": [], "color": 'green', "text": [], "name": "Catégorie (Genre)"},
        "COU": {"x": [], "y": [], "color": 'yellow', "text": [], "name": "Pays de production"},
        "SIMILAR": {"x": [], "y": [], "color": 'orange', "text": [], "name": "Film similaire"}
    }
    
    # Remplir les coordonnées et les textes pour chaque catégorie de nœud
    for node in subgraph.nodes():
        label = G.nodes[node]['label']
        if label in categories:
            categories[label]["x"].append(pos[node][0])
            categories[label]["y"].append(pos[node][1])
            categories[label]["text"].append(f'{label}: {node}')
    
    # Créer les traces pour chaque catégorie de nœud
    node_traces = []
    for category, data in categories.items():
        trace = go.Scatter(
            x=data["x"], y=data["y"],
            mode='markers',
            hoverinfo='text',
            marker=dict(
                color=data["color"],
                size=10,
                line=dict(width=2)),
            text=data["text"],
            name=data["name"]  # Légende associée à chaque catégorie
        )
        node_traces.append(trace)
    
    # Créer la figure avec Plotly
    fig = go.Figure(data=[edge_trace] + node_traces,
                    layout=go.Layout(
                        title=f"Graphe des connexions cinématographiques pour {', '.join(list_in)}",
                        titlefont_size=16,
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, visible=False),
                        yaxis=dict(showgrid=False, zeroline=False, visible=False)
                    )
    )
    
    return fig
    
def get_recommendation(root, G, df):
    commons_dict = {}  # Dictionnaire pour stocker les films communs et leurs liens
    
    # Parcourir les voisins du film racine
    for e in G.neighbors(root):
        # Pour chaque voisin du voisin, vérifier s'il s'agit d'un autre film
        for e2 in G.neighbors(e):
            if e2 == root:  # Ignorer le film racine lui-même
                continue
            if G.nodes[e2]['label'] == "MOVIE":  # On ne garde que les nœuds de type "MOVIE"
                commons = commons_dict.get(e2)
                if commons is None:
                    commons_dict.update({e2: [e]})  # Si le film n'existe pas encore, on l'ajoute avec son voisin
                else:
                    commons.append(e)  # Si le film est déjà présent, on ajoute le voisin à sa liste
                    commons_dict.update({e2: commons})
    
    # Création des listes pour stocker les résultats
    movies = []
    weight = []
    provenance = []
    
    # Calcul de la pondération pour chaque film recommandé
    for key, values in commons_dict.items():
        w = 0.0
        # La pondération est calculée en fonction des connexions communes (avec une pondération logarithmique)
        for e in values:
            degree_e = G.degree(e)
            if degree_e > 1:  # Safeguard against log(1) or log(0)
                w += 1 / math.log(degree_e)
            else:
                w += 1  # Handle very low degrees directly
        
        movies.append(key)
        weight.append(w)

        # Récupérer la provenance du film (service de streaming : Netflix, Disney, etc.)
        if key in df['title'].values and 'service' in df.columns:
            provenance.append(df[df['title'] == key]['service'].values[0])
        else:
            provenance.append('Unknown')

    # Créer un DataFrame pour les résultats avec les colonnes 'movie', 'weight', et 'provenance'
    result = pd.DataFrame({'movie': movies, 'weight': weight, 'provenance': provenance})
    
    # Trier les résultats par pondération décroissante
    result.sort_values(by='weight', ascending=False, inplace=True)
    
    return result