from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

# Carregar dados para uso no layout
data = pd.read_excel('data/dados_diawine23_24.xls', sheet_name='dados_diawine23_24')

# Layout principal da aplicação, com estrutura dividida em seções
layout = html.Div(style={'backgroundColor': '#111111', 'color': '#FFFFFF'}, children=[

    # Barra de cabeçalho com logo e título
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
                html.P(f"2023: R${data['TOTAL'].sum():.2f}"),
                html.P(f"2024: R${data['TOTAL'].sum():.2f}"),
                html.P(f"Crescimento: {(data['TOTAL'].sum() - data['TOTAL'].sum()) / data['TOTAL'].sum() * 100:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col([
                html.H4("Quantidade de Garrafas"),
                html.P(f"2023: {data['QT'].sum():.0f}"),
                html.P(f"2024: {data['QT'].sum():.0f}"),
                html.P(f"Crescimento: {(data['QT'].sum() - data['QT'].sum()) / data['QT'].sum() * 100:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col([
                html.H4("Quantidade de Clientes"),
                html.P(f"2023: {data['COD CLIENTE'].nunique():.0f}"),
                html.P(f"2024: {data['COD CLIENTE'].nunique():.0f}")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'})
        ])
    ], style={'margin-bottom': '30px'}),

    # Seção de Filtros
    dbc.Container([
        html.H2("Filtros", style={'color': '#F6C62D'}),
        dbc.Row([
            dbc.Col(dcc.Dropdown(id='filtro-rca', options=[{'label': i, 'value': i} for i in data['RCA'].unique()], value='Todos'), width=3),
            dbc.Col(dcc.Dropdown(id='filtro-cliente', options=[{'label': i, 'value': i} for i in data['COD CLIENTE'].unique()], value='Todos'), width=3),
            dbc.Col(dcc.DatePickerSingle(id='filtro-data-inicio', date=data['DT FAT'].min()), width=3),
            dbc.Col(dcc.DatePickerSingle(id='filtro-data-fim', date=data['DT FAT'].max()), width=3),
        ]),
        dbc.Row([
            dbc.Col(dcc.Dropdown(id='filtro-seguimento', options=[{'label': i, 'value': i} for i in data['SEGUIMENTO'].unique()], value='Todos'), width=3),
            dbc.Col(dcc.Dropdown(id='filtro-departamento', options=[{'label': i, 'value': i} for i in data['DEPARTAMENTO'].unique()], value='Todos'), width=3),
            dbc.Col(dcc.Dropdown(id='filtro-produto', options=[{'label': i, 'value': i} for i in data['COD PROD'].unique()], value='Todos'), width=3),
            dbc.Col(dcc.Dropdown(id='filtro-supervisor', options=[{'label': i, 'value': i} for i in data['NOME SUPERVISOR'].unique()], value='Todos'), width=3),
        ])
    ], style={'margin-bottom': '30px'}),

    # Seção de Resultados e Gráficos
    dbc.Container([
        html.H2("Resultados", style={'color': '#F6C62D'}),
        dbc.Row([
            dbc.Col(dcc.Graph(id='grafico-principal'), width=6, style={'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col(dash_table.DataTable(id='tabela-principal'), width=6, style={'border': '1px solid #F6C62D', 'padding': '10px'})
        ]),
    ], style={'margin-bottom': '30px'}),

    # Botões de Exportação
    dbc.Container([
        dbc.Row([
            dbc.Col(html.Button("Exportar em PDF", id="botao-pdf", n_clicks=0, style={'width': '100%'}), width=2),
            dbc.Col(html.Button("Exportar em Excel", id="botao-excel", n_clicks=0, style={'width': '100%'}), width=2)
        ], justify="center")
    ])
])
