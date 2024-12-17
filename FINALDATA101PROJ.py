#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import plotly.express as px
import numpy as np
import requests
from dash import Dash, dcc, html, Input, Output,State
import dash_bootstrap_components as dbc
import json
pd.DataFrame.iteritems = pd.DataFrame.items
pd.options.mode.chained_assignment = None


# In[3]:


#SEPARATE DATA LOADING BECAUSE IT TAKES LONG TO LOAD

df_fies2021 = pd.read_csv('https://raw.githubusercontent.com/elleblp/finalproject/main/fies_2021_final.csv')
df_fies2018 = pd.read_csv('https://raw.githubusercontent.com/elleblp/finalproject/main/fies_2018_final.csv')


# In[4]:


# Load data for all apps
df = pd.read_csv('https://raw.githubusercontent.com/elleblp/finalproject/main/total_income_exp_by_region.csv')
province_df = pd.read_csv('https://raw.githubusercontent.com/elleblp/finalproject/main/total_income_exp_by_province.csv')
exp_province_df = pd.read_csv('https://raw.githubusercontent.com/elleblp/finalproject/main/components_exp_by_province.csv')
components_province_df = pd.read_csv('https://raw.githubusercontent.com/elleblp/finalproject/main/components_income_exp_by_province.csv')

#REGIONAL GEOJSON
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/elleblp/data101/main/country.0.01.json') as response:
    geo_ph_regions = json.load(response)


# In[96]:


##ONE LAYOUT

# FROM FINAL GRAPH 1
region_centers = {
    100000000: {'lat': 16.902963843901748, 'lon': 120.48276792536502},
    200000000: {'lat': 17.204075477381206, 'lon': 121.73158896510874},
    300000000: {'lat': 15.391941180007118, 'lon': 120.82231232285217},
    400000000: {'lat': 14.162210954976622, 'lon': 121.56817081280585},
    500000000: {'lat': 13.271887489689934, 'lon': 123.47356081756668},
    600000000: {'lat': 10.843102150758034, 'lon': 122.6521125008806},
    700000000: {'lat': 9.921400136571263, 'lon': 123.61516185873698},
    800000000: {'lat': 11.535689480766273, 'lon': 124.95347277463267},
    900000000: {'lat': 7.826142862887799, 'lon': 122.84801596306916},
    1000000000: {'lat': 8.187333326412226, 'lon': 124.67485858617033},
    1100000000: {'lat': 7.21023013121781, 'lon': 125.82660704123714},
    1200000000: {'lat': 6.580559739704033, 'lon': 124.82103299191132},
    1300000000: {'lat': 14.606295006382998, 'lon': 121.03222186447566},
    1400000000: {'lat': 17.35390043024146, 'lon': 121.038444046383},
    1600000000: {'lat': 8.811611067211622, 'lon': 125.79170907103276},
    1700000000: {'lat': 11.350189143124805, 'lon': 119.88884824107006},
    1900000000: {'lat': 6.959462402323515, 'lon': 123.42453415392548},
}

# FROM FINAL GRAPH 2
legend_updates = {
    'BREAD': 'Rice & Bread',
    'MEAT': 'Meat',
    'FISH': 'Fish & Seafood',
    'FOODOUTSIDE': 'Food Outside',
    'VEG': 'Vegetables',
    'MILK': 'Milk & Dairy',
    'FRUIT': 'Fruits',
    'OTHERFOOD': 'Others',
    'HOUSINGWATER': 'Housing & Utilities',
    'MISCELLANEOUS': 'Miscellaneous',
    'TRANSPORT': 'Transportation',
    'COMMUNICATION': 'Communication',
    'HEALTH': 'Healthcare',
    'DURABLE': 'Durable Equipment',
    'OCCASION': 'Special Occasions',
    'FURNISHING': 'Furniture & Appliances',
    'OTHERNFOOD': 'Others'
}

# FROM FINAL GRAPH 3
colorscale = ['#56B4E9', '#009E73', '#D55E00', '#CC79A7', '#F0E442', '#882255', '#0072B2']

