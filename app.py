from dash import Dash, html
import dash_bootstrap_components as dbc
from components.layout import layout  # Layout principal importado do arquivo layout.py
from components.callbacks import register_callbacks  # Função para registrar callbacks

# Inicializar o aplicativo Dash
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Configurar o layout
app.layout = layout

# Registrar os callbacks
register_callbacks(app)

# Rodar o servidor
if __name__ == "__main__":
    app.run_server(debug=True)
