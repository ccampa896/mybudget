from dash import html, dcc, dash_table
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
                html.Legend('Filtrar por tipo', className='card-title d-flex justify-content-center align-items-center'),
                dcc.Checklist(
                    id='checklist-tipo',
                    options=[
                        {'label': 'Receita', 'value': 'Receita'},
                        {'label': 'Despesa', 'value': 'Despesa'}],
                    value=['Receita', 'Despesa'],
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
        ], width=12, className='d-flex justify-content-center align-items-center'),
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Média por ano(s)', className='card-title'),
                html.Div(id='media-anual', className='card-text'),
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Média por mês', className='card-title'),
                html.Div(id='media-mensal', className='card-text'),
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Média por dia da semana', className='card-title'),
                html.Div(id='media-diaria', className='card-text')
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
        ], width=4),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                html.Legend('Saldo anual', className='card-title'),
                html.Div(id='saldo-anual', className='card-text'),
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Saldo mensal', className='card-title'),
                html.Div(id='saldo-mensal', className='card-text'),
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
        ], width=4),
        dbc.Col([
            dbc.Card([
                html.Legend('Saldo diário', className='card-title'),
                html.Div(id='saldo-diario', className='card-text'),
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
        dbc.Col([
            dbc.Card([
                html.Div(id='melhor-ano', className='card-text')
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})], width=4),
        dbc.Col([
            dbc.Card([
                html.Div(id='melhor-mes', className='card-text'),
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
            ], width=4),
        dbc.Col([
            dbc.Card([
                html.Div(id='melhor-dia', className='card-text')
            ], style={'height': '100%',
                      'padding': '20px',
                      'font-size': '20px'})
        ], width=4),
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
    Output('media-anual', 'children'),
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("checklist-ano", "value"),
    Input("checklist-tipo", "value")]
)
def update_media(data_despesa, data_receita, ano, tipo):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)
    
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Receita'
    df_ds['Output'] = 'Despesa'
    df_final = pd.concat(dfs)
    
    df_final['Ano'] = df_final['Data'].dt.year

    df_final = df_final[df_final['Ano'].isin(ano) & df_final['Output'].isin(tipo)]

    media_anual = df_final.groupby(['Ano', 'Output'])['Valor'].mean()
    
    media_anual = media_anual.to_frame()
    
    media_anual.reset_index(inplace=True)
    media_anual.rename(columns={'Output': 'Tipo'}, inplace=True)
    
    # Função para formatar os valores
    def formatar_valor(valor):
        return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

    # Aplicar a formatação para a coluna 'Valor'
    media_anual['Valor'] = media_anual['Valor'].apply(formatar_valor)
    
    tabela = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in media_anual.columns],
        data=media_anual.reset_index().to_dict('records'),
        style_table={'overflowX': 'auto'},  # Para adicionar rolagem horizontal se necessário
    )
    
    return tabela
    


@app.callback(
    Output('media-mensal', 'children'),
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("checklist-mes", "value"),
    Input("checklist-ano", "value"),
    Input("checklist-tipo", "value")]
)
def update_media(data_despesa, data_receita, mes, ano, tipo):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)
    
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Receita'
    df_ds['Output'] = 'Despesa'
    df_final = pd.concat(dfs)
    
    df_final['Ano'] = df_final['Data'].dt.year
    df_final['Mês'] = df_final['Data'].dt.month

    df_final = df_final[df_final['Ano'].isin(ano) & df_final['Mês'].isin(mes) & df_final['Output'].isin(tipo)]

    media_mensal = df_final.groupby(['Ano', 'Mês', 'Output'])['Valor'].mean()
    
    media_mensal = media_mensal.to_frame()
    
    media_mensal.reset_index(inplace=True)
    media_mensal.rename(columns={'Output': 'Tipo'}, inplace=True)
    
    # Função para formatar os valores
    def formatar_valor(valor):
        return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    # Função para mudar o mês de número para nome
    def formatar_mes(mes):
        return calendar.month_name[mes].capitalize()

    # Aplicar a formatação para a coluna 'Valor'
    media_mensal['Valor'] = media_mensal['Valor'].apply(formatar_valor)
    media_mensal['Mês'] = media_mensal['Mês'].apply(formatar_mes)
    
    tabela = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in media_mensal.columns],
        data=media_mensal.reset_index().to_dict('records'),
        style_table={'overflowX': 'auto'},  # Para adicionar rolagem horizontal se necessário
    )
    
    return tabela

    