# FROM FINAL GRAPH 4
# Define function to map regions to their respective groups
def region_to_group(region):
    luzon_regions = [
        'Region I - Ilocos Region',
        'Region II - Cagayan Valley',
        'Region III - Central Luzon',
        'Region IVA - CALABARZON',
        'Region IVB - MIMAROPA',
        'Region V - Bicol',
        'Cordillera Administrative Region',
        'National Capital Region'
    ]
    visayas_regions = [
        'Region VI - Western Visayas',
        'Region VII - Central Visayas',
        'Region VIII - Eastern Visayas'
    ]
    mindanao_regions = [
        'Region IX - Zamboanga Peninsula',
        'Region X - Northern Mindanao',
        'Region XI - Davao',
        'Region XII - SOCCSKSARGEN',
        'Region XIII - Caraga',
        'Autonomous Region in Muslim Mindanao'
    ]

    if region in luzon_regions:
        return 'Luzon'
    elif region in visayas_regions:
        return 'Visayas'
    elif region in mindanao_regions:
        return 'Mindanao'
    else:
        return None

# Apply function to create new column
df_fies2021['Greater Region'] = df_fies2021['W_REGN_N'].apply(region_to_group)
df_fies2018['Greater Region'] = df_fies2018['W_REGN_N'].apply(region_to_group)


# CSS 
external_stylesheets = [
    'https://stackpath.bootstrapcdn.com/bootswatch/4.5.2/cosmo/bootstrap.min.css',
    'https://codepen.io/chriddyp/pen/bWLwgP.css', 
    'styles.css'
]

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Choropleth Maps", href="#1-title-heading")),
        dbc.NavItem(dbc.NavLink("Expenditure Composition", href="#2-title-heading")),
        dbc.NavItem(dbc.NavLink("Income Composition", href="#3-title-heading")),
        dbc.NavItem(dbc.NavLink("Scatterplot Matrix", href="#4-title-heading")),
    ],
    brand="About",
    brand_href="#main-title-heading",
    color="dark",
    dark=True,
)

