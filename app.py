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
states = state_consumption_df.loc['0':, 'State'].values.tolist()
states=[unicodedata.normalize('NFKD', word) for word in states]
states = [x.strip(' ') for x in states]
states = sorted(states)


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
            style={'textAlign': 'center', 'color': '#1f1f1f'}),
    html.Br(),
    html.H1('About Us', style={'textAlign': 'center', 'color':'#2b2b2b'}),
    html.H3('Future Energy was founded to help inspire people to inverse and use renewable energy. Eventually, we will run out of fossil fuels and we will need to use a new source of energy. Renewable energy is the way to go.', style={'textAlign':'center', 'color':'#2b2b2b'}),
    #html.Div(' The company was founded by Joseph Chica, Colin McNeil, Willis Reid, and Duy Minh Pham', style={'font-size':'120%', 'color':'#2b2b2b'}),
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
    html.Img(id='selected_state', src=[], style={'width':'300px', 'height':'400px'}),
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
    Output(component_id='selected_state', component_property='src')],
    [Input(component_id='slct_state', component_property='value')]
)
def update_map(option_slctd):
    container = f"The state chosen by user was {option_slctd}"
    pictureOfState = f'{option_slctd}.jpg'
    for st in states: 
        if option_slctd == st:
            container = f"The state chosen by user was {option_slctd}"
            state_consumption_df_copy = state_consumption_df.copy()
            state_consumption_df_copy = state_consumption_df_copy[state_consumption_df_copy['State']==option_slctd]
            fig = ''
            pictureOfState = app.get_asset_url(f'{option_slctd}.jpg')

    # container = "The state chosen by user was {}".format(option_slctd)
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

    return container, fig, pictureOfState



if __name__ == '__main__':
    app.run_server()
