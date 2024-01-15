from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO
import locale

# Configurando a localidade para português do Brasil
locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

graph_margin=dict(l=25, r=25, t=25, b=0)

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        html.H1('Análises',
                style={'textAlign': 'center',
                       'margin': 'auto',
                       'padding-top': '20px',
                       'padding-bottom': '20px'}),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Filtrar por ano', className='card-title'),
                html.Label('Ano'),
                dcc.Checklist(
                    id='checklist-ano',
                    persistence=True,
                    persistence_type='session',
                    labelStyle={'display': 'inline-block',
                                'margin-left': '10px',
                                'margin-right': '15px',
                                'font-size': '20px'},  # Estilo para cada checkbox
                    inputStyle={'margin-right': '5px'},
                    style={'width': '100%', 'text-align': 'center'},  # Estilo para o container dos checkboxes)
                ),
            ], style={'height': '100%', 'padding': '20px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Filtrar por mês', className='card-title'),
                html.Label('Mês'),
                dcc.Checklist(
                    id='checklist-mes',
                    persistence=True,
                    persistence_type='session',
                    labelStyle={'display': 'inline-block',
                                'margin-left': '10px',
                                'margin-right': '15px',
                                'font-size': '20px'},  # Estilo para cada checkbox
                    inputStyle={'margin-right': '5px'},
                    style={'width': '100%', 'text-align': 'center'},  # Estilo para o container dos checkboxes)
                ),
            ], style={'height': '100%', 'padding': '20px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Filtrar por dia', className='card-title'),
                html.Label('Dia da semana'),
                dcc.Checklist(
                    id='checklist-dia',
                    persistence=True,
                    persistence_type='session',
                    labelStyle={'display': 'inline-block',
                                'margin-left': '10px',
                                'margin-right': '15px',
                                'font-size': '20px'},  # Estilo para cada checkbox,
                    inputStyle={'margin-right': '5px'},
                    style={'width': '100%', 'text-align': 'center'},  # Estilo para o container dos checkboxes)
                    ),
            ], style={'height': '100%', 'padding': '20px'})
        ], width=4),
    ]),
    html.Br(),
    dbc.Row(
        dbc.Col(
            dbc.Card(dcc.Graph(id='graph-analise-1'), style={'height': '100%', 'padding': '10px'}),
            width=12
        )
    ),
    html.Br(),
    dbc.Row([
        html.H3('Médias',
        style={'textAlign': 'center',
                'margin': 'auto',
                'padding-top': '20px',
                'padding-bottom': '20px'}),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Média por ano(s)', className='card-title'),
                html.Div(id='media-anual', className='card-text'),
                html.Div(id='media-ano', className='card-text'),
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Média por mês', className='card-title'),
                html.Div(id='media-mensal', className='card-text'),
                html.Div(id='media-mes', className='card-text'),
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Média por dia da semana', className='card-title'),
                html.Div(id='media-diaria', className='card-text'),
                html.Div(id='media-dia', className='card-text'),
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
        ], width=4),
    ]),
    html.Br(),
    html.Br(),
    html.H3('Melhor indicador',
        style={'textAlign': 'center',
                'margin': 'auto',
                'padding-top': '20px',
                'padding-bottom': '20px'}),
    dbc.Row([
        dbc.Col([], width=4),
        dbc.Col([
            dbc.Card([
                html.Div(id='melhor-ano', className='card-text'),
                html.Div(id='melhor-mes', className='card-text'),
                html.Div(id='melhor-dia', className='card-text'),
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
            ], width=4),
        dbc.Col([], width=4),
    ]),
    html.Br(),
    html.Br()
])

# =========  Callbacks  =========== #
@app.callback(
    [Output('checklist-ano', 'options'),
     Output('checklist-ano', 'value')],
    [Input('store-receitas', 'data'),
    Input('store-despesas', 'data')]
)
def update_checklist_ano(data_receitas, data_despesas):
    df_receitas = pd.DataFrame.from_dict(data_receitas)
    df_despesas = pd.DataFrame.from_dict(data_despesas)
    df_receitas['Data'] = pd.to_datetime(df_receitas['Data'])
    df_despesas['Data'] = pd.to_datetime(df_despesas['Data'])
    anos = np.unique(df_receitas['Data'].dt.year.tolist() + df_despesas['Data'].dt.year.tolist())
    return ([{'label': ano, 'value': ano} for ano in anos], anos)

@app.callback(
    [Output('checklist-mes', 'options'),
     Output('checklist-mes', 'value')],
    [Input('store-receitas', 'data'),
    Input('store-despesas', 'data')],
)
def update_checklist_mes(data_receitas, data_despesas):
    df_receitas = pd.DataFrame.from_dict(data_receitas)
    df_despesas = pd.DataFrame.from_dict(data_despesas)
    df_receitas['Data'] = pd.to_datetime(df_receitas['Data'])
    df_despesas['Data'] = pd.to_datetime(df_despesas['Data'])
    meses = np.unique(df_receitas['Data'].dt.month.tolist() + df_despesas['Data'].dt.month.tolist())
    [{'label': calendar.month_name[mes].capitalize(), 'value': mes} for mes in meses]
    return ([{'label': calendar.month_name[mes].capitalize(), 'value': mes} for mes in meses], meses)

