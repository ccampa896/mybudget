import dash
import dash_bootstrap_components as dbc
import dash_auth
import os
import json
from conexao_banco import *


from dotenv import load_dotenv

load_dotenv()  # Isso carrega as variáveis de ambiente do arquivo .env

# Obtendo as credenciais do banco de dados a partir das variáveis de ambiente
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

# Conecta ao banco de dados
conn = psycopg2.connect(
    dbname=DB_NAME, 
    user=DB_USER, 
    password=DB_PASSWORD, 
    host=DB_HOST, 
    port=DB_PORT
)

# # Obtendo a string de conexão do banco de dados a partir das variáveis de ambiente
# DATABASE_URL = os.environ.get('DATABASE_URL')  # Adicione a variável de ambiente correspondente

# # Conecta ao banco de dados usando a string de conexão completa
# conn = psycopg2.connect(DATABASE_URL)

credenciais_str = os.environ.get('CREDENCIAIS', '{}')
VALID_USERNAME_PASSWORD_PAIRS = json.loads(credenciais_str)


estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", "https://fonts.googleapis.com/icon?family=Material+Icons", dbc.themes.COSMO]
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
# FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"



app = dash.Dash(__name__, external_stylesheets=estilos + [dbc_css])
app.title = "Flor de Mel"

app.config['suppress_callback_exceptions'] = True
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
app.scripts.config.serve_locally = True
server = app.server
