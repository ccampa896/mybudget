import dash
from dash.dependencies import Input, Output, State
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from conexao_banco import *
from globals import *
from datetime import datetime, date
import plotly.figure_factory as ff


# Função para formatar os valores
def formatar_valor(valor):
    return f"{valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')



from app import app

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        html.Legend('Tabela de Despesas'),
        html.Div(id='tabela-despesas', className='dbc')
    ]),
    
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-despesas', style={'margin-right': '20px'})
        ], width=9),
        
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Despesas"),
                    html.Legend("R$ -", id="valor_despesa_card", style={'font-size': '60px'}),
                    html.H6("Total de despesas")
                ], style={'text-align': 'center', 'padding-top': '30px'})
            )
        ], width=3)
    ]),
        html.Br(),
        html.Br(),
        
        
        dbc.Row([
        html.Legend('Tabela de Receitas'),
        html.Div(id='tabela-receitas', className='dbc')
    ]),
    
    html.Br(),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='bar-graph-receitas', style={'margin-right': '20px'})
        ], width=9),
        
        dbc.Col([
            dbc.Card(
                dbc.CardBody([
                    html.H4("Receitas"),
                    html.Legend("R$ -", id="valor_receita_card", style={'font-size': '60px'}),
                    html.H6("Total de receita")
                ], style={'text-align': 'center', 'padding-top': '30px'})
            )
        ], width=3)
    ]),

], style={'padding': '10px'}),


# =========  Callbacks  =========== #
# Tabela despesas
@app.callback(
    Output('tabela-despesas', 'children'),
    Input('store-despesas', 'data')
)
def imprimir_tabela(data):
    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data']).dt.date

    # Converter a coluna 'Fixo' para string
    df['Fixo'] = df['Fixo'].astype(str)


    # Substituir os valores '0' e '1' por 'Não' e 'Sim'
    df['Fixo'] = df['Fixo'].replace({'0': 'Não', '1': 'Sim'})
    
    df['Valor'] = df['Valor'].apply(formatar_valor)

    df = df.fillna('-')
    df.sort_values(by='Data', ascending=False)
    

    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            if i == "Descrição" or i == "Fixo" 
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df.columns
        ],

        data=df.to_dict('records'),
        filter_action="native",    
        sort_action="native",       
        sort_mode="single",  
        selected_columns=[],        
        selected_rows=[],          
        page_action="native",      
        page_current=0,             
        page_size=10,                        
    ),
    
    return tabela

# Tabela Receitas
@app.callback(
    Output('tabela-receitas', 'children'),
    Input('store-receitas', 'data')
)
def imprimir_tabela(data):
    df = pd.DataFrame(data)
    df['Data'] = pd.to_datetime(df['Data']).dt.date
    
    # Converter a coluna 'Fixo' para string
    df['Fixo'] = df['Fixo'].astype(str)

    # Substituir os valores '0' e '1' por 'Não' e 'Sim'
    df['Fixo'] = df['Fixo'].replace({'0': 'Não', '1': 'Sim'})
    
    df['Valor'] = df['Valor'].apply(formatar_valor)

    df = df.fillna('-')
    df.sort_values(by='Data', ascending=False)
    


    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            if i == "Descrição" or i == "Fixo" 
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df.columns
        ],

        data=df.to_dict('records'),
        filter_action="native",    
        sort_action="native",       
        sort_mode="single",  
        selected_columns=[],        
        selected_rows=[],          
        page_action="native",      
        page_current=0,             
        page_size=10,                        
    ),

    return tabela

# Bar Graph            
@app.callback(
    Output('bar-graph-despesas', 'figure'),
    [Input('store-despesas', 'data')]
)
def bar_chart(data):
    df = pd.DataFrame(data)
    df_grouped = df.groupby("Categoria").sum()[["Valor"]].reset_index()
    graph = px.bar(df_grouped, x='Categoria', y='Valor', title="Despesas Gerais")
    graph.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return graph

# Simple card
@app.callback(
    Output('valor_despesa_card', 'children'),
    Input('store-despesas', 'data')
)
def display_desp(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    valor = formatar_valor(valor)
    
    return f"R$ {valor}"


# Bar Graph            
@app.callback(
    Output('bar-graph-receitas', 'figure'),
    [Input('store-receitas', 'data')]
)
def bar_chart(data):
    df = pd.DataFrame(data)   
    df_grouped = df.groupby("Categoria").sum()[["Valor"]].reset_index()
    graph = px.bar(df_grouped, x='Categoria', y='Valor', title="Receitas Gerais")
    graph.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return graph

# Simple card
@app.callback(
    Output('valor_receita_card', 'children'),
    Input('store-receitas', 'data')
)
def display_desp(data):
    df = pd.DataFrame(data)
    valor = df['Valor'].sum()
    valor = formatar_valor(valor)
    
    return f"R$ {valor}"


