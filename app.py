import os
import dash
from dash import dcc, html
from components.layout import layout  # Layout principal importado do arquivo layout.py
from components.callbacks import register_callbacks  # Função para registrar callbacks
import dash_bootstrap_components as dbc

# Criar aplicação Dash com tema do Bootstrap
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
app.title = "DashBoard Dia Wine"

# Adicione o servidor para que Gunicorn possa usá-lo
server = app.server

# Configuração do layout da aplicação
app.layout = layout

# Registrar todos os callbacks
register_callbacks(app)

# Rodar a aplicação localmente, se necessário
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=int(os.environ.get("PORT", 8050)), debug=True)