import dash
from dash import dcc, html
from components.layout import layout  # Layout principal importado do arquivo layout.py
from components.callbacks import register_callbacks  # Função para registrar callbacks
import dash_bootstrap_components as dbc

# Criar aplicação Dash com tema do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "DashBoard Dia Wine"
server = app.server  # Adicionando isto para que o Gunicorn reconheça a aplicação

# Configuração do layout da aplicação
app.layout = layout

# Registrar todos os callbacks
register_callbacks(app)

# Verificar os nomes das abas no arquivo de 2023 e 2024
print(pd.ExcelFile('data/dados_2023.xlsx').sheet_names)
print(pd.ExcelFile('data/dados_2024.xlsx').sheet_names)

# Rodar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)  # Mude debug=True para False em produção
