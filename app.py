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
state_consumption_df['text'] = state_consumption_df['State'] + '<br>' + 'Consumption: ' + state_consumption_df['Consumption'] + '<br>' + 'Consumption per Capita: ' + state_consumption_df['Consumption per Capita']

#creating states list
states = state_consumption_df.loc['0':, 'State'].values.tolist()
states = [unicodedata.normalize('NFKD', word) for word in states]
states = [x.strip(' ') for x in states]
sorted_states = sorted(states)

#creating consumption list
consumption = state_consumption_df.loc['0':, 'Consumption'].values.tolist()
consumption = [unicodedata.normalize('NFKD', total) for total in consumption]
consumption = [i.strip(' ') for i in consumption]

total=0
#get average of consumption
for c in consumption:
    total+=float(c.replace(',', ''))
average = round(total/50, 2)

#creating cpc list
per_capita = state_consumption_df.loc['0': 'Consumption per Capita'].values.tolist()
# per_capita = [unicodedata.normalize('NFKD', p) for p in per_capita]
# per_capita = [k.strip(' ') for k in per_capita]

#making lines for the multiline chart
multiline_df['Month'] = pd.to_datetime(multiline_df['Month'])
trace1_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Fossil Fuels Production'], mode='lines', name='Fossil Fuel Production', line_color='black')
trace2_multiline = go.Scatter(x=multiline_df['Month'], y=multiline_df['Total Renewable Energy Production'], mode='lines', name='Renewable Energy Production', line_color='green')
data_multiline = [trace1_multiline, trace2_multiline]

#starts the app
app = dash.Dash(__name__)
server = app.server

#possible header
topMenu = html.Header(role='banner', children=[
    html.Div([
        html.A('Home', href='/'),
        html.A('Energy Consumption', href='#ec'),
        html.A('Energy Production Over Time', href='/page-1'),
        html.A('Further Reading on Renewable Energy', href='/page-2'),
    ], className='topnav'),
])

#Navigation bar will be used on each page. 
sideMenu = html.Div([
    html.H2('Menu'),
    html.Hr(),
    dbc.Nav([
        dbc.NavLink('Home', href='/', active='exact'),
        html.Br(),
        html.Br(),
        dbc.NavLink('Energy Production Over Time', href='/page-1', active='exact'),
        html.Br(),
        html.Br(),
        dbc.NavLink('Further Reading on Renewable Energy', href='/page-2', active='exact'),
    ],
    ),
], className='navBar')

#website title
app.title = 'Future Energy'

#html layout of the homepage
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    topMenu,
    html.Div(id='page-content')
])

#homepage layout
index_page = html.Div(style={
    "margin-left": "1rem",
    "padding": "2rem 1rem",
    }, children=[
    #title on the page
    html.H1('Future Energy Limited',
            style={'textAlign': 'center', 'color': 'seagreen', }),
    #1f1f1f
    html.Hr(),
    html.Br(),
    #A quick about us section

    html.H1('About Us', style={'textAlign': 'center', 'color':'#2b2b2b'}),
    html.H3('Our mission at Future Energy is to spark conversations about renewable energy. The fossil fuels we currently depend on will reach critically low levels if we do not do something right now. Take a look at the data, gathered by experienced researchers. We live by our motto: "See the data, make the change.', style={'textAlign':'center', 'color':'#2b2b2b'}),
    html.H3('Renewable energy is the way to go.', style={'textAlign':'center', 'color':'#2b2b2b'}),
    html.H3('Created by Joseph Chica, Colin McNeil, Duy Minh, and Willis Reid', style={'textAlign':'center', 'color':'#2b2b2b'}),
    html.Br(),
    html.Hr(),
    
    html.A(id='ec'),
    #Dropdown option to select a state
    html.H3('The following interactive US map displays how much non-renewable energy is consumed every year by each state in British thermal units (Btu). 1 Btu is about as much energy released by a burning match.', style={'color': '#2b2b2b'}),
    html.H3('Hover over the map to see the amount of energy each state consumes, or select a state below: *', style={'color': '#2b2b2b'}),
    dcc.Dropdown(id='slct_state',
                options=[
                    #loops through states list and adds them to the dropdown
                    {'label': st, 'value': st} for st in sorted_states],
                    multi=False,
                    value='none',
                    style={'width': '35%'}
                    ),

    #will state what state the user has selected                
    html.Div(id='output_container', children=[]),
    html.Br(),

    #once a user selects a state, the hidden[] option will become false, and show all of this information(state image, consumption, consumption per capita)
    html.Div(id='hide container', children=[
        html.Div(id='selected state', children=[
        html.Img(id='state img', src=[], style={'width':'25%', 'height':'25%', }),
        html.Div(children=[
            html.H2(id='state name', children=[]),
            html.H2(id='state consumption', children=[]),
            html.H2(id='avg', children=[]),
        ]),
    ], style={'textAlign':'center'}, className='selected_state'),
    ], hidden=[]),
    html.Br(),
    html.Br(),

    #graph that shows the us map with data
    dcc.Graph(id='usmap', figure={}),
    html.H3('*Total consumption is measured in Trillion Btu. Consumption per Capita is measured in Million Btu.', style={'textAlign': 'center', 'color': '#2b2b2b'}),
    html.Br(),
    html.Br(),
    html.Hr(),
])

