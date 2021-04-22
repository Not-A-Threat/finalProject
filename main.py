import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import plotly.graph_objs as go 
import plotly.express as px
import os

#Grabs current working directory
cwd = os.getcwd()

#loads data from excel file 
state_consumption_df = pd.read_excel(cwd + '/Datasets/State_Energy_Consumption.xls')
multiline_df = pd.read_excel(cwd + '/Datasets/Overall_Energy.xlsx')

state_consumption_df = state_consumption_df.groupby(['State', 'Consumption', 'Rank', 'Consumption per Capita', 'Expenditures'])['Rank']

#making lines for the multiline chart
multiline_df['Month'] = pd.to_datetime(multiline_df['Month'])
trace1_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Fossil Fuels Production'], mode='lines', name='Fossil Fuel Production')
trace2_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Renewable Energy Production'], mode='lines', name='Renewable Energy Production')
data_multiline = [trace1_multiline, trace2_multiline]

app = dash.Dash()

#html layout of the page
app.layout = html.Div(children=[
    html.H1(children='Team Not a Threat',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),

    html.H1('Renewable and Nonrenewable Energy', style={'textAlign': 'center'}),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Map of the US', style={'color': '#df1e56'}),
    dcc.Dropdown(id='slct_state',
                options=[
                    {'label': 'Alabama', 'value': 'Alabama'},
                    {'label': 'Alaska', 'value': 'Alaska'}],
                    
                    multi=False,
                    value='Albama',
                    style={'width': '40%'}
                    ),
    html.Div(id='output_container', children=[]),
    html.Br(),
    #html.Iframe(id='usmap', src="https://createaclickablemap.com/map.php?&id=102341&maplocation=false&online=true", width='1200', height='700'),

    dcc.Graph(id='usmap', figure={}),

    dcc.Graph(id='graph1', 
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Fossil Fuel production vs Renewable Energy production',
                      xaxis={'title': 'Date'}, yaxis={'title': 'Energy Production in Quadrillion Btu'})       
    }),
])

@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='usmap', component_property='figure')],
    [Input(component_id='slct_state', component_property='value')]
)
def update_map(option_slctd):
    print(option_slctd)

    container = "The state chosen by user was {}".format(option_slctd)

    fig = px.choropleth(
        data_frame=state_consumption_df,
        locationmode='USA-states',
        locations='State',
        scope="usa",
        color='Consumption',
        hover_data=['State', 'Consumption', 'Consumption per Capita', 'Expenditures'],
        color_continuous_scale=px.colors.sequential.YlOrRd,
        labels={'Consumption': 'Consumption'},
        template='plotly_dark'
    )

    return container, fig



if __name__ == '__main__':
    app.run_server()