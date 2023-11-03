import dash
from dash import dcc
from dash import html 
from dash import dash_table

from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

#Local API for ETL 
from dataapi import load_df

#Load dataset
df = load_df()


app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Data Dashboard"),
    
    # Filter controls
    html.Div([
        html.Label("Filter by Date:"),
        dcc.DatePickerRange(
            id='date-filter',
            start_date=df['date'].min(),
            end_date=df['date'].max(),
        ),
    ]),
    html.Div([
        html.Label("Filter by Hour:"),
        dcc.RangeSlider(
            id='hour-filter',
            min=df['hour'].min(),
            max=df['hour'].max(),
            step=1,
            marks={i: str(i) for i in range(df['hour'].min(), df['hour'].max() + 1)},
            value=[df['hour'].min(), df['hour'].max()],
        ),
    ]),
    html.Div([
        html.Label("Filter by Expected Download Mbps:"),
        dcc.Dropdown(
                id='download-filter',
                options=[{'label': mbps, 'value': mbps} for mbps in df['expected_download_mbps'].unique()],
                multi=True,
                placeholder="Select Download (Mbps)"
            ),        
    ]),      
    
    
    
     # Row 1: Pie Chart and Ratio
    html.Div([
      html.Div([
            html.H3("Ratio of 'SI'"),
            html.Div(id='ratio-chart' , style={'text-align': 'center', 'font-family': 'cursive', 'width': '300px', 'height': '300px'  } ,
            #'vertical-align': 'middle'
              ),
        ]
        , style={'width': '50%', 'display': 'inline-block'}
        # , style={'display': 'inline-block', 'vertical-align': 'middle'}
        #, 'vertical-align': 'middle' 
        ),
    
      html.Div([
            dcc.Graph(id='pie-chart', config={'displayModeBar': False}),
        ], style={'width': '50%', 'display': 'inline-block'}),
        
    ]),
    
    
    # Timeline showing counts of 'cumple' column
    dcc.Graph(id='timeline'),
    
    # Table containing filtered data
    dash_table.DataTable(
        data=df.to_dict('records'), 
        columns=[{"name": i, "id": i} for i in df.columns],  id='filtered-data',
        style_table={'height': '400px', 'overflowY': 'auto'},
        page_size=10
    )   ,
    
    # Download link for filtered data
    html.A("Download Filtered Data", id="download-link", download="filtered_data.csv", href="", target="_blank"),
])

# Callback to update visualizations and filtered data
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('timeline', 'figure'),
     Output('filtered-data', 'data'),
     Output('download-link', 'href'),
     Output('ratio-chart', 'children')],
    [Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date'),
     Input('hour-filter', 'value'),
     Input('download-filter', 'value')]
)
def update_data(start_date, end_date, hour_range, download_range):
    filtered_df = df[
        (df['date'] >= start_date) &
        (df['date'] <= end_date) &
        (df['hour'] >= hour_range[0]) &
        (df['hour'] <= hour_range[1]) 
    ]
    if download_range:
        filtered_df = filtered_df[filtered_df['expected_download_mbps'].isin(download_range)]
    
    pie_fig = px.pie(filtered_df, names='cumple', title='Cumple Distribution', width=400, height=400)
    
    timeline_fig = px.histogram(filtered_df, x='date', color='cumple')    
    
    # Calculate and display the ratio
    total_count = len(filtered_df)
    si_count = len(filtered_df[filtered_df['cumple'] == 'SI'])
    ratio = (si_count / total_count) * 100
    
    download_link = f"data:text/csv;charset=utf-8,{filtered_df.to_csv(index=False)}"
    
    return pie_fig, timeline_fig, filtered_df.to_dict('records'), download_link,  f"Ratio of 'SI' values: {ratio:.2f}%" 

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050)

