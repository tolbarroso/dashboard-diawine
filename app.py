import dash
from dash import dcc, html
from components.layout import layout  # Layout principal importado do arquivo layout.py
from components.callbacks import register_callbacks  # Função para registrar callbacks
import dash_bootstrap_components as dbc
import pandas as pd

# Criar aplicação Dash com tema do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "Dashboard Dia Wine"
server = app.server  # Adicionando isto para que o Gunicorn reconheça a aplicação

# Verificar os dados CSV carregados corretamente
try:
    dados_2023 = pd.read_csv('data/dados_2023.csv', encoding='latin1', sep=';', on_bad_lines='skip')
    print(dados_2023.head())  # Imprime as primeiras linhas do dataframe
except Exception as e:
    print(f"Erro ao ler 'dados_2023.csv': {e}")

try:
    dados_2024 = pd.read_csv('data/dados_2024.csv', encoding='latin1', sep=';', on_bad_lines='skip')
    print(dados_2024.head())  # Imprime as primeiras linhas do dataframe
except Exception as e:
    print(f"Erro ao ler 'dados_2024.csv': {e}")

# Configuração do layout da aplicação
app.layout = layout

# Registrar todos os callbacks
register_callbacks(app)

# Rodar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)  # Mude debug=True para False em produção
