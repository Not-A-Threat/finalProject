import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from _plotly_utils.colors.cmocean import solar
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

#starts the app
app = dash.Dash(__name__)
server = app.server

#Navigation bar will be used on each page. 
sideMenu = html.Div([
    html.H2('Menu'),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink('Home', href='/', active='exact'),
        html.Br(),
        html.Br(),
        dbc.NavLink('MultiLine Graph', href='/page-1', active='exact'),
        html.Br(),
        html.Br(),
        dbc.NavLink('How to Help', href='/page-2', active='exact'),
    ],
    vertical=True,
    pills=True,
    ),
], className='navBar')

#website title
app.title = 'Future Energy'

#html layout of the homepage
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    sideMenu,
    html.Div(id='page-content')
])

#homepage layout
index_page = html.Div(style={
    'background-image':'url("/assets/green-gradient.svg")',
    "margin-left": "15rem",
    "padding": "2rem 1rem",
    }, children=[
    #title on the page
    html.H1(children='Team Not a Threat',
            style={'textAlign': 'center', 'color': '#1f1f1f'}),
    html.Br(),
    html.Br(),
    #A quick about us section
    html.H1('About Us', style={'textAlign': 'center', 'color':'#2b2b2b'}),
    html.H3('Future Energy was founded to help inspire people to inverse and use renewable energy. Eventually, we will run out of fossil fuels and we will need to use a new source of energy.', style={'textAlign':'center', 'color':'#2b2b2b'}),
    html.H3('Renewable energy is the way to go.', style={'textAlign':'center', 'color':'#2b2b2b'}),
    html.Br(),
    html.Br(),

    #Dropdown option to select a state
    html.H3('Hover over the map to see data for each state, or select a State below:', style={'color': '#2b2b2b'}),
    dcc.Dropdown(id='slct_state',
                options=[
                    #loops through states list and adds them to the dropdown
                    {'label': st, 'value': st} for st in states],
                    multi=False,
                    value='none',
                    style={'width': '35%'}
                    ),

    #will state what state the user has selected                
    html.Div(id='output_container', children=[]),
    html.Br(),

    #once a user selects a state, the hidden[] option will become false, and show all of this information(state image, consumption, consumption per capita)
    html.Div(id='selected state', children=[
        html.Img(id='state img', src=[]),
        html.H2(id='state name', children=[]),
        html.H2(id='state consumption', children=[])
    ], style={'textAlign':'center'}, hidden=[]),
    html.Br(),
    html.Br(),

    #graph that shows the us map with data
    dcc.Graph(id='usmap', figure={}),
])

#multigraph layout
page_1_layout = html.Div(style={
    'background-image':'url("/assets/green-gradient.svg")',
    "margin-left": "15rem",
    "padding": "2rem 1rem",
    }, children=[
        html.H1('Here is the production of Fossil fuels compared to Renewable energy.', style={'textAlign':'center'}),
        html.H2('As you can tell, fossil fuels has steadily climbed up since the start of 2010, while renewable energy barely has gone up since the 1970s', style={'textAlign':'center'}),
        dcc.Graph(id='graph1', 
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Fossil Fuel production vs Renewable Energy production',
                      xaxis={'title': 'Date'}, yaxis={'title': 'Energy Production in Quadrillion Btu'})  
                }),
        html.Br(),
        html.Br(),
        html.Hr(),
])