app.layout = html.Div([
    navbar,
    
# App layout
html.Div([
    html.Br(),
    html.Br(),
    html.H1("A Profile of Family Income and Expenditures (FIES) in the Philippines", id="main-title-heading", style={'font-family': 'Lora, serif'}),
    html.P("Explore the FIES 2018 and 2021 datasets from the Philippine Statistics Authority", style={'font-family': 'Open Sans, sans-serif'}),
    html.Br(),
    html.Br(),
    html.H1("Income and Expenditures by Region and Province", style={'font-family': 'Lora', 'margin-bottom': '3px'}),
    html.P("The choropleth maps below illustrate the income or expenditure of families by median or total for the years 2018 and 2021. You can click specific regions to drill down and view the same variable for provinces in that region", style={'font-family': 'Open Sans'}),
    html.Br(),

    html.Div(id='region-info', style={'vertical-align': 'top', 'display': 'flex', 'alignItems': 'flex-start', 'width': '20%', 'display': 'inline-block'}, children=[
        html.P('Select Year:'),
        dcc.RadioItems(
            id='app1-year-selector',
            options=[
                {'label': '2018', 'value': '2018'},
                {'label': '2021', 'value': '2021'}
            ],
            value='2018',
            labelStyle={'display': 'inline-block', 'margin': '10px'},
            className='radio-group'
        ),
        
        html.P('Select Variable:'),
        dcc.RadioItems(
            id='variable-selector',
            options=[
                {'label': 'Income', 'value': 'TOINC'},
                {'label': 'Expenditure', 'value': 'TOTEX'}
            ],
            value='TOINC',
            labelStyle={'display': 'inline-block', 'margin': '10px'},
            className='radio-group'
        ),
        
        html.P('Select Aggregation:'),
        dcc.RadioItems(
            id='aggregation-selector',
            options=[
                {'label': 'Median', 'value': 'Median'},
                {'label': 'Sum', 'value': 'Sum'}
            ],
            value='Median',
            labelStyle={'display': 'inline-block', 'margin': '10px'},
            className='radio-group'
        ),
    ]),

    # Flex container for maps and region-info
    html.Div(dcc.Graph(id='choropleth-map'), style={'display': 'inline-block', 'width': '40%'}),
    html.Div(dcc.Graph(id='province-map'), style={'display': 'inline-block', 'width': '40%'}),
], style={'width': '90%', 'marginLeft': '5%', 'marginRight': '5%', 'padding': '20px'}),


    # App 2 layout
html.Div([
    html.H1("Drilling Down on Food and Nonfood Spending", style={'font-family': 'Lora', 'margin-bottom': '3px'}),
    html.P("The interactive chart below presents the total food and nonfood expenditures of families per region. You can click the food or nonfood bars on the left chart to visualize the components of the provinces in that region", style={'font-family': 'Open Sans'}),
    html.Br(),
    dcc.RadioItems(
        id='app2-year-selector',
        options=[{'label': str(year), 'value': year} for year in [2018, 2021]],
        value=2018,  # Default value
        style={'marginBottom': 20}, inline=True
    ),
    html.Div([
        dcc.Graph(id='left-graph', style={'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='right-graph', style={'width': '50%', 'display': 'inline-block'})
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%'}),
], style={'width': '90%', 'marginLeft': '5%', 'marginRight': '5%', 'padding': '20px'}),

    # App 3 layout
html.Div([
    html.Div([
        html.H1("How Filipino Families Earn", style={'font-family': 'Lora', 'margin-bottom': '3px'}),
        html.P("The following graphs break down the percentage shares of the components of family income. You can choose a region and year to visualize what comprises their income and its split per province", style={'font-family': 'Open Sans'}),
        html.Br(),
        dcc.Dropdown(
            id='region-selector',
            # Sort the unique region names before creating dropdown options
            options=[{'label': region, 'value': region} for region in sorted(components_province_df['W_REGN_N'].unique())],
            value=sorted(components_province_df['W_REGN_N'].unique())[0],  # Set the default value to the first alphabetically sorted region
            style={'width': '350px', 'marginBottom': '10px'}  # Fixed width for the dropdown
        ),
        dcc.Dropdown(
            id='year-selector',
            options=[
                {'label': '2018', 'value': '2018'},
                {'label': '2021', 'value': '2021'}
            ],
            value='2018',
            style={'width': '150px', 'marginBottom': '10px'}  # Fixed width for the dropdown
        ),
    ], style={'textAlign': 'left', 'width': '100%'}),

    html.Div([
        dcc.Graph(id='income-donut-chart', style={'width': '50%', 'display': 'inline-block'}),  # Responsive width
        dcc.Graph(id='income-stacked-bar-chart', style={'width': '50%', 'display': 'inline-block'}),  # Responsive width
    ], style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%'}),
], style={'width': '90%', 'marginLeft': '5%', 'marginRight': '5%', 'padding': '20px'}),

    # App 4 Layout
html.Div([
    html.H1("The Relationship Between Income and Expenditures", style={'font-family': 'Lora', 'margin-bottom': '3px'}),
    html.P("The scatterplot matrix visualizes each household as a point on the matrix, segregated into Luzon, Visayas, and Mindanao by color. The top five and bottom five provinces by median income are shown on the bar graphs below too. You can select a year and visualize one or more regions", style={'font-family': 'Open Sans'}),
    html.Br(),
    dcc.RadioItems(
        id='year_dropdown',
        options=[
            {'label': '2018', 'value': 2018},
            {'label': '2021', 'value': 2021}
        ],
        value=2021, inline=True
    ),
    dcc.Checklist(
        id='region_dropdown',
        options=[
            {'label': 'Luzon', 'value': 'Luzon'},
            {'label': 'Visayas', 'value': 'Visayas'},
            {'label': 'Mindanao', 'value': 'Mindanao'}
        ],
        value=['Luzon', 'Visayas', 'Mindanao'], inline=True
    ),
    dcc.Graph(id='scatter_matrix'), 
    html.Div(id='top_bottom_charts')
], style={'width': '90%', 'marginLeft': '5%', 'marginRight': '5%', 'padding': '20px'})
])

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lora:wght@700&family=Open+Sans&display=swap');
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# APP 1 CALLBACKS
# Callback for updating the choropleth map
@app.callback(
    Output('choropleth-map', 'figure'),
    [Input('app1-year-selector', 'value'),
     Input('variable-selector', 'value'),
     Input('aggregation-selector', 'value')]
)
def update_map(selected_year, selected_variable, selected_aggregation):
    column_name = f'{selected_year}_{selected_variable}_{selected_aggregation}'
    df['log_value'] = np.log(df[column_name] + 1)
    fig = px.choropleth_mapbox(df, geojson=geo_ph_regions, locations='Region_Code', color='log_value',
                               color_continuous_scale="Blugrn",
                               mapbox_style="white-bg",
                               range_color=(df['log_value'].min(), df['log_value'].max()),
                               zoom=4, center={"lat": 12, "lon": 121},
                               opacity=0.5,
                               labels={'log_value': f'Log of {selected_variable} {selected_aggregation}'},
                               custom_data=['W_REGN_N_2021', column_name]
                              )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, showlegend=False)
    fig.update_layout(coloraxis_showscale=False)
    fig.update_traces(hovertemplate="<b>Region:</b> %{customdata[0]} <br><b>Value:</b> %{customdata[1]:,.0f}")
    return fig

@app.callback(
    Output('province-map', 'figure'),
    [Input('choropleth-map', 'clickData'),  # Listening to clickData as well
     Input('choropleth-map', 'selectedData'),
     Input('app1-year-selector', 'value'),
     Input('variable-selector', 'value'),
     Input('aggregation-selector', 'value')]
)
def update_province_map(clickData, selectedData, selected_year, selected_variable, selected_aggregation):
    # Determine the region code based on click or selection
    if clickData:
        region_code = clickData['points'][0]['location']
    elif selectedData and selectedData['points']:
        region_code = selectedData['points'][0]['location']
    else:
        region_code = 1700000000  # Default/fallback value

    center = region_centers.get(region_code, {'lat': 12, 'lon': 121})    
    geojson_url = f'https://raw.githubusercontent.com/faeldon/philippines-json-maps/master/2023/geojson/regions/medres/provdists-region-{int(region_code)}.0.01.json'
    
    try:
        response = requests.get(geojson_url)
        geojson_provinces = response.json()
    except Exception as e:
        return px.scatter_mapbox()

    filtered_province_df = province_df[province_df['Region_Code'] == region_code]
    column_name = f'{selected_year}_{selected_variable}_{selected_aggregation}'
    if selected_aggregation == 'Sum':
        filtered_province_df['log_value'] = np.log(filtered_province_df[column_name] + 1)
        color_column = 'log_value'
    else:
        color_column = column_name

    fig = px.choropleth_mapbox(filtered_province_df, geojson=geojson_provinces, locations='Province_Code', color=color_column,
                               color_continuous_scale="Blugrn",
                               mapbox_style="white-bg",
                               zoom=5, center=center,
                               opacity=0.5,
                               labels={color_column: f'Log of {selected_variable} {selected_aggregation}'},
                               custom_data=['W_PROV_N', column_name]
                               )
    fig.update_layout(margin={"r":0, "t":0, "l":0, "b":0})
    fig.update_layout(coloraxis_showscale=False)
    fig.update_layout(font_family="Open Sans")
    fig.update_traces(hovertemplate="<b>Province:</b> %{customdata[0]} <br><b>Value:</b> %{customdata[1]:,.0f}")
    return fig

# APP 2 CALLBACKS
@app.callback(
    Output('left-graph', 'figure'),
    Input('app2-year-selector', 'value'))
def update_left_graph(selected_year):

    # Define the specific order for the regions
    region_order_2021 = [
        'National Capital Region',
        'Region III - Central Luzon',
        'Region VI - Western Visayas',
        'Region IVA - CALABARZON',
        'Cordillera Administrative Region',
        'Region VIII - Eastern Visayas',
        'Region VII - Central Visayas',
        'Region X - Northern Mindanao',
        'Region V - Bicol',
        'Region IVB - MIMAROPA',
        'Region XI - Davao',
        'Region XIII - Caraga',
        'Region XII - SOCCSKSARGEN',
        'Region II - Cagayan Valley',
        'Region I - Ilocos Region',
        'Autonomous Region in Muslim Mindanao',
        'Region IX - Zamboanga Peninsula'
    ]

    region_order_2018 = [
        'National Capital Region',
        'Region III - Central Luzon',
        'Region VI - Western Visayas',
        'Region IVA - CALABARZON',
        'Region VIII - Eastern Visayas',
        'Cordillera Administrative Region',
        'Region VII - Central Visayas',
        'Region X - Northern Mindanao',
        'Region V - Bicol',
        'Region XIII - Caraga',
        'Region IVB - MIMAROPA',
        'Region XI - Davao',
        'Region XII - SOCCSKSARGEN',
        'Region I - Ilocos Region',
        'Region II - Cagayan Valley',
        'Region IX - Zamboanga Peninsula',
        'Autonomous Region in Muslim Mindanao'
    ]

    region_order_2021 = region_order_2021[::-1]
    region_order_2018 = region_order_2018[::-1]

    # Select the region order based on the selected year
    region_order = region_order_2021 if selected_year == 2021 else region_order_2018

    # Filter the data
    df_filtered = exp_province_df.copy()

    # Set the order in the dataframe
    df_filtered['W_REGN_N'] = pd.Categorical(df_filtered['W_REGN_N'], categories=region_order, ordered=True)

    # Sort by the predefined region order
    df_filtered = df_filtered.sort_values('W_REGN_N')

    # Plotting the graph with updated labels
    fig = px.bar(df_filtered, y='W_REGN_N', x=[f'FOOD_{selected_year}', f'NFOOD_{selected_year}'],
                 labels={'value': 'Total', 'W_REGN_N': 'Region', 'variable': 'Component'},
                 color_discrete_map={f'FOOD_{selected_year}': '#88CCEE', f'NFOOD_{selected_year}': '#44AA99'},
                 orientation='h')

    # Update trace names for the legend
    for trace in fig.data:
        if trace.name == f'FOOD_{selected_year}':
            trace.name = 'Food'
        elif trace.name == f'NFOOD_{selected_year}':
            trace.name = 'Nonfood'

    fig.update_layout(showlegend=True, yaxis={'visible': True, 'showticklabels': True})
    fig.update_layout(yaxis_title=None)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=None, traceorder="normal"))
    fig.update_layout(margin=dict(r=3))
    return fig

# Callback to update the right graph based on click data from the left graph
@app.callback(
    Output('right-graph', 'figure'),
    [Input('left-graph', 'clickData'),
     Input('app2-year-selector', 'value')])
def update_right_graph(click_data, selected_year):
    # Set default values if no click data is provided (on initial load)
    if click_data is None:
        region_clicked = 'National Capital Region'
        category_clicked = 'FOOD'
    else:
        region_clicked = click_data['points'][0]['y']
        category_clicked = 'FOOD' if click_data['points'][0]['curveNumber'] == 0 else 'NFOOD'

    df_region = exp_province_df[exp_province_df['W_REGN_N'] == region_clicked]
    
    # Define and update the components based on the clicked category
    components = ['BREAD', 'MEAT', 'FISH', 'FOODOUTSIDE', 'VEG', 'MILK', 'FRUIT', 'OTHERFOOD'] if category_clicked == 'FOOD' else ['HOUSINGWATER', 'MISCELLANEOUS', 'TRANSPORT', 'COMMUNICATION', 'HEALTH', 'DURABLE', 'OCCASION', 'FURNISHING', 'OTHERNFOOD']
    components = [f"{component}_{selected_year}" for component in components]

    df_region['total'] = df_region[components].sum(axis=1)
    for component in components:
        df_region[component] = df_region[component] / df_region['total']

    df_melted = pd.melt(df_region, id_vars=['W_PROV_N'], value_vars=components, var_name='Component', value_name='Share')
    df_melted['Component'] = df_melted['Component'].str.replace('_' + str(selected_year), '').map(legend_updates)

    color_discrete_map = {
        'Rice & Bread': '#999999',
        'Meat': '#E69F00',
        'Fish & Seafood': '#56CC59',
        'Food Outside': '#6B6B47',
        'Vegetables': '#5F9ED1',
        'Milk & Dairy': '#0D5EAF',
        'Fruits': '#F0027F',
        'Others': '#4A6B6E',  # Used for OTHERFOOD and OTHERNFOOD
        'Housing & Utilities': '#8B6F47',
        'Miscellaneous': '#AA4499',
        'Transportation': '#D2B48C',
        'Communication': '#E69F00',
        'Healthcare': '#117733',
        'Durable Equipment': '#669999',
        'Special Occasions': '#CC9999',
        'Furniture & Appliances': '#5E644F'
    }
    
    # Create the plot
    fig = px.bar(df_melted, y='W_PROV_N', x='Share', color='Component', labels={'W_PROV_N': 'Province'},
                 orientation='h', color_discrete_map=color_discrete_map)
    fig.update_layout(showlegend=True)
    fig.update_layout(yaxis_title=None)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=None, traceorder="normal"))
    return fig

