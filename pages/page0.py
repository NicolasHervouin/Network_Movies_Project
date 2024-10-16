from dash import html, register_page

register_page(__name__, "/")

layout = html.Div(
    [
        html.Div(
            [
                html.H2("Introduction", style={"text-align": "justify"}),
                html.P(
                    """
                    The objective of this project is to perform a network analysis using film databases from several video-on-demand (VOD) platforms, namely Amazon Prime, Netflix, and Disney+. By combining the information from these three platforms, the analysis focuses on action films released between 1920 and 2021, establishing relationships between films based on various attributes such as actors, directors, genres, production countries, as well as similarities in film descriptions.
                    """,
                    style={"text-align": "justify"}
                ),
                html.H3("Problem Statement", style={"text-align": "justify"}),
                html.P(
                    """
                    How can network theory help us build a recommendation model? More specifically, how does analyzing the relationships between films and their attributes (actors, directors, genres, etc.) help better understand the similarities between films to build an effective recommendation model?
                    """,
                    style={"text-align": "justify"}
                ),
                html.H3("Data and Preparation", style={"text-align": "justify"}),
                html.P(
                    """
                    Three databases were used, each representing the film catalogs of Amazon Prime, Netflix, and Disney+. After merging the three datasets, an additional column was added to identify the platform of each film. The film IDs were modified to ensure uniqueness across the different platforms. Then, additional information such as actors, directors, genres, and production countries were extracted and structured as lists.
                    """,
                    style={"text-align": "justify"}
                ),
                html.Ul(
                    [
                        html.Li(
                            html.A("Amazon Link", href="https://www.kaggle.com/datasets/shivamb/amazon-prime-movies-and-tv-shows/data", target="_blank")
                        ),
                        html.Li(
                            html.A("Netflix Link", href="https://www.kaggle.com/datasets/shivamb/netflix-shows", target="_blank")
                        ),
                        html.Li(
                            html.A("Disney Link", href="https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows", target="_blank")
                        ),
                    ]
                ),
                html.H3("Methodology", style={"text-align": "justify"}),
                html.P(
                    """
                    The network analysis was performed by constructing a graph using NetworkX, where each film is represented by a node. Relationships (edges) were created between films based on common actors, directors, genres, countries, and similarities in film descriptions, calculated using the TF-IDF method and K-Means clustering.
                    """,
                    style={"text-align": "justify"}
                ),
                html.H4("Main Steps:", style={"text-align": "justify"}),
                html.Ol(
                    [
                        html.Li("Data exploration and preparation: Cleaning, transforming columns into lists, and filtering action films between 2000 and 2023."),
                        html.Li("Graph creation: Using NetworkX to create a graph with nodes representing the films and associated people (actors, directors)."),
                        html.Li("Graph property analysis: Calculating metrics such as average degree, density, transitivity, as well as degree, betweenness, and closeness centralities."),
                        html.Li("Community detection: Applying the Louvain algorithm to detect communities within the network."),
                        html.Li("Film recommendation: Building a recommendation system based on the similarity of descriptions (TF-IDF) and connections in the film network."),
                    ],
                    style={"text-align": "justify"}
                ),
                html.H3("Visualization and Recommendation", style={"text-align": "justify"}),
                html.P(
                    """
                    Interactive visualizations were generated using Plotly to explore the connections between films and their actors, directors, genres, and countries. Additionally, a film recommendation system was implemented, suggesting similar films based on both descriptions and the connections between films in the network.
                    """,
                    style={"text-align": "justify"}
                ),
                html.H3("Conclusion", style={"text-align": "justify"}),
                html.P(
                    """
                    This project illustrates how network analysis can be applied to explore relationships between elements in a large dataset, here films and their attributes. Clustering techniques and graphical visualization help better understand the relationships between films and improve recommendation systems by leveraging these connections.
                    """,
                    style={"text-align": "justify"}
                ),
            ],
            style={"padding": "20px", "border": "1px solid #ccc", "border-radius": "10px", "box-shadow": "2px 2px 5px rgba(0,0,0,0.1)"}
        )
    ]
)