@app.callback(
    Output('media-diaria', 'children'),
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("checklist-dia", "value"),
    Input("checklist-mes", "value"),
    Input("checklist-ano", "value"),
    Input("checklist-tipo", "value")]
)
def update_media(data_despesa, data_receita, dia, mes, ano, tipo):
    df_ds = pd.DataFrame(data_despesa)
    df_rc = pd.DataFrame(data_receita)
    
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])

    dfs = [df_ds, df_rc]

    df_rc['Output'] = 'Receita'
    df_ds['Output'] = 'Despesa'
    df_final = pd.concat(dfs)
    
    df_final['Dia_semana'] = df_final['Data'].dt.dayofweek
    df_final['Mês'] = df_final['Data'].dt.month
    df_final['Ano'] = df_final['Data'].dt.year

    df_final = df_final[df_final['Dia_semana'].isin(dia) & df_final['Mês'].isin(mes) & df_final['Ano'].isin(ano) & df_final['Output'].isin(tipo)]

    media_diaria = df_final.groupby(['Ano', 'Mês', 'Dia_semana', 'Output'])['Valor'].mean()
    
    media_diaria = media_diaria.to_frame()
    
    media_diaria.reset_index(inplace=True)
    media_diaria.rename(columns={'Output': 'Tipo'}, inplace=True)
    
    # Função para formatar os valores
    def formatar_valor(valor):
        return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    # Função para mudar o mês de número para nome
    def formatar_mes(mes):
        return calendar.month_name[mes].capitalize()
    
    # Função para mudar o dia da semana de número para nome
    def formatar_dia(dia):
        return calendar.day_name[dia].capitalize()

    # Aplicar a formatação para a coluna 'Valor'
    media_diaria['Valor'] = media_diaria['Valor'].apply(formatar_valor)
    media_diaria['Mês'] = media_diaria['Mês'].apply(formatar_mes)
    media_diaria['Dia_semana'] = media_diaria['Dia_semana'].apply(formatar_dia)
    
    tabela = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in media_diaria.columns],
        data=media_diaria.reset_index().to_dict('records'),
        style_table={'overflowX': 'auto'},  # Para adicionar rolagem horizontal se necessário
    )
    
    return tabela

@app.callback(
    Output('saldo-anual', 'children'),
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("checklist-ano", "value")]
)
def update_saldo(data_despesa, data_receita, ano):
    # Carrega os dados em DataFrames
    df_rc = pd.DataFrame(data_receita)
    df_ds = pd.DataFrame(data_despesa)
    
    # Converte a coluna 'Data' para datetime
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])

    df_rc['Valor_receita'] = df_rc['Valor']
    df_ds['Valor_despesa'] = df_ds['Valor']
    
    
    df_rc['Ano'] = df_rc['Data'].dt.year
    df_ds['Ano'] = df_ds['Data'].dt.year
        
    df_saldo = pd.merge(df_rc, df_ds, on='Data', how='outer')
    df_saldo.fillna(0, inplace=True)
    df_saldo['Saldo'] = df_saldo['Valor_receita'] - df_saldo['Valor_despesa']
    
    df_saldo['Ano'] = df_saldo['Data'].dt.year
    df_saldo = df_saldo.groupby(['Ano'])['Saldo'].sum() 
    
    df_saldo = df_saldo.to_frame()
    
    df_saldo.reset_index(inplace=True)
    
    saldo_anual = df_saldo[df_saldo['Ano'].isin(ano)]
    
    # Função para formatar os valores
    def formatar_valor(valor):
        return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    saldo_anual['Saldo'] = saldo_anual['Saldo'].apply(formatar_valor)
    
    tabela = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in saldo_anual.columns],
        data=saldo_anual.reset_index().to_dict('records'),
        style_table={'overflowX': 'auto'},  # Para adicionar rolagem horizontal se necessário
    )
    
    return tabela

