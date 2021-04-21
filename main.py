import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import plotly.graph_objs as go 
import os

#loading excel file from dataset folder
cwd = os.getcwd()

state_consumption_df = pd.read_excel(cwd + '\Datasets\State_Energy_Consumption.xls')
multiline_df = pd.read_excel(cwd + '\Datasets\Overall_Energy.xlsx')
'''print(state_consumption_df)
'''
list_of_states = pd.DataFrame(state_consumption_df, columns=['State'])
print(list_of_states)

multiline_df['Month'] = pd.to_datetime(multiline_df['Month'])
trace1_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Fossil Fuels Production'], mode='lines', name='Fossil Fuel Production')
trace2_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Renewable Energy Production'], mode='lines', name='Renewable Energy Production')

data_multiline = [trace1_multiline, trace2_multiline]

app = dash.Dash()

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