#multigraph layout
page_1_layout = html.Div(style={
    "margin-left": "2rem",
    "padding": "2rem 1rem",
    }, children=[
        html.H1('Fossil Fuels vs Renewable Energy', style={'textAlign':'center', 'color': 'seagreen'}),
        html.H2('As you can tell, fossil fuels has steadily climbed up since the start of 2010, while renewable energy barely has gone up since the 1970s', style={'textAlign':'center'}),
        dcc.Graph(id='graph1', 
              figure={
                  'data': data_multiline,
                  'layout': go.Layout(
                      title='Fossil Fuel production vs Renewable Energy production',
                      xaxis={'title': 'Date'}, yaxis={'title': 'Energy Production in Quadrillion Btu'},
                      height=600,)  
                }),
        html.Br(),
        html.Br(),
        html.Hr(),
])

#links page
page_2_layout = html.Div(style={
    "margin-left": "1rem",
    "padding": "2rem 1rem",
    }, children=[
    html.H1('Further Reading On Renewable Resources', style={'textAlign':'center', 'color': 'seagreen'}),
    html.Hr(),
    html.H3('SOLAR ENERGY'),
    html.H3('Since the growth of solar in the United States industry, it has helped pave the way to cleaner energy. Over the last couple of years, the cost of solar energy has reduced making it more affordable for American families and businesses to afford solar energy.'),
    html.H3('Click the image below to learn more:'),
    html.A([
        html.Img(
            src='/assets/panels.png', style={'width':'70%', 'height':'70%'}
        )], href='https://www.energy.gov/science-innovation/energy-sources/renewable-energy/solar'
    ),
    html.Br(),
    html.Hr(),
    html.H3('WIND POWER'),
    html.H3('The United States is home to one of the largest and fastest-growing wind markets in the world. The Energy Department invests in different researchers and development projects both on land and offshore. All these different investments show that The Department of Energy is taking steps to cut carbon pollution.'),
    html.H3('Click the image below to learn more:'),
    html.A([
        html.Img(
            src='/assets/Wind Turbines.png', style={'width':'70%', 'height':'70%'}
        )], href='https://www.energy.gov/science-innovation/energy-sources/renewable-energy/wind'
    ),
    html.Br(),
    html.Hr(),
    html.H3('HYDROPOWER'),
    html.H3('America has a vast wave of tidal and hydropower resources, but a lot of this energy remains untouched. The Energy Department is researching new ways to expand electricity generation from this clean, bountiful resource.'),
    html.H3('Click the image below to learn more:'),
    html.A([
        html.Img(
            src='/assets/Hydro Power.png', style={'width':'70%', 'height':'70%'}
        )], href='https://www.energy.gov/science-innovation/energy-sources/renewable-energy/water'
    ),
    html.Br(),
    html.Hr(),
    html.H3('WHAT CAN LOCAL GOVERMENT DO?'),
    html.H3('The local government can reduce the carbon footprint by directly passing strict laws. For example, only zero-emission vehicles will be sold in California after the year 2035'),
    html.H3('Click the image below to learn more:'),
    html.A([
        html.Img(
            src='/assets/Electric cars.png', style={'width':'70%', 'height':'70%'}
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
    Output(component_id='hide container', component_property='hidden'),
    Output(component_id='state name', component_property='children'),
    Output(component_id='state consumption', component_property='children'),
    Output(component_id='avg', component_property='children')],
    [Input(component_id='slct_state', component_property='value')]
)
def update_map(option_slctd):
    #setting all my variables to their original value
    hide_state=True
    container = f"The state chosen by user was {option_slctd}"
    pictureOfState = f'{option_slctd}.png'
    state_name = f'State: {option_slctd}'
    state_consume = f'Total Consumption (in quadrillion Btu): '
    bOrA = f'{option_slctd} is '

    #once a state is chosen that is in the State list information is grabbed from that state, and revealed
    for st in states: 
        if option_slctd == st:
            container = f"The state chosen by user was {option_slctd}"
            pictureOfState = app.get_asset_url(f'{option_slctd}.png')
            index = states.index(f'{option_slctd}')
            state_consume += consumption[index]
            hide_state=False
            fConsume = float(consumption[index])
            if fConsume < average:
                difference = average - fConsume
                difference = round(difference, 2)
                bOrA += f'below the National average of {average} by {difference}'
            else:
                difference = fConsume - average 
                difference = round(difference, 2)
                bOrA += f'above the National average of {average} by {difference}'

    #US Map with data
    fig = go.Figure(
        data=[go.Choropleth(
            locationmode='USA-states',
            locations=state_consumption_df['Code'],
            z=state_consumption_df["Consumption per Capita"],
            colorscale='emrld',
            reversescale=False,
            colorbar_title='Consumption per Capita',
            text=state_consumption_df['text'],
        )]
    )
    # Colorscales:
    #          'aggrnyl' f,
    #          'bluyl' t,
    #          'curl' f,
    #          'earth' t,
    #          'emrld' f, 'fall', 'geyser',
    #          'haline', 'jet',
    #          'mint',
    #          'orrd',
    #          'plasma', 'prgn',
    #          'ylgn',

    #to focus on just US
    fig.update_layout(
        geo_scope='usa',
    )
    return container, fig, pictureOfState, hide_state, state_name, state_consume, bOrA

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