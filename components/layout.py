from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

# Carregar dados de 2023 e 2024 em CSV com separador correto
dados_2023 = pd.read_csv('data/dados_2023.csv', encoding='latin1', sep=';', on_bad_lines='skip')
dados_2024 = pd.read_csv('data/dados_2024.csv', encoding='latin1', sep=';', on_bad_lines='skip')

# Converter as colunas TOTAL e QT para numérico, forçando erros para NaN
dados_2023['TOTAL'] = pd.to_numeric(dados_2023['TOTAL'], errors='coerce')
dados_2023['QT'] = pd.to_numeric(dados_2023['QT'], errors='coerce')
dados_2024['TOTAL'] = pd.to_numeric(dados_2024['TOTAL'], errors='coerce')
dados_2024['QT'] = pd.to_numeric(dados_2024['QT'], errors='coerce')

# Remover NaNs se necessário
dados_2023 = dados_2023.dropna(subset=['TOTAL', 'QT'])
dados_2024 = dados_2024.dropna(subset=['TOTAL', 'QT'])

# Calcular os totais e o crescimento
total_2023 = dados_2023['TOTAL'].sum()
total_2024 = dados_2024['TOTAL'].sum()
crescimento = (total_2024 - total_2023) / total_2023 * 100

# Combinar as duas tabelas para uma visão geral consolidada
data = pd.concat([dados_2023, dados_2024])

# Layout principal do dashboard
layout = html.Div(style={'backgroundColor': '#111111', 'color': '#FFFFFF'}, children=[
    
    # Barra de cabeçalho
    dbc.Navbar(
        dbc.Container([ 
            dbc.Row([ 
                dbc.Col(html.Img(src='/assets/logo.png', height="40px")),
                dbc.Col(html.H1("Dashboard Dia Wine", style={'textAlign': 'center', 'color': '#F6C62D'}))
            ], align="center", justify="center")
        ]),
        color="#151D52", dark=True, style={'margin-bottom': '20px'}
    ),

    # Seção de Visão Geral
    dbc.Container([
        html.H2("Visão Geral", style={'color': '#F6C62D'}),
        dbc.Row([
            dbc.Col([
                html.H4("Faturamento Total"),
                html.P(f"2023: R${total_2023:,.2f}"),
                html.P(f"2024: R${total_2024:,.2f}"),
                html.P(f"Crescimento: {crescimento:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col([
                html.H4("Quantidade de Garrafas"),
                html.P(f"2023: {dados_2023['QT'].sum():.0f}"),
                html.P(f"2024: {dados_2024['QT'].sum():.0f}"),
                html.P(f"Crescimento: {(dados_2024['QT'].sum() - dados_2023['QT'].sum()) / dados_2023['QT'].sum() * 100:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col([
                html.H4("Quantidade de Clientes"),
                html.P(f"2023: {dados_2023['CODCLI'].nunique():.0f}"),
                html.P(f"2024: {dados_2024['CODCLI'].nunique():.0f}"),
                html.P(f"Crescimento: {(dados_2024['CODCLI'].nunique() - dados_2023['CODCLI'].nunique()) / dados_2023['CODCLI'].nunique() * 100:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'})
        ])
    ], style={'margin-bottom': '30px'}),

    # Seção de Filtros
    dbc.Container([
        html.H2("Filtros", style={'color': '#F6C62D'}),
        dbc.Row([
            dbc.Col([
                html.Label("RCA", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-rca',
                    options=[{'label': i, 'value': i} for i in data['CODUSUR'].unique()],
                    value='Todos',
                    style={'color': '#000000', 'backgroundColor': '#F6C62D'}
                )
            ], width=3),
            dbc.Col([
                html.Label("Cliente", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-cliente',
                    options=[{'label': i, 'value': i} for i in data['CODCLI'].unique()],
                    value='Todos',
                    style={'color': '#000000', 'backgroundColor': '#F6C62D'}
                )
            ], width=3),
            dbc.Col([
                html.Label("Data Início", style={'color': '#F6C62D'}),
                dcc.DatePickerSingle(
                    id='filtro-data-inicio',
                    date=data['DTFAT'].min(),
                    style={'color': '#000000', 'backgroundColor': '#F6C62D'}
                )
            ], width=3),
            dbc.Col([
                html.Label("Data Fim", style={'color': '#F6C62D'}),
                dcc.DatePickerSingle(
                    id='filtro-data-fim',
                    date=data['DTFAT'].max(),
                    style={'color': '#000000', 'backgroundColor': '#F6C62D'}
                )
            ], width=3),
        ], style={'margin-bottom': '10px'}),
        dbc.Row([
            dbc.Col([
                html.Label("Seguimento", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-seguimento',
                    options=[{'label': i, 'value': i} for i in data['RAMO'].unique()],
                    value='Todos',
                    style={'color': '#000000', 'backgroundColor': '#F6C62D'}
                )
            ], width=3),
            dbc.Col([
                html.Label("Departamento", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-departamento',
                    options=[{'label': i, 'value': i} for i in data['CODEPTO'].unique()],
                    value='Todos',
                    style={'color': '#000000', 'backgroundColor': '#F6C62D'}
                )
            ], width=3),
            dbc.Col([
                html.Label("Produto", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-produto',
                    options=[{'label': i, 'value': i} for i in data['CODPROD'].unique()],
                    value='Todos',
                    style={'color': '#000000', 'backgroundColor': '#F6C62D'}
                )
            ], width=3),
            dbc.Col([
                html.Label("Supervisor", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-supervisor',
                    options=[{'label': i, 'value': i} for i in data['SUPERVISOR'].unique()],
                    value='Todos',
                    style={'color': '#000000', 'backgroundColor': '#F6C62D'}
                )
            ], width=3),
        ])
    ], style={'margin-bottom': '30px'}),

    # Seção de Tabela e Gráficos
    dbc.Container([
        html.H2("Resultados", style={'color': '#F6C62D'}),
        dash_table.DataTable(
            id='tabela',
            columns=[{"name": col, "id": col} for col in data.columns],
            style_table={'overflowX': 'auto'},
            style_cell={
                'textAlign': 'left',
                'padding': '5px',
                'backgroundColor': '#1E1E1E',
                'color': 'white'
            }
        ),
        dcc.Graph(id='grafico1', config={'displayModeBar': False}),
        dcc.Graph(id='grafico2', config={'displayModeBar': False})
    ], style={'margin-top': '30px'})
])
