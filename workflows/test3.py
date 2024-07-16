import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
#from jupyter_dash import JupyterDash

import os 
app = dash.Dash(__name__)
#app = JupyterDash(__name__)

# Read the data from the CSV file
df = pd.read_csv('combined_metadata.csv')
df = df.fillna('NA')

# Define taxonomic ranks
tax_ranks = ['domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']

# Split the classification column into separate columns for each level
df[tax_ranks] = df['classification'].str.split(';', expand=True)

metadata_columns = [col for col in df.columns if col not in tax_ranks + ['classification', 'Genome']]

dropdown_options = [{'label': col, 'value': col} for col in metadata_columns]

def create_sunburst(selected_metadata):
    path = tax_ranks + [selected_metadata]
    sunburst_fig = px.sunburst(
        df, 
        path=path,
        color=selected_metadata,
        color_continuous_scale=px.colors.sequential.RdBu,
        maxdepth=7  # This will show up to species level (6) plus one more for metadata
    )
    sunburst_fig.update_layout(height=700, width=700) 
    return sunburst_fig

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Label('Select your metadata', style={'fontSize': 15, 'fontWeight': 'bold', 'marginBottom': '10px'}),
            dcc.Dropdown(
                id='color-dropdown',
                options=[{'label': col, 'value': col} for col in metadata_columns],
                value=metadata_columns[0] if metadata_columns else None,
                placeholder="Select color variable",
                style={
                    'width': '100%', 
                    'height': '30px',
                    'fontSize': 16,
                    'whiteSpace': 'normal',
                    'textOverflow': 'ellipsis'
                }
            ),
        ], style={'width': '50%', 'margin': '10px auto'}),
    ], style={'backgroundColor': 'white', 'padding': '20px'}),

    html.Div([
        dcc.Graph(id='overall-scatter-plot', style={'height': '600px'})
    ], style={'width': '65%', 'display': 'inline-block'}),
    html.Div([
        dcc.Graph(id='overall-distribution-plot', style={'height':'600px'})
    ], style={'width': '35%', 'display': 'inline-block', 'vertical-align': 'top'}),
    
    html.Div([
        dcc.Dropdown(
            id='metadata-dropdown',
            options=dropdown_options,
            value='pass.GUNC',  # Default value
            style={'width': '50%'}
        ),
    ]),
    html.Div([
        html.Div([
            dcc.Graph(id='sunburst-plot')
        ], style={'width': '65%', 'display': 'inline-block'}),
        html.Div([
            html.Div([
                dcc.Graph(id='filtered-scatter-plot', style={'height': '350px'})
            ]),        
            html.Div([
                dcc.Graph(id='filtered-distribution-plot', style={'height': '350px'})
            ])
        ], style={'width': '35%', 'display': 'inline-block', 'vertical-align': 'top'}),
    ]),

    html.Div([
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Search table...',
            style={'marginRight': '10px', 'width': '200px'}
        ),
        dcc.Input(
            id='filename-input',
            type='text',
            placeholder='Enter filename for CSV',
            style={'marginRight': '10px', 'width': '200px'}
        ),
        html.Button('Save to Local', id='save-local-button', n_clicks=0),
        html.Button('Save to Server', id='save-server-button', n_clicks=0),        
        #html.Button('Save to CSV', id='save-button', n_clicks=0),
    ], style={'marginBottom': '10px'}),
    dash_table.DataTable(
        id='data-table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.head(10).to_dict('records'),
        page_size=10,
        filter_action='custom',
        filter_query=''
    ),
    dcc.Download(id="download-dataframe-csv"),
    html.Div(id='save-status') 
])

