import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import plotly.graph_objs as go 
import os

#Grabs current working directory
cwd = os.getcwd()

#loads data from excel file 
state_consumption_df = pd.read_excel(cwd + '\Datasets\State_Energy_Consumption.xls')
multiline_df = pd.read_excel(cwd + '\Datasets\Overall_Energy.xlsx')

#splits data into states and just energy
split_states = state_consumption_df['State'].str.split(' ')
split_energy = state_consumption_df['Consumption'].str.split(' ')
 
#making lines for the multiline chart
multiline_df['Month'] = pd.to_datetime(multiline_df['Month'])
trace1_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Fossil Fuels Production'], mode='lines', name='Fossil Fuel Production')
trace2_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Renewable Energy Production'], mode='lines', name='Renewable Energy Production')
data_multiline = [trace1_multiline, trace2_multiline]

app = dash.Dash()

#html layout of the page
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),

    html.H1('Energy production in the United States', style={'textAlign': 'center'}),
    html.Br(),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('H3', style={'color': '#df1e56'}),
    html.Div('3rd div'),
    dcc.Graph(id='graph1', 
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Fossil Fuel production vs Renewable Energy production',
                      xaxis={'title': 'Date'}, yaxis={'title': 'Energy Production in Quadrillion Btu'})       
    }),
])

if __name__ == '__main__':
    app.run_server()