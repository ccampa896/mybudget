import pandas as pd
import os
from app import *
from conexao_banco import *


# Lendo as categorias de receitas e despesas
df_cat_receita = read_data("SELECT nome_categoria FROM cat_receitas", conn)
df_cat_despesa = read_data("SELECT nome_categoria FROM cat_despesas", conn)
cat_receita = df_cat_receita['nome_categoria'].tolist()
cat_despesa = df_cat_despesa['nome_categoria'].tolist()

# Lendo as tabelas de despesas e receitas
df_despesas = read_data("SELECT * FROM despesas", conn)
df_receitas = read_data("SELECT * FROM receitas", conn)

# Convertendo a coluna 'Data' para o formato de data
df_despesas["Data"] = pd.to_datetime(df_despesas["Data"]).dt.date
df_receitas["Data"] = pd.to_datetime(df_receitas["Data"]).dt.date