# App 3 Callbacks
# Callback for updating the scatter matrix
@app.callback(
    [Output('income-donut-chart', 'figure'),
     Output('income-stacked-bar-chart', 'figure')],
    [Input('region-selector', 'value'),
     Input('year-selector', 'value')]
)
def update_income_charts(selected_region, selected_year):
    filtered_df = components_province_df[components_province_df['W_REGN_N'] == selected_region]
    income_components = ['WAGES','EAINC','OTHER_INC','CASH_ABROAD','CASH_DOMESTIC','NET_RECEIPT','REGFT']

    # Aggregate the data for the entire region
    region_aggregated_df = filtered_df.groupby('W_REGN_N')[[f'{component}_{selected_year}' for component in income_components]].sum().reset_index()
    
    labels_map = {
        'WAGES': 'Wages',
        'CASH_ABROAD': 'Remittances',
        'CASH_DOMESTIC': 'Domestic Earnings',
        'NET_RECEIPT': 'Net Receipts',
        'REGFT': 'Gifts',
        'EAINC': 'Entrepreneurship',
        'OTHER_INC': 'Other Income'
    }
    
    component_colors = {
        'Wages': '#56B4E9',
        'Remittances': '#CC79A7',
        'Domestic Earnings': '#F0E442',
        'Net Receipts': '#882255',
        'Gifts': '#0072B2',
        'Entrepreneurship': '#009E73',
        'Other Income': '#D55E00'
    }
    
    values = region_aggregated_df[[f'{component}_{selected_year}' for component in income_components]].iloc[0].tolist()
    labels = [labels_map[component] for component in income_components]

    # Use the labels_map to get the correct color for each label
    colors = [component_colors[label] for label in labels]

    donut_fig = px.pie(values=values, names=labels, hole=0.5, 
                       color=labels,
                       color_discrete_map=component_colors)
    donut_fig.update_traces(textinfo='percent+label', textposition='outside',
                            hovertemplate="<b>Component:</b> %{label}<br><b>Sum:</b> %{value}<extra></extra>")
    donut_fig.update_layout(showlegend=False)

    components = [f'{component}_{selected_year}' for component in income_components]
    province_data = filtered_df.groupby('W_PROV_N_2018')[components].sum().reset_index()
    province_data['Total'] = province_data[components].sum(axis=1)
    
    for component in income_components:
        percentage_column = f'{component}_{selected_year}'
        province_data[percentage_column] = province_data[percentage_column] / province_data['Total'] * 100
        province_data.rename(columns={percentage_column: labels_map[component]}, inplace=True)

    stacked_fig = px.bar(province_data, x=labels, y='W_PROV_N_2018',
                         labels={'value': '% Share', 'variable': 'Component', 'W_PROV_N_2018': 'Province'},
                         orientation='h', color_discrete_sequence=colorscale)
    
    # Customizing the hover template
    stacked_fig.update_traces(hovertemplate="<b>% Share:</b> %{x:.2f} <br><b>Province:</b> %{y}")
    stacked_fig.update_layout(barmode='stack', xaxis={'range': [0, 100]}, showlegend=True)
    stacked_fig.update_layout(yaxis_title=None)
    
    stacked_fig.update_layout(plot_bgcolor='white')
    stacked_fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, title=None, traceorder="normal"))
    
    return donut_fig, stacked_fig

