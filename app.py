from dash import Dash, dcc, html, page_container, callback, Input, Output

# Initialize the Dash app with multi-page support
app = Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
app.config.suppress_callback_exceptions = True

# Main layout with improved page navigation
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),  # Location component to track the current URL
    
    # Main container with sidebar and page content
    html.Div([
        # Sidebar for navigation
        html.Div(id='nav-bar', style={
            'width': '350px', 
            'padding': '20px', 
            'background-color': '#f8f9fa', 
            'position': 'fixed', 
            'top': '0', 
            'left': '0', 
            'bottom': '0',
            'overflow': 'auto',
        }),
        
        # Page content container
        html.Div([
            page_container
        ], style={'margin-left': '370px', 'padding': '20px'})  # Add margin to shift content right of the sidebar
    ])
])

# Callback to dynamically apply the active class based on the current page
@app.callback(
    Output('nav-bar', 'children'),
    [Input('url', 'pathname')]  # Use the 'url' component to get the current pathname
)
def update_navbar(pathname):
    return html.Div([        
        dcc.Link(
            html.H1("Network Theory Project", style={'text-align': 'center', 'font-family': 'Arial, sans-serif'}),
            href='/',
            style={'text-decoration': 'none'}    
        ),
        dcc.Link('Full Network', href='/page1', className='nav-link nav-link-active' if pathname == '/page1' else 'nav-link', style={'display': 'block', 'margin-bottom': '10px'}),
        dcc.Link('Movie Network', href='/page2', className='nav-link nav-link-active' if pathname == '/page2' else 'nav-link', style={'display': 'block', 'margin-bottom': '10px'}),
        dcc.Link('Network between 2 movies', href='/page3', className='nav-link nav-link-active' if pathname == '/page3' else 'nav-link', style={'display': 'block', 'margin-bottom': '10px'}),
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
