#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 11:47:52 2019

@author: Heppa
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import time
import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions']=True 


# read the data
df = pd.read_csv('aqiDataDownload.csv')


df = pd.read_csv('aqiDataDownload.csv')

# add field "hour"
df['Date Time']=pd.to_datetime(df['Date Time'])
divider=60*60*1000000000
df['hour']=(24-(pd.to_numeric((df['Date Time'].max()-df['Date Time']))/divider)).astype(int)
df['hour_string']=[hour.strftime('%H:%M') for hour in df['Date Time']]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)



app.layout = html.Div([
    dcc.Graph(id='graph-with-slider'),
    dcc.Slider(
        id='time-slider',
        min=df['hour'].min(),
        max=df['hour'].max(),
        value=df['hour'].max(),
        marks=dict(zip(df['hour'], df['hour_string']))
    )
])


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('time-slider', 'value')])
def update_figure(hour_index):
    filtered_df = df[df.hour == hour_index].append(df[df.hour == hour_index-1])
    traces = []
    for i in filtered_df['station'].unique():
        df_by_station = filtered_df[filtered_df['station'] == i]
        traces.append(go.Scatter(
            x=df_by_station['aqhi_official'],
            y=df_by_station['aqi'],
            text=df_by_station['station'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': go.Layout(
            xaxis={'title': 'AQHI', 'range': [0, 11]},
            yaxis={'title': 'AQI', 'range': [0, 300]},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 0, 'y': 1},
            hovermode='closest'
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)