# App 4 Callbacks
# Define scatterplot matrix callback
#This creates the actual scatterplot matrix
@app.callback(
    Output('scatter_matrix', 'figure'),
    Input('year_dropdown', 'value'),
    Input('region_dropdown', 'value')
)
def update_scatter_matrix(year, regions):
    if year == 2018:
        df = df_fies2018.copy()
    else:
        df = df_fies2021.copy()
    
    if regions:
        df = df[df['Greater Region'].isin(regions)]

    df['TOTEX_scaled'] = df['TOTEX'] / 1000000
    df['TOINC_scaled'] = df['TOINC'] / 1000000
    
    color_discrete_map = {'Luzon': '#56B4E9', 'Visayas': '#CC79A7', 'Mindanao': '#009E73'}

    fig_splom = px.scatter_matrix(df,
                                  dimensions=["TOTEX_scaled", "FSIZE", "TOINC_scaled"],
                                  color="Greater Region",
                                  color_discrete_map=color_discrete_map,
                                  labels={col: col.replace('_', ' ') for col in df.columns},
                                  hover_data={'W_REGN_N':True,'W_PROV_N':True})
    
    hover_template = '<b>X-Axis:</b> %{x:,.2f}<br>' + \
                 '<b>Y-Axis:</b> %{y:,.2f}<br>' + \
                 '<b>Region:</b> %{customdata[0]}<br>' + \
                 '<b>Province:</b> %{customdata[1]}'
    fig_splom.update_traces(hovertemplate=hover_template)
    
    fig_splom.update_traces(diagonal_visible=False)
    fig_splom.update_layout(xaxis=dict(title='Expenditure (in M)'),
                             xaxis2=dict(title='Family Size'),
                             xaxis3=dict(title='Income (in M)'),
                             yaxis=dict(title='Expenditure (in M)'),
                             yaxis2=dict(title='Family Size'),
                             yaxis3=dict(title='Income (in M)'))
    fig_splom.update_traces(marker=dict(line=dict(color='white', width=0.5)))
    fig_splom.update_layout(height=800)
    fig_splom.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    return fig_splom

