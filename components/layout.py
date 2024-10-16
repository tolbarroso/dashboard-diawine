from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

# Carregar dados de 2023 e 2024 separadamentes
dados_2023 = pd.read_excel('data/dados_2023.csv', sheet_name='dados_2023')
dados_2024 = pd.read_excel('data/dados_2024.csv', sheet_name='dados_2024')

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
                html.P(f"2023: R${dados_2023['TOTAL'].sum():,.2f}"),
                html.P(f"2024: R${dados_2024['TOTAL'].sum():,.2f}"),
                html.P(f"Crescimento: {(dados_2024['TOTAL'].sum() - dados_2023['TOTAL'].sum()) / dados_2023['TOTAL'].sum() * 100:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col([
                html.H4("Quantidade de Garrafas"),
                html.P(f"2023: {dados_2023['QT'].sum():.0f}"),
                html.P(f"2024: {dados_2024['QT'].sum():.0f}"),
                html.P(f"Crescimento: {(dados_2024['QT'].sum() - dados_2023['QT'].sum()) / dados_2023['QT'].sum() * 100:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col([
                html.H4("Quantidade de Clientes"),
                html.P(f"2023: {dados_2023['COD CLIENTE'].nunique():.0f}"),
                html.P(f"2024: {dados_2024['COD CLIENTE'].nunique():.0f}"),
                html.P(f"Crescimento: {(dados_2024['COD CLIENTE'].sum() - dados_2023['COD CLIENTE'].sum()) / dados_2023['COD CLIENTE'].sum() * 100:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'})
        ])
    ], style={'margin-bottom': '30px'}),

    # Seção de Filtros com identificação
    dbc.Container([
        html.H2("Filtros", style={'color': '#F6C62D'}),
        dbc.Row([
            dbc.Col([
                html.Label("RCA", style={'color': '#F6C62D'}),
                dcc.Dropdown(id='filtro-rca', options=[{'label': i, 'value': i} for i in data['RCA'].unique()], 
                             value='Todos', style={'color': '#000000', 'backgroundColor': '#F6C62D'})
            ], width=3),
            dbc.Col([
                html.Label("Cliente", style={'color': '#F6C62D'}),
                dcc.Dropdown(id='filtro-cliente', options=[{'label': i, 'value': i} for i in data['COD CLIENTE'].unique()], 
                             value='Todos', style={'color': '#000000', 'backgroundColor': '#F6C62D'})
            ], width=3),
            dbc.Col([
                html.Label("Data Início", style={'color': '#F6C62D'}),
                dcc.DatePickerSingle(id='filtro-data-inicio', date=data['DT FAT'].min(), 
                                     style={'color': '#000000', 'backgroundColor': '#F6C62D'})
            ], width=3),
            dbc.Col([
                html.Label("Data Fim", style={'color': '#F6C62D'}),
                dcc.DatePickerSingle(id='filtro-data-fim', date=data['DT FAT'].max(), 
                                     style={'color': '#000000', 'backgroundColor': '#F6C62D'})
            ], width=3),
        ], style={'margin-bottom': '10px'}),
        dbc.Row([
            dbc.Col([
                html.Label("Seguimento", style={'color': '#F6C62D'}),
                dcc.Dropdown(id='filtro-seguimento', options=[{'label': i, 'value': i} for i in data['SEGUIMENTO'].unique()], 
                             value='Todos', style={'color': '#000000', 'backgroundColor': '#F6C62D'})
            ], width=3),
            dbc.Col([
                html.Label("Departamento", style={'color': '#F6C62D'}),
                dcc.Dropdown(id='filtro-departamento', options=[{'label': i, 'value': i} for i in data['DEPARTAMENTO'].unique()], 
                             value='Todos', style={'color': '#000000', 'backgroundColor': '#F6C62D'})
            ], width=3),
            dbc.Col([
                html.Label("Produto", style={'color': '#F6C62D'}),
                dcc.Dropdown(id='filtro-produto', options=[{'label': i, 'value': i} for i in data['COD PROD'].unique()], 
                             value='Todos', style={'color': '#000000', 'backgroundColor': '#F6C62D'})
            ], width=3),
            dbc.Col([
                html.Label("Supervisor", style={'color': '#F6C62D'}),
                dcc.Dropdown(id='filtro-supervisor', options=[{'label': i, 'value': i} for i in data['NOME SUPERVISOR'].unique()], 
                             value='Todos', style={'color': '#000000', 'backgroundColor': '#F6C62D'})
            ], width=3),
        ])
    ], style={'margin-bottom': '30px'}),

    # Seção de Resultados e Gráficos
    dbc.Container([
        html.H2("Resultados", style={'color': '#F6C62D'}),
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id='tipo-visualizacao',
                options=[
                    {'label': 'Gráfico', 'value': 'grafico'},
                    {'label': 'Tabela', 'value': 'tabela'}
                ],
                value='grafico',
                style={'color': '#000000', 'backgroundColor': '#F6C62D'}
            ), width=2),
            dbc.Col(dcc.Graph(id='grafico1'), width=6, style={'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col(dcc.Graph(id='grafico2'), width=6, style={'border': '1px solid #F6C62D', 'padding': '10px'})
        ]),
        dbc.Row([
            dbc.Col(dcc.Graph(id='grafico3'), width=6, style={'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col(dcc.Graph(id='grafico4'), width=6, style={'border': '1px solid #F6C62D', 'padding': '10px'})
        ]),
        dbc.Row([ 
            dbc.Col(dash_table.DataTable(id='tabela-principal'), width=12, style={'border': '1px solid #F6C62D', 'padding': '10px'})
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
