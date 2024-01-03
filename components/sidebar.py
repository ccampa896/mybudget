import os
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd
from globals import *
import pdb

from flask import send_file
import os
import zipfile
import io

from dash_bootstrap_templates import ThemeChangerAIO





# ========= Layout ========= #
layout = dbc.Col([
    html.H1("Flor de Mel", className="text-primary"),
    html.P("By @campanaricarlos", className="text-info"),
    html.Hr(),

    # ========= Seção Perfil ========= #
    dbc.Button(id='botao_avatar',
               children=[html.Img(src='/assets/flor_de_mel.png', id='avatar_change',
                                  alt='Avatar', className='perfil_avatar')],
            style={'background-color': 'transparent', 'border-color': 'transparent'}),

    # ========= Seção NOVO ========= #
    dbc.Row([
        dbc.Col([
            dbc.Button(color='success', id='open-novo-receita',
                       children=['+ Receita'])
        ], width=6),
        dbc.Col([
            dbc.Button(color='danger', id='open-novo-despesa',
                       children=['- Despesa'])
        ], width=6)
    ]),

    # Modal Receita
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Adicionar Receita")),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição: '),
                    dbc.Input(placeholder="Ex.: peso, picolé, pote 2l...", id="txt-receita"),
                ], width=6),
                dbc.Col([
                    dbc.Label('Valor: '),
                    dbc.Input(placeholder="R$ 100.00", id="valor_receita", value="")
                ])
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Label('Data: '),
                    dcc.DatePickerSingle(id='date-receita',
                                         min_date_allowed=date(2020, 1, 1),
                                         max_date_allowed=date(2030, 12, 31),
                                         date=date.today(),
                                         style={'width': '100%'})
                ], width=4),

                dbc.Col([
                    dbc.Label('Extras: '),
                    dbc.Checklist(
                        options=[
                            {'label': 'Fixa', 'value': 2},
                            ],
                        value=[1],
                        id='switches-input-receita',
                        switch=True,
                    )
                ], width=4),
                
                
                
                dbc.Col([
                    html.Label('Categoria da receita'),
                    dbc.Select(id='select_receita',
                               options=[{'label': i, 'value': i} for i in cat_receita],
                               value=cat_receita['Categoria'][0] if isinstance(cat_receita, dict) else cat_receita[0])
                ], width=4)
            ], style={'margin-top': '25px'}),

            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Adicionar categoria", style={'color': 'green'}),
                                dbc.Input(type='text', placeholder='Nova Categoria...', id='input-add-receita', value=''),
                                html.Br(),
                                dbc.Button('Adicionar', className='btn btn-success', id='add-category-receita', style={'margin-top': "20px"}),
                                html.Br(),
                                html.Div(id='category-div-add-receita', style={})
                            ]),

                            dbc.Col([
                                html.Legend("Excluir categorias", style={'color': 'red'}),
                                dbc.Checklist(
                                    id='checklist-selected-style-receita',
                                    options=[{"label": i, "value": i} for i in cat_receita],
                                    value=[],
                                    label_checked_style={'color': 'red'},
                                    input_checked_style={'background-color': 'blue', 'borderColor': 'orange'}
                                ),
                                dbc.Button('Remover', color='warning', id='remove-category-receita', style={'margin-top': '20px'}),
                            ], width=6)
                        ])
                    ], title='Adicionar/Remover Categorias')
                ], flush=True, start_collapsed=True, id='accordion-receita'),

                html.Div(id='id_teste_receita', style={'padding-top': '20px'}),
                dbc.ModalFooter([
                    dbc.Button('Adicionar Receita', id='salvar_receita', color='success'),
                    dbc.Popover(dbc.PopoverBody('Receita salva'), target='salvar_receita', placement='left', trigger='click'),
                ])
            ], style={'margin-top': '25px'})
        ])
    ], id='modal-novo-receita',
       style={'background-color': 'rgba(17, 140, 79, 0.05)'},
       size='lg',
       is_open=False,
       centered=True,
       backdrop=True),
    # Modal Despesa
    dbc.Modal([
        dbc.ModalHeader(dbc.ModalTitle("Adicionar Despesa")),
        dbc.ModalBody([
            dbc.Row([
                dbc.Col([
                    dbc.Label('Descrição: '),
                    dbc.Input(placeholder="Ex.: Aluguel, energia, produtos, funcionária...", id="txt-despesa"),
                ], width=6),
                dbc.Col([
                    dbc.Label('Valor: '),
                    dbc.Input(placeholder="R$ 100.00", id="valor_despesa", value="")
                ])
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Label('Data: '),
                    dcc.DatePickerSingle(id='date-despesa',
                                         min_date_allowed=date(2020, 1, 1),
                                         max_date_allowed=date(2030, 12, 31),
                                         date=date.today(),
                                         style={'width': '100%'})
                ], width=4),

                dbc.Col([
                    dbc.Label('Extras: '),
                    dbc.Checklist(
                        options=[
                            {'label': 'Fixa', 'value': 2},
                            ],
                        value=[1],
                        id='switches-input-despesa',
                        switch=True,
                    )
                ], width=4),
                
                dbc.Col([
                    html.Label('Categoria da despesa'),
                    dbc.Select(id='select_despesa',
                               options=[{'label': i, 'value': i} for i in cat_despesa],
                               value=cat_despesa['Categoria'][0] if isinstance(cat_despesa, dict) else cat_despesa[0])
                ], width=4)
            ], style={'margin-top': '25px'}),

            dbc.Row([
                dbc.Accordion([
                    dbc.AccordionItem(children=[
                        dbc.Row([
                            dbc.Col([
                                html.Legend("Adicionar categoria", style={'color': 'green'}),
                                dbc.Input(type='text', placeholder='Nova Categoria...', id='input-add-despesa', value=''),
                                html.Br(),
                                dbc.Button('Adicionar', className='btn btn-success', id='add-category-despesa', style={'margin-top': "20px"}),
                                html.Br(),
                                html.Div(id='category-div-add-despesa', style={})
                            ]),

                            dbc.Col([
                                html.Legend("Excluir categorias", style={'color': 'red'}),
                                dbc.Checklist(
                                    id='checklist-selected-style-despesa',
                                    options=[{"label": i, "value": i} for i in cat_receita],
                                    value=[],
                                    label_checked_style={'color': 'red'},
                                    input_checked_style={'background-color': 'blue', 'borderColor': 'orange'}
                                ),
                                dbc.Button('Remover', color='warning', id='remove-category-despesa', style={'margin-top': '20px'}),
                            ], width=6)
                        ])
                    ], title='Adicionar/Remover Categorias')
                ], flush=True, start_collapsed=True, id='accordion-despesa'),

                html.Div(id='id_teste_despesa', style={'padding-top': '20px'}),
                dbc.ModalFooter([
                    dbc.Button('Adicionar Despesa', id='salvar_despesa', color='success'),
                    dbc.Popover(dbc.PopoverBody('Despesa salva'), target='salvar_despesa', placement='left', trigger='click'),
                ])
            ], style={'margin-top': '25px'})
        ]),
    ], id='modal-novo-despesa',
       style={'background-color': 'rgba(17, 140, 79, 0.05)'},
       size='lg',
       is_open=False,
       centered=True,
       backdrop=True),

    # ========= Seção Nav ========= #
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Dashboard", href="/dashboards", active="exact"),
                    dbc.NavLink("Extratos", href="/extratos", active="exact"),
                ], vertical=True, pills=True, id='nav_buttons', style={"margin-bottom": "50px"}),
            ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.BOOTSTRAP}),
            html.Br(),
            dbc.Button('Baixar Arquivos', id='btn-baixar-arquivos', color='success', className='btn btn-block'),
            dcc.Download(id="download-csv"),

        ], id='sidebar_completa'
    )











# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output('modal-novo-receita', 'is_open'),
    Input('open-novo-receita', 'n_clicks'),
    State('modal-novo-receita', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

# Pop-up despesa
@app.callback(
    Output('modal-novo-despesa', 'is_open'),
    Input('open-novo-despesa', 'n_clicks'),
    State('modal-novo-despesa', 'is_open')
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open

@app.callback(
    Output('store-receitas', 'data'),
    
    Input('salvar_receita', 'n_clicks'),
    [
        State('txt-receita', 'value'),
        State('valor_receita', 'value'),
        State('date-receita', 'date'),
        State('switches-input-receita', 'value'),
        State('select_receita', 'value'),
        State('store-receitas', 'data')
    ]
)
def salve_form_receita(n, descricao, valor, date, switches, categoria, dict_receita):
    df_receitas = pd.DataFrame(dict_receita)
    
    if n and not(valor == '' or valor == None):
        valor = round(float(valor), 2)
        date = pd.to_datetime(date).date()
        categoria = categoria[0] if type(categoria) == list else categoria
        fixa = 1 if 2 in switches else 0
        
        # Criar um novo DataFrame com a nova linha
        new_row = pd.DataFrame([[valor, fixa, date, categoria, descricao]], 
                               columns=df_receitas.columns)

        # Concatenar o novo DataFrame com o DataFrame existente, colocando a nova linha no topo
        df_receitas = pd.concat([new_row, df_receitas]).reset_index(drop=True)
        
        
        df_receitas.to_csv("df_receitas.csv")
    
    data_return = df_receitas.to_dict()
    return data_return

@app.callback(
    Output('store-despesas', 'data'),
    
    Input('salvar_despesa', 'n_clicks'),
    [
        State('txt-despesa', 'value'),
        State('valor_despesa', 'value'),
        State('date-despesa', 'date'),
        State('switches-input-despesa', 'value'),
        State('select_despesa', 'value'),
        State('store-despesas', 'data')
    ]
)
def salve_form_despesa(n, descricao, valor, date, switches, categoria, dict_despesa):
    df_despesas = pd.DataFrame(dict_despesa)
    
    if n and not(valor == '' or valor == None):
        valor = round(float(valor), 2)
        date = pd.to_datetime(date).date()
        categoria = categoria[0] if type(categoria) == list else categoria
        fixa = 1 if 2 in switches else 0
        
        # Criar um novo DataFrame com a nova linha
        new_row = pd.DataFrame([[valor, fixa, date, categoria, descricao]], 
                               columns=df_despesas.columns)

        # Concatenar o novo DataFrame com o DataFrame existente, colocando a nova linha no topo
        df_despesas = pd.concat([new_row, df_despesas]).reset_index(drop=True)
        
        
        df_despesas.to_csv("df_despesas.csv")
    
    data_return = df_despesas.to_dict()
    return data_return


@app.callback(
    [
        Output("select_despesa", "options"),
        Output("checklist-selected-style-despesa", "options"),
        Output("checklist-selected-style-despesa", "value"),
        Output("stored-cat-despesas", "data")
    ],
    [
        Input("add-category-despesa", "n_clicks"),
        Input("remove-category-despesa", "n_clicks"),
    ],
    
    [
        State("input-add-despesa", "value"),
        State("checklist-selected-style-despesa", "value"),
        State("stored-cat-despesas", "data")
    ]
)
def add_category(n, n2, txt, check_delete, data):
    cat_despesa = list(data['Categoria'].values())
    if n and not(txt == '' or txt == None):
        cat_despesa = cat_despesa + [txt] if txt not in cat_despesa else cat_despesa

    if n2:
        if len(check_delete) > 0:
            cat_despesa = [i for i in cat_despesa if i not in check_delete]
    
    opt_despesa = [{'label': i, 'value': i} for i in cat_despesa]
    df_cat_despesa = pd.DataFrame(cat_despesa, columns=['Categoria'])
    df_cat_despesa.to_csv("df_cat_despesa.csv")
    data_return = df_cat_despesa.to_dict()
    
    return [opt_despesa, opt_despesa, [], data_return]

@app.callback(
    [
        Output("select_receita", "options"),
        Output("checklist-selected-style-receita", "options"),
        Output("checklist-selected-style-receita", "value"),
        Output("stored-cat-receitas", "data")
    ],
    [
        Input("add-category-receita", "n_clicks"),
        Input("remove-category-receita", "n_clicks"),
    ],
    
    [
        State("input-add-receita", "value"),
        State("checklist-selected-style-receita", "value"),
        State("stored-cat-receitas", "data")
    ]
)
def add_category(n, n2, txt, check_delete, data):
    cat_receita = list(data['Categoria'].values())
    if n and not(txt == '' or txt == None):
        cat_receita = cat_receita + [txt] if txt not in cat_receita else cat_receita

    if n2:
        if len(check_delete) > 0:
            cat_receita = [i for i in cat_receita if i not in check_delete]
    
    opt_receita = [{'label': i, 'value': i} for i in cat_receita]
    df_cat_receita = pd.DataFrame(cat_receita, columns=['Categoria'])
    df_cat_receita.to_csv("df_cat_receita.csv")
    data_return = df_cat_receita.to_dict()
    
    return [opt_receita, opt_receita, [], data_return]

@app.callback(
    Output("download-csv", "data"),
    [Input("btn-baixar-arquivos", "n_clicks"),
     Input("store-receitas", "data"),
     Input("store-despesas", "data")],
    prevent_initial_call=True,
)
def download_csvs(n_clicks, receitas, despesas):
    if n_clicks is None:
        # O botão não foi clicado ainda
        raise dash.exceptions.PreventUpdate

    df_receitas = pd.DataFrame(receitas)
    df_despesas = pd.DataFrame(despesas)

    # Nome do arquivo zip temporário
    zip_filename = "csv_files.zip"

    # Criar um arquivo zip em memória para enviar ao usuário
    with io.BytesIO() as in_memory:
        with zipfile.ZipFile(in_memory, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Adicionar df1 ao arquivo ZIP
            with io.StringIO() as buffer:
                df_receitas.to_csv(buffer, index=False)
                zipf.writestr('df_receitas.csv', buffer.getvalue())
            
            # Adicionar df2 ao arquivo ZIP
            with io.StringIO() as buffer:
                df_despesas.to_csv(buffer, index=False)
                zipf.writestr('df_despesas.csv', buffer.getvalue())

        # Voltar ao início do buffer
        in_memory.seek(0)
        
        # Iniciar o download do arquivo zip
        return dcc.send_bytes(in_memory.read(), filename=zip_filename)