#links page
page_2_layout = html.Div(style={
    "margin-left": "15rem",
    "padding": "2rem 1rem",
}, children=[
    html.H1('Want to do your part in helping? These following links have more information:'),
    html.Hr(),
    html.H3('Since the growth of solar in the United States industry, it has helped pave the way to cleaner energy. Over the last couple of years, the cost of solar energy has reduced making it more affordable for American families and businesses to afford solar energy.'),
    html.H3('Click the image below to learn more:'),
    html.A([
        html.Img(
            src='/assets/Solar_panels.png', style={'width':'70%', 'height':'70%'}
        )], href='https://www.energy.gov/science-innovation/energy-sources/renewable-energy/solar'
    ),
    html.Br(),
    html.Hr(),
    html.H3('The United States is home to one of the largest and fastest-growing wind markets in the world. The Energy Department invests in different researchers and development projects both on land and offshore. All these different investments show that The Department of Energy is taking steps to cut carbon pollution.'),
    html.H3('Click the image below to learn more:'),
    html.A([
        html.Img(
            src='/assets/Wind Energy.png', style={'width':'70%', 'height':'70%'}
        )], href='https://www.energy.gov/science-innovation/energy-sources/renewable-energy/wind'
    ),
    html.Br(),
    html.Hr(),
    html.H3('American has a vast wave of tidal and hydropower resources, but a lot of this energy remains untouched. Simply because we do not have enough money back in it or enough research, The Energy Department is researching and developing efforts to expand electricity generation from these clean energy resources.'),
    html.H3('Click the image below to learn more:'),
    html.A([
        html.Img(
            src='/assets/Hydro_energy.png', style={'width':'70%', 'height':'70%'}
        )], href='https://www.energy.gov/science-innovation/energy-sources/renewable-energy/water'
    ),
    html.Br(),
    html.Hr(),
    html.H3('The local government can reduce the carbon footprint by directly passing strict laws like in California. To where you most have zero-emission vehicles by the year 2035 or generating electricity from clean, renewable sources.'),
    html.H3('Click the image below to learn more:'),
    html.A([
        html.Img(
            src='/assets/gas-vs-electric.png', style={'width':'70%', 'height':'70%'}
        )], href='https://www.epa.gov/statelocalenergy/local-renewable-energy-benefits-and-resources'
    ),
    html.Br(),
    html.Hr(),
])

#updates the map anytime a user selects a different state
@app.callback(
    [Output(component_id='output_container', component_property='children'),
    Output(component_id='usmap', component_property='figure'),
    Output(component_id='state img', component_property='src'),
    Output(component_id='selected state', component_property='hidden'),
    Output(component_id='state name', component_property='children'),
    Output(component_id='state consumption', component_property='children')],
    [Input(component_id='slct_state', component_property='value')]
)
def update_map(option_slctd):
    #setting all my variables to their original value
    hide_state=True
    container = f"The state chosen by user was {option_slctd}"
    pictureOfState = f'{option_slctd}.png'
    state_name = f'State: {option_slctd}'
    state_consume = f'Total Consumption (in quadrillion Btu): '

    #once a state is chosen that is in the State list information is grabbed from that state, and revealed
    for st in states: 
        if option_slctd == st:
            container = f"The state chosen by user was {option_slctd}"
            state_consumption_df_copy = state_consumption_df.copy()
            state_consumption_df_copy = state_consumption_df_copy[state_consumption_df_copy['State']==option_slctd]
            pictureOfState = app.get_asset_url(f'{option_slctd}.png')
            index = states.index(f'{option_slctd}')
            state_consume += consumption[index]
            hide_state=False

    #US Map with data
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

    #to focus on just US
    fig.update_layout(
        geo_scope='usa',
    )
    return container, fig, pictureOfState, hide_state, state_name, state_consume

#update index
@app.callback(Output(component_id='page-content', component_property='children'),
[Input(component_id='url', component_property='pathname')])
def display_page(pathname):
    if pathname =='/page-1':
        return page_1_layout
    elif pathname =='/page-2':
        return page_2_layout
    elif pathname =='/':
        return index_page
    else:
        return dbc.Jumbotron(
            [   html.H1('404: Not Found', style={"margin-left": "15rem", "padding": "2rem 1rem",}),
                html.Hr(),
                html.P(f'Pathname: {pathname} was not recognized', style={"margin-left": "15rem", "padding": "2rem 1rem",}),
            ]
        )

if __name__ == '__main__':
    app.run_server()
