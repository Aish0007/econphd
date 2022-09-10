import plotly.graph_objects as go
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc
import numpy as np

from app import app

# needed if running single page dash app instead
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

cd = pd.read_csv("compiledbase_2021.csv")
cd = cd.dropna(how="all")
cd.columns = ['University', 'Year', 'Name', 'Institution', 'Position', 'Postdoc', 'Ranking', 'Tier', 'Field']

# # Use the same file as base for all_tiers
all_base = pd.read_csv("compiledbase_2021.csv")
all_base = all_base.dropna(how="all")
all_base.columns = ['University', 'Year', 'Name', 'Institution', 'Position', 'Postdoc', 'Ranking', 'Tier', 'Field']
all_tiers_cols = ['University','Year', 'Ranking', 'Tier']
all_tiers = pd.DataFrame(all_base, columns=all_tiers_cols)


all_tiers.Ranking = all_tiers.apply(lambda x: 11 if (x.Ranking == 1 and x.Tier == 1) else x.Ranking, axis=1)
all_tiers.Ranking = all_tiers.apply(lambda x: 12 if (x.Ranking == 1 and x.Tier == 2) else x.Ranking, axis=1)
all_tiers.Ranking = all_tiers.apply(lambda x: 13 if (x.Ranking == 1 and x.Tier == 3) else x.Ranking, axis=1)
d1 = {11: "Academia_1", 12: "Academia_2", 13: "Academia_3", 2 : "Professional_Schools", 3: "Central_Banks", 4: "Other_Govt_Jobs", 5 : "Econ_Consulting", 6 : "Private_Sector_Banks", 7 : "Non-ladder_Academic", 8 : "Postdoc", 9 : "Non-profit", 10 : "Others"}
# all_tiers["Ranking"] = all_tiers["Ranking"].map(d1)
all_tiers.replace({"Ranking": d1},inplace=True)

cd.Ranking = cd.apply(lambda x: 11 if (x.Ranking == 1 and x.Tier == 1) else x.Ranking, axis=1)
cd.Ranking = cd.apply(lambda x: 12 if (x.Ranking == 1 and x.Tier == 2) else x.Ranking, axis=1)
cd.Ranking = cd.apply(lambda x: 13 if (x.Ranking == 1 and x.Tier == 3) else x.Ranking, axis=1)
# cd["Ranking"] = cd["Ranking"].map(d1)
cd.replace({"Ranking": d1},inplace=True)
cd = cd[['University', 'Year', 'Institution', 'Ranking']]

available_uni = all_tiers['University'].unique()
available_categories = all_tiers['Ranking'].unique()
available_years = all_tiers['Year'].unique()
available_inst_years = cd['Year'].unique()
available_uni = np.append(available_uni, 'All')
available_uni = np.sort(available_uni)
new_cat = ['All', 'Econ_Acad', 'All_Academia', 'All_Private']
available_categories = np.append(available_categories, new_cat)
available_categories= np.sort(available_categories)
available_sort_categories = np.delete(available_categories, [3])
available_trend_categories = np.delete(available_categories, [4,5,8])
available_years = np.append(available_years, 'All')
available_years = np.sort(available_years)[::-1]

all_tiers = all_tiers.set_index("University")
cd = cd.set_index("University")


units = {'Percentages': 'In Percentages%', 'Numbers': 'In number'}

# change to app.layout if running as single page app instead
layout = html.Div([
    
    # Header 
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='Economics PhD Placements'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Comparison across Universities and Placement Categories'), className="mb-4")
        ]),

    
        # Choose between percentages and numbers
        dbc.Row([dbc.Col(html.Div(children=[
            html.Label(['Numbers or Percentages:'], style={'font-weight': 'bold', "text-align": "center"}),
            dcc.Dropdown(
                id='percent_nums',
                options=[
                    {'label': 'Percentages', 'value': 'Percentages'},
                    {'label': 'Numbers', 'value': 'Numbers'},
                ],
                value='Percentages',
        #         multi=True,
                style={'width': '100%', 'margin-left': '0px'}
                )])),   

        
        # Choose between years
            dbc.Col(html.Div(children=[
                html.Label(['Year:'], style={'font-weight': 'bold', "text-align": "center"}),
                dcc.Dropdown(
                    id='year',
                    options=[{'label': i, 'value': i} for i in available_years],
                    value=['All'],
                    multi=True,
                    style={'width': '100%', 'margin-right': '10px'}
                    )])),
          
        
        # Sort by category
            dbc.Col(html.Div(children=[
                html.Label(['Sort by:'], style={'font-weight': 'bold', "text-align": "center"}),
                dcc.Dropdown(
                    id='cat_sort',
                    options=[{'label': i, 'value': i} for i in available_sort_categories],
                    value=['Econ_Acad'],
    #                 multi=True,
                    style={'width': '100%', 'margin-right': '10px'}
                    )])),
        ]),          
        
    
    dash_table.DataTable(
        id='year_summary',
#         fixed_columns={'headers': True,'data': 1},
        style_table={'overflowX': 'scroll','padding': 20, 'minWidth': '100%', 'minHeight': '100%'},
        style_header={'backgroundColor': '#25597f', 'color': 'white', 'lineHeight': 5, 'maxHeight': 5},
        style_cell={
            'backgroundColor': 'white',
            'color': 'black',
            'fontSize': 13,
            'font-family': 'Nunito Sans', 'minWidth': 100, 'width': 100, 'maxWidth': 100}),

    
    # Second Sub-section - Trends 
    dbc.Row([
        dbc.Col(dbc.Card(html.H3(children='Category wise trends',
                                 className="text-center text-light bg-primary"), body=True, color="primary"), 
                className="mb-4")
        ]),
    
        
        # Choose University
        dbc.Row([dbc.Col(html.Div(children=[
                html.Label(['University:'], style={'font-weight': 'bold', "text-align": "center"}),
                dcc.Dropdown(
                    id='university',
                    options=[{'label': i, 'value': i} for i in available_uni],
                    value=['Yale', 'MIT', 'Harvard'],
                    multi=True,
                    style={'width': '100%', 'margin-left': '0px'}
                )])),     

        
        # Choose between categories
            dbc.Col(html.Div(children=[
                html.Label(['Placement Category:'], style={'font-weight': 'bold', "text-align": "center"}),
                dcc.Dropdown(
                id='ranking',
                options=[{'label': i, 'value': i} for i in available_trend_categories],
                value=['Academia_1', 'Academia_2', 'Academia_3'],
                multi=True,
                style={'width': '100%', 'margin-right': '10px'}
                )])),
        ]),   
        

    dcc.Graph(id='trend_category'),
        
    # Third Sub-section - Institutions 
    dbc.Row([
        dbc.Col(dbc.Card(html.H3(children='Institutions',
                                 className="text-center text-light bg-primary"), body=True, color="primary"), 
                className="mb-4")
        ]),
    
        
        # Choose University
        dbc.Row([dbc.Col(html.Div(children=[
                html.Label(['University:'], style={'font-weight': 'bold', "text-align": "center"}),
                dcc.Dropdown(
                    id='inst_university',
                    options=[{'label': i, 'value': i} for i in available_uni],
                    value=['Yale'],
                    multi=True,
                    style={'width': '100%', 'margin-left': '0px'}
                )])),  
                 
        # Choose between years
            dbc.Col(html.Div(children=[
                html.Label(['Year:'], style={'font-weight': 'bold', "text-align": "center"}),
                dcc.Dropdown(
                    id='inst_year',
                    options=[{'label': i, 'value': i} for i in available_inst_years],
                    value=['2021'],
                    multi=True,
                    style={'width': '100%', 'margin-right': '10px'}
                )])),

        ]),  
        
        dash_table.DataTable(
            id='inst_summary',
    #         fixed_columns={'headers': True,'data': 1},
            style_table={'overflowX': 'scroll','padding': 20, 'minWidth': '100%', 'minHeight': '100%'},
            style_header={'backgroundColor': '#25597f', 'color': 'white', 'lineHeight': 5, 'maxHeight': 5},
            style_cell={
                'backgroundColor': 'white',
                'color': 'black',
                'fontSize': 13,
                'font-family': 'Nunito Sans',
                'textAlign': 'left'}),

])

])


@app.callback([Output('year_summary', 'data'),
               Output('year_summary', 'columns'),
               Output('trend_category', 'figure'),
               Output('inst_summary', 'data'),
               Output('inst_summary', 'columns')],
              [Input('percent_nums', 'value'),
               Input('ranking', 'value'), 
               Input('year', 'value'),
               Input('university', 'value'),
               Input('inst_university', 'value'),
               Input('inst_year', 'value'),
               Input('cat_sort', 'value')])


def update_graph(per_num, category, choice, uni, inst_uni, inst_year, sort_cat):  
    
    # Data Table
    at = all_tiers.copy().reset_index()
    
    if 'All' in choice:
        at = at.groupby(["University", "Ranking"]).size().reset_index()
    else:
        at = at[at.Year.isin(choice)]
        at = at.groupby(["University", "Ranking"]).size().reset_index()
    
    at = at.rename(columns = {0: "Freq"})
    at_pivot = pd.pivot_table(at, values = "Freq", index = "University", columns="Ranking")
    
    if per_num == "Percentages":
        at_pivot = at_pivot.apply(lambda x : round( 100 * x / float(x.sum()), 2), axis = 1)
        
    acad_names = ['Academia_1', 'Academia_2', 'Academia_3']
    acad_all_names = ['Academia_1', 'Academia_2', 'Academia_3','Professional_Schools']
    pvt_names = ['Private_Sector_Banks', 'Others']
    
    at_pivot['Econ_Acad']= at_pivot[acad_names].sum(axis=1)
    at_pivot['All_Academia']= at_pivot[acad_all_names].sum(axis=1)
    at_pivot['All_Private']= at_pivot[pvt_names].sum(axis=1)
    
    at_pivot = at_pivot.reindex(columns=['Econ_Acad', 'All_Academia', 'All_Private', "Academia_1", "Academia_2","Academia_3", "Professional_Schools", "Central_Banks", "Other_Govt_Jobs", "Econ_Consulting", "Private_Sector_Banks","Non-ladder_Academic", "Postdoc", "Non-profit", "Others"])
    
    at_pivot = at_pivot.sort_values(sort_cat, ascending = False)
    at_pivot = at_pivot.fillna("-") 
    at_pivot = at_pivot.reset_index()
    at_pivot = at_pivot.round(2)
    at_pivot = at_pivot.replace(0, '-')
    
    data = at_pivot.to_dict('records')
    pcolumns = at_pivot.columns
    columns = [{"name": i, "id": i} for i in pcolumns]


    # Trends
    if per_num == "Percentages": 

        at = all_tiers.copy().reset_index()
        at = at.groupby(["University", "Ranking", 'Year']).size().reset_index()
        at = at.rename(columns = {0: "Freq"})

        numpy_array = at.to_numpy()

        if 'All' in uni:

            year = {}

            for row in range(numpy_array.shape[0]):

                value = str(numpy_array[row,2])
                if value in year:
                    year[value]+=numpy_array[row,3]
                else:
                    year[value]=numpy_array[row,3]

            for row in range(numpy_array.shape[0]):
                value = str(numpy_array[row,2])
                numpy_array[row,3]=numpy_array[row,3]*100/year[value]


        else: 

            uni_year = {}

            for row in range(numpy_array.shape[0]):
                value = numpy_array[row,0]+str(numpy_array[row,2])
                if value in uni_year:
                    uni_year[value]+=numpy_array[row,3]
                else:
                    uni_year[value]=numpy_array[row,3]

            for row in range(numpy_array.shape[0]):
                value = numpy_array[row,0]+str(numpy_array[row,2])
                numpy_array[row,3]=numpy_array[row,3]*100/uni_year[value]

        at = pd.DataFrame(numpy_array, columns = ["University", "Ranking", "Year", "Percentage"])
        at = at.groupby(["University", "Ranking", 'Year']).sum().reset_index()

        trend_at = at.copy()
        if 'All' not in category:
            trend_at = trend_at[trend_at.Ranking.isin(category)]

        if 'All' in uni:
            trend_at = trend_at.groupby(["Year"]).sum().reset_index()
            trend_at = trend_at.rename(columns = {0: "Freq"})

        else:
            trend_at = trend_at[trend_at.University.isin(uni)]
            trend_at = trend_at.groupby(["Year", "University"]).sum().reset_index()
            trend_at = trend_at.rename(columns = {0: "Freq"})

        if 'All' in uni:
            trend_at_pivot = pd.pivot_table(trend_at, values = "Percentage", index = "Year")

        else:
            trend_at_pivot = pd.pivot_table(trend_at, values = "Percentage", index = "Year", columns="University")

    else: 
        trend_at = all_tiers.copy().reset_index()
        if 'All' not in category:
            trend_at = trend_at[trend_at.Ranking.isin(category)]

        if 'All' in uni:
            trend_at = trend_at.groupby(["Year"]).size().reset_index()
            trend_at = trend_at.rename(columns = {0: "Freq"})
            trend_at_pivot = pd.pivot_table(trend_at, values = "Freq", index = "Year")

        else:
            trend_at = trend_at[trend_at.University.isin(uni)]
            trend_at = trend_at.groupby(["Year", "University"]).size().reset_index()
            trend_at = trend_at.rename(columns = {0: "Freq"})
            trend_at_pivot = pd.pivot_table(trend_at, values = "Freq", index = "Year", columns="University")

    trend_at_pivot = trend_at_pivot.sort_values(['Year'], ascending = False)

    fig = go.Figure()
    for col in trend_at_pivot.columns:
        fig.add_trace(go.Bar(x= trend_at_pivot.index, y=trend_at_pivot[col].values, 
                                name=col))

        fig.update_layout(yaxis_title=units[per_num], 
                          paper_bgcolor='rgba(0,0,0,0)',
                          plot_bgcolor='rgba(0,0,0,0)',
                          template = "seaborn",
                          margin=dict(t=0), barmode='group')
        
    # Institution Summary
    inst = cd.copy().reset_index()
    inst = inst[inst.Year.isin(inst_year)]
    inst = inst[inst.University.isin(inst_uni)]
    inst = inst.reindex(columns=["Institution", 'Ranking', 'University', 'Year'])
    inst = inst.sort_values(['Year','University'], ascending = False)
    
    inst_data = inst.to_dict('records')
    icolumns = inst.columns
    inst_columns = [{"name": i, "id": i} for i in icolumns]
 

    return data, columns, fig, inst_data, inst_columns


# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)