@app.callback(
    [Output('checklist-dia', 'options'),
     Output('checklist-dia', 'value')],
    [Input('store-receitas', 'data'),
    Input('store-despesas', 'data')],
)
def update_checklist_dia(data_receitas, data_despesas):
    df_receitas = pd.DataFrame.from_dict(data_receitas)
    df_despesas = pd.DataFrame.from_dict(data_despesas)
    df_receitas['Data'] = pd.to_datetime(df_receitas['Data'])
    df_despesas['Data'] = pd.to_datetime(df_despesas['Data'])
    dias = np.unique(df_receitas['Data'].dt.dayofweek.tolist() + df_despesas['Data'].dt.dayofweek.tolist())

    return ([{'label': calendar.day_name[dia].capitalize(), 'value': dia} for dia in dias], dias)

@app.callback(
    Output('graph-analise-1', 'figure'),
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("checklist-ano", "value"),
    Input("checklist-mes", "value"),
    Input('checklist-dia', "value"),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")])
def update_output(data_despesa, data_receita, ano, mes, dia, theme):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)
    
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    df_final = pd.concat(dfs)
    
    df_final['Ano'] = df_final['Data'].dt.year
    df_final['Mês'] = df_final['Data'].dt.month
    df_final['Dia'] = df_final['Data'].dt.day
    df_final['Dia_semana'] = df_final['Data'].dt.dayofweek

    df_final = df_final[df_final['Ano'].isin(ano) & df_final['Mês'].isin(mes) & df_final['Dia_semana'].isin(dia)]

    fig = px.bar(df_final, x="Data", y="Valor", color='Output', barmode="group")
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_layout(
        title={
            'text': "Receitas e Despesas x Data",
            'y':0.95,
            'x':0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
    )
    return fig

@app.callback(
    [Output('media-anual', 'children'),
     Output('media-ano', 'children')],
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("checklist-ano", "value")]
)
def update_media(data_despesa, data_receita, ano):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)
    
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    df_final = pd.concat(dfs)
    
    df_final['Ano'] = df_final['Data'].dt.year

    df_final = df_final[df_final['Ano'].isin(ano)]

    media_anual = df_final.groupby('Ano')['Valor'].sum().mean()
    
    year = ''
    for i in ano:
        year = year + str(i) + ', '

    return f'R$ {media_anual:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'), f'Anos: {year}'

@app.callback(
    [Output('media-mensal', 'children'),
     Output('media-mes', 'children')],
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("checklist-mes", "value")]
)
def update_media(data_despesa, data_receita, mes):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)
    
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    df_final = pd.concat(dfs)
    
    df_final['Mês'] = df_final['Data'].dt.month

    df_final = df_final[df_final['Mês'].isin(mes)]

    media_mensal = df_final.groupby('Mês')['Valor'].sum().mean()
    
    month = ''
    for i in mes:
        month = month + calendar.month_name[i].capitalize() + ', '

    return f'R$ {media_mensal:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'), f'Meses: {month}'

@app.callback(
    [Output('media-diaria', 'children'),
     Output('media-dia', 'children')],
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("checklist-dia", "value")]
)
def update_media(data_despesa, data_receita, dia):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)
    
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Receitas'
    df_ds['Output'] = 'Despesas'
    df_final = pd.concat(dfs)
    
    df_final['Dia_semana'] = df_final['Data'].dt.dayofweek

    df_final = df_final[df_final['Dia_semana'].isin(dia)]

    media_diaria = df_final.groupby('Dia_semana')['Valor'].sum().mean()
    
    day = ''
    for i in dia:
        day = day + calendar.day_name[i].capitalize() + ', '

    return f'R$ {media_diaria:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.'), f'Dias: {day}'

@app.callback(
    [Output('melhor-ano', 'children'),
     Output('melhor-mes', 'children'),
     Output('melhor-dia', 'children')],
    [Input('store-despesas', 'data'),
     Input('store-receitas', 'data'),]
)
def update_media(data_despesa, data_receita):
    # Carrega os dados em DataFrames
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)
    
    # Converte a coluna 'Data' para datetime
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])

    # Define a coluna 'Output' e concatena os DataFrames
    df_ds['Output'] = 'Despesas'
    df_rc['Output'] = 'Receitas'
    df_final = pd.concat([df_ds, df_rc])
    
    # Extrai ano, mês, dia e dia da semana
    df_final['Ano'] = df_final['Data'].dt.year
    df_final['Mês'] = df_final['Data'].dt.month
    df_final['Dia'] = df_final['Data'].dt.day
    df_final['Dia_semana'] = df_final['Data'].dt.dayofweek

    # Agrupa por Ano, Mês e Dia da semana e calcula a soma
    media_anual = df_final.groupby('Ano')['Valor'].sum()
    media_mensal = df_final.groupby(['Ano', 'Mês'])['Valor'].sum()
    media_diaria = df_final.groupby(['Ano', 'Mês', 'Dia', 'Dia_semana'])['Valor'].sum()

    # Encontra o melhor ano, mês e dia
    melhor_ano_valor = media_anual.max()
    melhor_ano = media_anual.idxmax()

    melhor_mes = media_mensal.idxmax()
    melhor_mes_valor = media_mensal.max()

    melhor_dia = media_diaria.idxmax()
    melhor_dia_valor = media_diaria.max()

    # Formata a saída
    melhor_ano_str = f'Melhor ano: {melhor_ano} - R$ {melhor_ano_valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    melhor_mes_str = f'Melhor mês: {calendar.month_name[melhor_mes[1]].capitalize()} de {melhor_mes[0]} - R$ {melhor_mes_valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    melhor_dia_str = (
        f'Melhor dia: {calendar.day_name[melhor_dia[3]].capitalize()} - '
        f'{melhor_dia[2]} de {calendar.month_name[melhor_dia[1]].capitalize()} de {melhor_dia[0]} - '
        f'R$ {melhor_dia_valor:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    )
    return melhor_ano_str, melhor_mes_str, melhor_dia_str