# Define top/bottom bar chart callback
#Now creating the top 3 bottom 3 charts
@app.callback(
    Output('top_bottom_charts', 'children'),
    Input('year_dropdown', 'value'),
    Input('region_dropdown', 'value')
)
def update_top_bottom_charts(year, regions):
    if year == 2018:
        df = df_fies2018.copy()
    else:
        df = df_fies2021.copy()
    
    if regions:
        df = df[df['Greater Region'].isin(regions)]


    grouped_data = df.groupby(['Greater Region','W_REGN_N','W_PROV_N'])['TOINC'].median().reset_index()
    sorted_data = grouped_data.sort_values(['Greater Region', 'TOINC'], ascending=[True, False])
    top_bottom_data = pd.concat([
        sorted_data.groupby('Greater Region').head(5),
        sorted_data.groupby('Greater Region').tail(5)
    ])

    top_chart_data = top_bottom_data.groupby(['Greater Region']).head(5)
    bottom_chart_data = top_bottom_data.groupby(['Greater Region']).tail(5)
    
    color_discrete_map = {'Luzon': '#56B4E9', 'Visayas': '#CC79A7', 'Mindanao': '#009E73'}
    
    top_chart_data = top_chart_data.sort_values(by='TOINC', ascending=True)
    bottom_chart_data = bottom_chart_data.sort_values(by='TOINC', ascending=True)
    region_order = ['Mindanao', 'Visayas', 'Luzon']

    top_chart = px.bar(top_chart_data, y='W_PROV_N', x='TOINC', color='Greater Region',
                       labels={'TOINC': 'Total Income'},
                       title='Top 5 Provinces by Greater Region and Income',
                       height=300,
                       text_auto='.2s',
                       color_discrete_map=color_discrete_map,
                       category_orders={'Greater Region': region_order},orientation='h',hover_data={'W_REGN_N': True})
    top_chart.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    top_chart.update_layout(showlegend=False)
    top_chart.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    top_chart.update_yaxes(title_text='')
    top_chart.update_xaxes(title_text='', showticklabels=False)
    top_chart.update_layout(height=500)
    top_chart.update_traces(
    hovertemplate='<b>Province:</b> %{y}<br>' +
                  '<b>Region:</b> %{customdata}<br>' +
                  '<b>Median Income:</b> %{x:,.0f}'
    )

    bottom_chart = px.bar(bottom_chart_data, y='W_PROV_N', x='TOINC', color='Greater Region',
                          labels={'TOINC': 'Total Income'},
                          title='Bottom 5 Provinces by Greater Region and Income',
                          height=300,
                          text_auto='.2s',
                          color_discrete_map=color_discrete_map,
                          category_orders={'Greater Region': region_order},orientation='h',hover_data={'W_REGN_N': True})
    bottom_chart.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    bottom_chart.update_layout(showlegend=False)
    bottom_chart.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False)
    bottom_chart.update_yaxes(title_text='')
    bottom_chart.update_xaxes(title_text='', showticklabels=False)
    bottom_chart.update_layout(height=500)
    bottom_chart.update_traces(
    hovertemplate='<b>Province:</b> %{y}<br>' +
                  '<b>Region:</b> %{customdata}<br>' +
                  '<b>Median Income:</b> %{x:,.0f}'
    )


    return html.Div([
        html.Div([
            dcc.Graph(figure=top_chart)
        ], className='six columns'),
        html.Div([
            dcc.Graph(figure=bottom_chart)
        ], className='six columns')
    ], className='row')

if __name__ == '__main__':
    app.run_server(debug=True)


# In[ ]:




