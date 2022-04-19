import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collect import get_data
import numpy as np
import re
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import collect
from dash import dash_table as dt
import plotly.express as px
import datetime as t

global table_value


data = pd.read_csv('Data/final_data.csv')
data_age = pd.read_csv('Data/age_data.csv')
system_value = pd.pivot_table(data_age, values='valeur',columns=['mois'],index=['category'],aggfunc=np.sum, fill_value=0).reset_index()
age_value = pd.pivot_table(data_age, values='valeur',columns=['mois'],index=['bucket'],aggfunc=np.sum, fill_value=0).reset_index()
table_value = data.groupby(['mois']).sum()
table_value['% Stock losses'] = np.round(table_value['loss']/table_value['valeur'] *100,2)
table_value = table_value.transpose().reset_index()
table_value.drop([0],inplace=True)
# table_value.rename(columns= {'index':'KPI'},inplace=True)

# kpi_chart = px.line(data, x='mois', y=['valeur','loss','reimburse'], title='Valeur, perte et remboursement par mois')
#
# age_chart = px.line(data_age, x='mois', y='valeur',color='bucket', title='Stock value par tranche par mois')


print(table_value.shape)
print(table_value.to_dict('records'))


table_header_style = {
    "backgroundColor": "rgb(2,21,70)",'minWidth': '0px', 'maxWidth': '100px', 'width': '10px',
    "color": "white",
    "textAlign": "center",
}

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
            dcc.Interval(
                            id='interval-component',
                            interval=1*43200000,
                            n_intervals=0
                        ),
            dbc.Row([
                dbc.Col([html.H1('Oolu Logistique KPI',
                                style={
                                    'textAlign': 'center',
                                    'color': 'white', "font-family": "Montserrat"
                                    }),
                         ],width={'size': 5, 'offset': 4}, ),
            ]),
            dbc.Row([
                dbc.Row([
                    dbc.Col([
                        html.A([html.Img(src=app.get_asset_url('oolu.png'),
                                     id='oolu-logo',
                                     style={
                                         "height": "30px",
                                         "width": "auto",
                                         # "margin-bottom": "25px",
                                     }, )]),
                    ],width={'size': 1}),
                    dbc.Col([
                        dcc.Dropdown(id = 'pays',multi=False,
                                        options=[{'label':x, 'value':x} for x in data['country'].unique()],
                                        placeholder="Country",
                                        className='form-dropdown',
                                        style={'width':'200px', "font-family": "Montserrat"}
                                     )
                        ],width={'size': 3, 'offset':0}),
                    dbc.Col([html.P(id ='refresh' ,children='Last update  :  ' f'{t.date.today()}',
                                       style={
                                               'textAlign': 'right',
                                               'color': 'orange',
                                               'fontSize': 16}),
                                 ],width={'size': 5, 'offset': 2}, ),

                    ],className="card_container twelve columns"),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.H4(children='Stock KPI ',style={ 'textAlign': 'center','color': 'white'}),
                    dt.DataTable(
                        id='valeur',
                        style_header=table_header_style,
                        columns=[{'name': i, 'id': i} for i in table_value.columns],
                        # style_table={'height': '600px', 'overflowY': 'auto'}
                        style_table={'height': '250px', 'overflowY': 'auto', "font-family": "Montserrat"},
                        fixed_rows={'headers': True},
                        style_cell={'minWidth': '0px', 'maxWidth': '100px', 'width': '50px', 'fontSize': 11,
                                    'backgroundColor': '#1f2c56', 'color': 'white',
                                    'textAlign': 'center', "font-family": "Montserrat"},
                        export_format="csv", ),
                ],width={'size': 7, 'offset':0})
            ]),
            # dbc.Row([
            #     dbc.Col([html.Div([
            #             html.H4(children='Valeur, perte et remboursement par mois',
            #                     style={ 'textAlign': 'center','color': 'white', "font-family": "Montserrat"}
            #                     ),
            #             dcc.Graph(id='kpi_char',figure={},
            #                    ),],style={'overflow-x': 'scrol'})
            #         ],width={'size': 4},)
            # ]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.H4(children='Valeur des Systemes complets ',style={ 'textAlign': 'center','color': 'white'}),
                    dt.DataTable(
                        id='syst_val',
                        style_header=table_header_style,
                        columns=[{'name': i, 'id': i} for i in system_value.columns],
                        # style_table={'height': '600px', 'overflowY': 'auto'}
                        style_table={'height': '250px', 'overflowY': 'auto', "font-family": "Montserrat"},
                        fixed_rows={'headers': True},
                        style_cell={'minWidth': '0px', 'maxWidth': '100px', 'width': '50px', 'fontSize': 11,
                                    'backgroundColor': '#1f2c56', 'color': 'white',
                                    'textAlign': 'center', "font-family": "Montserrat"},
                        export_format="csv", ),
                ],width={'size': 7, 'offset':0})
            ]),
            # dbc.Row([
            #     dbc.Col([html.Div([
            #             html.H4(children='Stock value par tranche d\'age par mois',
            #                     style={ 'textAlign': 'center','color': 'white', "font-family": "Montserrat"}
            #                     ),
            #             dcc.Graph(id='age_char',figure={},
            #                    ),],style={'overflow-x': 'scrol'})
            #         ],width={'size': 4},)
            # ]),
            dbc.Row([
                dbc.Col([
                    html.Br(),
                    html.H4(children='Valeur des Systemes complets par tranche d\'age ',style={ 'textAlign': 'center','color': 'white'}),
                    dt.DataTable(
                        id='age_val',
                        style_header=table_header_style,
                        columns=[{'name': i, 'id': i} for i in age_value.columns],
                        # style_table={'height': '600px', 'overflowY': 'auto'}
                        style_table={'height': '250px', 'overflowY': 'auto', "font-family": "Montserrat"},
                        fixed_rows={'headers': True},
                        style_cell={'minWidth': '0px', 'maxWidth': '100px', 'width': '50px', 'fontSize': 11,
                                    'backgroundColor': '#1f2c56', 'color': 'white',
                                    'textAlign': 'center', "font-family": "Montserrat"},
                        export_format="csv", ),
                ],width={'size': 7, 'offset':0})
            ]),
])

@app.callback(
    [Output('valeur','data'),
     Output('syst_val','data'),
     Output('age_val','data'),
     ],
    Input('pays','value')
)
def udpdate_data(c):
    if not c :
        table_value = data.groupby('mois').sum()
        table_value['% Stock losses'] = np.round(table_value['loss'] / table_value['valeur'] * 100, 2)
        table_value = table_value.transpose().reset_index()
        table_value.drop([0], inplace=True)
        system_value = pd.pivot_table(data_age, values='valeur', columns=['mois'], index=['category'], aggfunc=np.sum,
                                      fill_value=0).reset_index()
        age_value = pd.pivot_table(data_age, values='valeur', columns=['mois'], index=['bucket'], aggfunc=np.sum,
                                   fill_value=0).reset_index()

        return table_value.to_dict('records'),system_value.to_dict('records'),age_value.to_dict('records')
    else:
        table_value = data[data['country']==c].groupby('mois').sum()
        table_value['% Stock losses'] = np.round(table_value['loss'] / table_value['valeur'] * 100, 2)
        table_value = table_value.transpose().reset_index()
        table_value.drop([0], inplace=True)
        system_value = pd.pivot_table(data_age[data_age['country']==c], values='valeur', columns=['mois'], index=['category'], aggfunc=np.sum,
                                      fill_value=0).reset_index()
        age_value = pd.pivot_table(data_age[data_age['country']==c], values='valeur', columns=['mois'], index=['bucket'], aggfunc=np.sum,
                                   fill_value=0).reset_index()
        return table_value.to_dict('records'),system_value.to_dict('records'),age_value.to_dict('records')

@app.callback(
    Output('refresh','children'),
    Input('interval-component','n_intervals')
)
def udpdate_data(n):
    if n>0 :
        print('App refreshed')
        data = pd.read_csv('Data/final_data.csv')
        data_age = pd.read_csv('Data/age_data.csv')

        return 'Last update  :  ' f'{t.date.today()}'




if __name__ == '__main__':
    app.run_server(debug=True,dev_tools_ui=False, host='0.0.0.0', port=8855)
