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
state_consumption_df = pd.read_csv(cwd + '/Datasets/State_Energy_Consumption.csv')
multiline_df = pd.read_excel(cwd + '/Datasets/Overall_Energy.xlsx')

#creates a 'text' field of parts of the state consumption data frame
state_consumption_df['text'] = state_consumption_df['State'] + '<br>' + 'Consumption: ' + state_consumption_df['Consumption'] + '<br>' + ' Consumption per Capita: ' + state_consumption_df['Consumption per Capita']
#state_consumption_df = state_consumption_df.groupby(['State', 'Consumption', 'Rank', 'Consumption per Capita', 'Expenditures'])['Rank']

#making lines for the multiline chart
multiline_df['Month'] = pd.to_datetime(multiline_df['Month'])
trace1_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Fossil Fuels Production'], mode='lines', name='Fossil Fuel Production')
trace2_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Renewable Energy Production'], mode='lines', name='Renewable Energy Production')
data_multiline = [trace1_multiline, trace2_multiline]

app = dash.Dash()
server = app.server

#html layout of the page
app.layout = html.Div(style={
    'background-image':'url("/assets/green-gradient.svg")'
},
children=[
    html.H1(children='Team Not a Threat',
            style={'textAlign': 'center', 'color': '#e0e0e0'}),
    html.Br(),
    html.H1('About Us', style={'textAlign': 'center', 'color':'#d4d4d4'}),
    html.H3('Future Energy was founded to help inspire people to inverse and use renewable energy. Eventually, we will run out of fossil fuels and we will need to use a new source of energy. Renewable energy is the way to go.', style={'textAlign':'center', 'color':'#d4d4d4'}),
    html.Br(),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Map of the US', style={'color': '#d4d4d4'}),
    dcc.Dropdown(id='slct_state',
                options=[
                    {'label': 'Alabama', 'value': 'Alabama'},
                    {'label': 'Alaska', 'value': 'Alaska'}],
                    
                    multi=False,
                    value='none',
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

    container = "The state chosen by user was {}".format(option_slctd)
    # fig = px.choropleth(
    #     data_frame=state_consumption_df,
    #     locationmode='USA-states',
    #     locations='Code',
    #     scope="usa",
    #     color='Consumption per Capita',
    #     hover_data=['State','Consumption', 'Consumption per Capita'],
    #     labels={'Consumption': 'Consumption'},
    #     template='presentation'
    # )

    fig = go.Figure(
        data=[go.Choropleth(
            locationmode='USA-states',
            locations=state_consumption_df['Code'],
            z=state_consumption_df["Consumption per Capita"].astype(float),
            colorscale='Greens',
            reversescale=True,
            colorbar_title='Consumption per Capita',
            text=state_consumption_df['text'],
        )]
    )
    fig.update_layout(
        geo_scope='usa',
    )

    return container, fig



if __name__ == '__main__':
    app.run_server()
