import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd 
import plotly.graph_objs as go 
import plotly.express as px
import os
import unicodedata

#Grabs current working directory
cwd = os.getcwd()

#loads data from excel file 
state_consumption_df = pd.read_csv(cwd + '/Datasets/State_Energy_Consumption.csv')
multiline_df = pd.read_excel(cwd + '/Datasets/Overall_Energy.xlsx')

#creates a 'text' field of parts of the state consumption data frame
state_consumption_df['text'] = state_consumption_df['State'] + '<br>' + 'Consumption: ' + state_consumption_df['Consumption'] + '<br>' + ' Consumption per Capita: ' + state_consumption_df['Consumption per Capita']

#creating states list
states = state_consumption_df.loc['0':, 'State'].values.tolist()
states = [unicodedata.normalize('NFKD', word) for word in states]
states = [x.strip(' ') for x in states]
states = sorted(states)

#creating consumption list
consumption = state_consumption_df.loc['0':, 'Consumption'].values.tolist()
consumption = [unicodedata.normalize('NFKD', total) for total in consumption]
consumption = [i.strip(' ') for i in consumption]


#making lines for the multiline chart
multiline_df['Month'] = pd.to_datetime(multiline_df['Month'])
trace1_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Fossil Fuels Production'], mode='lines', name='Fossil Fuel Production')
trace2_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Renewable Energy Production'], mode='lines', name='Renewable Energy Production')
data_multiline = [trace1_multiline, trace2_multiline]

app = dash.Dash(__name__)
server = app.server

app.title = 'Future Energy'

#html layout of the page
app.layout = html.Div(style={
    'background-image':'url("/assets/green-gradient.svg")'
},
children=[
    html.H1(children='Team Not a Threat',
            style={'textAlign': 'center', 'color': '#1f1f1f'}),
    html.Br(),
    html.H1('About Us', style={'textAlign': 'center', 'color':'#2b2b2b'}),
    html.H3('Future Energy was founded to help inspire people to inverse and use renewable energy. Eventually, we will run out of fossil fuels and we will need to use a new source of energy. Renewable energy is the way to go.', style={'textAlign':'center', 'color':'#2b2b2b'}),
    html.Br(),
    html.Br(),
    html.H3('Hover over the map to see data for each state, or select a State below:', style={'color': '#2b2b2b'}),
    dcc.Dropdown(id='slct_state',
                options=[
                    {'label': st, 'value': st} for st in states],
                    multi=False,
                    value='none',
                    style={'width': '35%'}
                    ),
    html.Div(id='output_container', children=[]),
    html.Br(),
    #html.Iframe(id='usmap', src="https://createaclickablemap.com/map.php?&id=102341&maplocation=false&online=true", width='1200', height='700'),
    html.Div(id='selected_state', children=[
        html.Img(id='state_img', src=[]),
        html.H2(id='state name', children=[])
    ], style={'textAlign':'center'}, hidden=[]),
    html.Br(),
    html.Br(),
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
    Output(component_id='usmap', component_property='figure'),
    Output(component_id='state_img', component_property='src'),
    Output(component_id='selected_state', component_property='hidden'),
    Output(component_id='state name', component_property='children')],
    [Input(component_id='slct_state', component_property='value')]
)
def update_map(option_slctd):
    hide_state=True
    hide_info=True
    container = f"The state chosen by user was {option_slctd}"
    pictureOfState = f'{option_slctd}.png'
    state_name = f'State: {option_slctd};'
    for st in states: 
        if option_slctd == st:
            container = f"The state chosen by user was {option_slctd}"
            state_consumption_df_copy = state_consumption_df.copy()
            state_consumption_df_copy = state_consumption_df_copy[state_consumption_df_copy['State']==option_slctd]
            fig = ''
            pictureOfState = app.get_asset_url(f'{option_slctd}.png')
            hide_state=False
            hide_info=False

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

    return container, fig, pictureOfState, hide_state, state_name



if __name__ == '__main__':
    app.run_server()