@app.callback(
    Output('saldo-mensal', 'children'),
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("checklist-mes", "value"),
    Input("checklist-ano", "value")]
)
def update_saldo(data_despesa, data_receita, mes, ano):
    # Carrega os dados em DataFrames
    df_rc = pd.DataFrame(data_receita)
    df_ds = pd.DataFrame(data_despesa)
    
    # Converte a coluna 'Data' para datetime
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])

    df_rc['Valor_receita'] = df_rc['Valor']
    df_ds['Valor_despesa'] = df_ds['Valor']
    
    
    df_rc['Ano'] = df_rc['Data'].dt.year
    df_ds['Ano'] = df_ds['Data'].dt.year
        
    df_saldo = pd.merge(df_rc, df_ds, on='Data', how='outer')
    df_saldo.fillna(0, inplace=True)
    df_saldo['Saldo'] = df_saldo['Valor_receita'] - df_saldo['Valor_despesa']
    
    df_saldo['Ano'] = df_saldo['Data'].dt.year
    df_saldo['Mês'] = df_saldo['Data'].dt.month
    df_saldo = df_saldo.groupby(['Ano', 'Mês'])['Saldo'].sum() 
    
    df_saldo = df_saldo.to_frame()
    
    df_saldo.reset_index(inplace=True)
    
    saldo_mensal = df_saldo[df_saldo['Ano'].isin(ano) & df_saldo['Mês'].isin(mes)]
    
    # Função para formatar os valores
    def formatar_valor(valor):
        return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    # Função para mudar o mês de número para nome
    def formatar_mes(mes):
        return calendar.month_name[mes].capitalize()
    
    saldo_mensal['Saldo'] = saldo_mensal['Saldo'].apply(formatar_valor)
    saldo_mensal['Mês'] = saldo_mensal['Mês'].apply(formatar_mes)
    
    tabela = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in saldo_mensal.columns],
        data=saldo_mensal.reset_index().to_dict('records'),
        style_table={'overflowX': 'auto'},  # Para adicionar rolagem horizontal se necessário
    )
    
    return tabela

@app.callback(
    Output('saldo-diario', 'children'),
    [Input('store-despesas', 'data'),
    Input('store-receitas', 'data'),
    Input("checklist-dia", "value"),
    Input("checklist-mes", "value"),
    Input("checklist-ano", "value")]
)
def update_saldo(data_despesa, data_receita, dia, mes, ano):
    # Carrega os dados em DataFrames
    df_rc = pd.DataFrame(data_receita)
    df_ds = pd.DataFrame(data_despesa)
    
    # Converte a coluna 'Data' para datetime
    df_rc['Data'] = pd.to_datetime(df_rc['Data'])
    df_ds['Data'] = pd.to_datetime(df_ds['Data'])

    df_rc['Valor_receita'] = df_rc['Valor']
    df_ds['Valor_despesa'] = df_ds['Valor']
    
    
    df_rc['Ano'] = df_rc['Data'].dt.year
    df_ds['Ano'] = df_ds['Data'].dt.year
        
    df_saldo = pd.merge(df_rc, df_ds, on='Data', how='outer')
    df_saldo.fillna(0, inplace=True)
    df_saldo['Saldo'] = df_saldo['Valor_receita'] - df_saldo['Valor_despesa']
    
    df_saldo['Ano'] = df_saldo['Data'].dt.year
    df_saldo['Mês'] = df_saldo['Data'].dt.month
    df_saldo['Dia_semana'] = df_saldo['Data'].dt.dayofweek
    df_saldo = df_saldo.groupby(['Ano', 'Mês', 'Dia_semana'])['Saldo'].sum() 
    
    df_saldo = df_saldo.to_frame()
    
    df_saldo.reset_index(inplace=True)
    
    saldo_diario = df_saldo[df_saldo['Ano'].isin(ano) & df_saldo['Mês'].isin(mes) & df_saldo['Dia_semana'].isin(dia)]
    
    # Função para mudar o dia da semana de número para nome
    def formatar_dia(dia):
        return calendar.day_name[dia].capitalize()
    
    # Função para formatar os valores
    def formatar_valor(valor):
        return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    
    # Função para mudar o mês de número para nome
    def formatar_mes(mes):
        return calendar.month_name[mes].capitalize()
    
    saldo_diario['Saldo'] = saldo_diario['Saldo'].apply(formatar_valor)
    saldo_diario['Mês'] = saldo_diario['Mês'].apply(formatar_mes)
    saldo_diario['Dia_semana'] = saldo_diario['Dia_semana'].apply(formatar_dia)
    
    tabela = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in saldo_diario.columns],
        data=saldo_diario.reset_index().to_dict('records'),
        style_table={'overflowX': 'auto'},  # Para adicionar rolagem horizontal se necessário
    )
    
    return tabela


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