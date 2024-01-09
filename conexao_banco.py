import psycopg2
import pandas as pd
import os

from dotenv import load_dotenv

load_dotenv()  # Isso carrega as variáveis de ambiente do arquivo .env

# # Obtendo as credenciais do banco de dados a partir das variáveis de ambiente
# DB_HOST = os.environ.get('DB_HOST')
# DB_PORT = os.environ.get('DB_PORT')
# DB_NAME = os.environ.get('DB_NAME')
# DB_USER = os.environ.get('DB_USER')
# DB_PASSWORD = os.environ.get('DB_PASSWORD')

# # Conecta ao banco de dados
# conn = psycopg2.connect(
#     dbname=DB_NAME, 
#     user=DB_USER, 
#     password=DB_PASSWORD, 
#     host=DB_HOST, 
#     port=DB_PORT
# )


# Obtendo a string de conexão do banco de dados a partir das variáveis de ambiente
DATABASE_URL = os.environ.get('DATABASE_URL')  # Adicione a variável de ambiente correspondente

# Conecta ao banco de dados usando a string de conexão completa
conn = psycopg2.connect(DATABASE_URL)

# Função para conectar ao banco de dados e ler os dados
def read_data(query, conn):
    try:
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return pd.DataFrame(rows, columns=columns)
    except psycopg2.InterfaceError as e:
        # Reconectar e tentar novamente
        conn = psycopg2.connect(
            dbname=DB_NAME, 
            user=DB_USER, 
            password=DB_PASSWORD, 
            host=DB_HOST, 
            port=DB_PORT
        )
        with conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()
            columns = [desc[0] for desc in cur.description]
            return pd.DataFrame(rows, columns=columns)


def inserir_receita(categoria, data, valor, descricao, fixa, conn):
    if conn.closed:
        # Reconectar; substitua as variáveis de ambiente pelas suas credenciais reais
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'), 
            user=os.environ.get('DB_USER'), 
            password=os.environ.get('DB_PASSWORD'), 
            host=os.environ.get('DB_HOST'), 
            port=os.environ.get('DB_PORT')
        )
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO receitas ("Categoria", "Data", "Valor", "Descrição", "Fixo") VALUES (%s, %s, %s, %s, %s)',
            (categoria, data, valor, descricao, fixa)
        )
        conn.commit()


def inserir_despesas(categoria, data, valor, descricao, fixa, conn):
    if conn.closed:
        # Reconectar; substitua as variáveis de ambiente pelas suas credenciais reais
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'), 
            user=os.environ.get('DB_USER'), 
            password=os.environ.get('DB_PASSWORD'), 
            host=os.environ.get('DB_HOST'), 
            port=os.environ.get('DB_PORT')
        )
    with conn.cursor() as cur:
        cur.execute(
            'INSERT INTO despesas ("Categoria", "Data", "Valor", "Descrição", "Fixo") VALUES (%s, %s, %s, %s, %s)',
            (categoria, data, valor, descricao, fixa)
        )
        conn.commit()


def inserir_categoria(nome_categoria, conn, tabela):
    if conn.closed:
        # Reconectar; substitua as variáveis de ambiente pelas suas credenciais reais
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'), 
            user=os.environ.get('DB_USER'), 
            password=os.environ.get('DB_PASSWORD'), 
            host=os.environ.get('DB_HOST'), 
            port=os.environ.get('DB_PORT')
        )
    with conn.cursor() as cur:
        cur.execute(
            f"INSERT INTO {tabela} (nome_categoria) VALUES (%s)",
            (nome_categoria,)
        )
        conn.commit()


def deletar_categoria(nome_categoria, conn, tabela):
    if conn.closed:
        # Reconectar; substitua as variáveis de ambiente pelas suas credenciais reais
        conn = psycopg2.connect(
            dbname=os.environ.get('DB_NAME'), 
            user=os.environ.get('DB_USER'), 
            password=os.environ.get('DB_PASSWORD'), 
            host=os.environ.get('DB_HOST'), 
            port=os.environ.get('DB_PORT')
        )
    with conn.cursor() as cur:
        cur.execute(
            f"DELETE FROM {tabela} WHERE nome_categoria = %s",
            (nome_categoria,)
        )
        conn.commit()




