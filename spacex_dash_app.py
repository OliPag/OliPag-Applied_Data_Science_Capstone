#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 15:04:39 2024

@author: olivierpaget
"""

# Import required libraries
import pandas as pd
import dash
#import dash_html_components as html
from dash import html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[{'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'}, 
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}, 
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'}, 
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}],
                                    value='ALL',
                                    placeholder='Select the launch site',
                                    searchable=True,
                                    style={'width':'80%','padding':'3px','font-size':'16px','text-align-last':'center'}
                                             ),
                                    
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                # Function decorator to specify function input and output
                                  


                                html.Div([dcc.Graph(id='success-pie-chart')],
                                
                                style={'display':'inline-block'},
                                       ),

                                html.Br(),
                                
                            
                                html.P('Payload range (Kg):'),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(min=min_payload, max=max_payload, step=500, id='my-range-slider',
                                value=[min_payload, max_payload]),
                                

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart',component_property='figure'),
    Input(component_id='site-dropdown',component_property='value'))

def get_pie_chart(list_site):
    fiLtered_df=spacex_df
    if list_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
                     names='Launch Site', 
                     title='Total successful launches count for all sites')
        return fig
    else:
        fiLtered_df = spacex_df[spacex_df['Launch Site']==list_site]
        df_group=fiLtered_df.groupby(['Launch Site', 'class'],axis=0).size().reset_index(name='class count')
        fig=px.pie(df_group, values='class count',
                   names='class',title=f"Number of successful vs unsuccessful flights for the site {list_site}")
        return fig
    print(fiLtered_df)
                 
                 
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter{chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart',component_property='figure'),
    [Input(component_id='site-dropdown',component_property='value'),
    Input(component_id='my-range-slider',component_property='value')])

def get_scatter(list_site,choix_load):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(choix_load[0],choix_load[1])]
    if list_site=='ALL':
        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category')
        return fig
    else:
        filtered_df = filtered_df[filtered_df['Launch Site']==list_site]
        fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color='Booster Version Category')
        return fig
        
    
    
    
# Run the app
if __name__ == '__main__':
    app.run_server()