@app.callback(
    [Output('overall-scatter-plot', 'figure'),
     Output('overall-distribution-plot', 'figure')],
    [Input('color-dropdown', 'value')]
)
def update_overall_plots(color_var):
    scatter_fig = px.scatter(
        df, 
        x='Completeness', 
        y='Contamination', 
        color=color_var,
        hover_data=['classification'],
        title='Overall: Completeness vs Contamination'
    )
    scatter_fig.update_layout(plot_bgcolor='white', font={'family': 'Arial', 'size': 14})

    dist_fig = px.histogram(
        df, 
        x=color_var,
        title=f'Overall Distribution of {color_var}'
    )
    dist_fig.update_layout(plot_bgcolor='white', font={'family': 'Arial', 'size': 14})

    return scatter_fig, dist_fig

@app.callback(
    Output('sunburst-plot', 'figure'),
    Input('metadata-dropdown', 'value')
)
def update_sunburst(selected_metadata):
    return create_sunburst(selected_metadata)

@app.callback(
    [Output('filtered-scatter-plot', 'figure'),
     Output('filtered-distribution-plot', 'figure')],
    [Input('sunburst-plot', 'clickData'),
     Input('metadata-dropdown', 'value')],
    [State('sunburst-plot', 'figure')]
)
def update_filtered_plots(clickData, selected_metadata, current_figure):
    filtered_df = df.copy()
    
    if clickData:
        current_path = clickData['points'][0]['id'].split('/')
        for i, level in enumerate(current_path):
            if level and i < len(tax_ranks):
                filtered_df = filtered_df[filtered_df[tax_ranks[i]] == level]
    
    if filtered_df.empty:
        return dash.no_update, dash.no_update

    scatter_fig = px.scatter(
        filtered_df, 
        x='Completeness', 
        y='Contamination', 
        color=selected_metadata,
        hover_data=['classification'],
        title='Filtered: Completeness vs Contamination'
    )
    scatter_fig.update_layout(plot_bgcolor='white', font={'family': 'Arial', 'size': 14})

    metadata_dist_fig = px.histogram(
        filtered_df, 
        x=selected_metadata,
        title=f'Filtered Distribution of {selected_metadata}'
    )
    metadata_dist_fig.update_layout(plot_bgcolor='white', font={'family': 'Arial', 'size': 14})

    return scatter_fig, metadata_dist_fig

@app.callback(
    Output('data-table', 'data'),
    [Input('search-input', 'value'),
     Input('sunburst-plot', 'clickData'),
     Input('metadata-dropdown', 'value')]
)
def update_table(search_value, clickData, selected_metadata):
    filtered_df = df.copy()
    
    if clickData:
        current_path = clickData['points'][0]['id'].split('/')
        for i, level in enumerate(current_path):
            if level and i < len(tax_ranks):
                filtered_df = filtered_df[filtered_df[tax_ranks[i]] == level]
    
    if search_value:
        filtered_df = filtered_df[filtered_df.apply(lambda row: any(str(search_value).lower() in str(cell).lower() for cell in row), axis=1)]

    return filtered_df.head(10).to_dict('records')

@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("save-local-button", "n_clicks"),
    State("filename-input", "value"),
    State("data-table", "data"),
    prevent_initial_call=True,
)
def save_to_local(n_clicks, filename, table_data):
    if n_clicks == 0:
        raise PreventUpdate
    
    if not filename:
        filename = "data"
    
    df = pd.DataFrame(table_data)
    return dcc.send_data_frame(df.to_csv, f"{filename}.csv", index=False)

# 서버 저장 콜백
@app.callback(
    Output("save-status", "children"),
    Input("save-server-button", "n_clicks"),
    State("filename-input", "value"),
    State("data-table", "data"),
    prevent_initial_call=True,
)
def save_to_server(n_clicks, filename, table_data):
    if n_clicks == 0:
        raise PreventUpdate
    
    if not filename:
        filename = "data"
    
    df = pd.DataFrame(table_data)
    server_path = os.path.join(os.getcwd(), f"{filename}.csv")
    df.to_csv(server_path, index=False)
    return f"File saved to server at {server_path}"

if __name__ == '__main__':
    app.run_server(debug=True)

#if __name__ == '__main__':
    #  use 'external' to open in a new browser tab, or 'inline' to display within the notebook. 'jupyterlab'
#    app.run_server(mode='inline') 