from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from utils import formata_moeda

# Carregar dados de 2023 e 2024
dados_2023 = pd.read_excel('data/dados_2023.xlsx', sheet_name='dados_2023')
dados_2024 = pd.read_excel('data/dados_2024.xlsx', sheet_name='dados_2024')

# Converter a coluna 'TOTAL' para numérico, substituindo não numéricos por NaN
dados_2023['TOTAL'] = pd.to_numeric(dados_2023['TOTAL'], errors='coerce')
dados_2024['TOTAL'] = pd.to_numeric(dados_2024['TOTAL'], errors='coerce')

# Certificar-se de que os NaN sejam tratados ao somar
total_2023 = dados_2023['TOTAL'].sum()
total_2024 = dados_2024['TOTAL'].sum()

# Converter a coluna 'DT FAT' para datetime, substituindo erros por NaT
dados_2023['DT FAT'] = pd.to_datetime(dados_2023['DT FAT'], errors='coerce')
dados_2024['DT FAT'] = pd.to_datetime(dados_2024['DT FAT'], errors='coerce')

# Layout principal do dashboard
layout = html.Div(style={'backgroundColor': '#111111', 'color': '#FFFFFF'}, children=[
    # Barra de cabeçalho com logo e título
    dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col(html.Img(src='/assets/logo.png', height="40px")),  # Logo
                dbc.Col(html.H1("DASHBOARD DIA WINE", style={'color': '#F6C62D', 'margin-left': '10px'}))  # Título
            ], align="center")
        ]),
        color="#151D52", dark=True, style={'margin-bottom': '20px'}
    ),
    
    # Seção de Visão Geral
    dbc.Container([
        html.H2("Visão Geral", style={'color': '#F6C62D'}),
        dbc.Row([
            dbc.Col([
                html.H4("Faturamento Total"),
                html.P(f"2023: {formata_moeda(total_2023)}"),
                html.P(f"2024: {formata_moeda(total_2024)}"),
                html.P(f"Crescimento: {(total_2024 - total_2023) / total_2023 * 100:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col([
                html.H4("Quantidade de Garrafas"),
                html.P(f"2023: {dados_2023['QT'].sum():.0f}"),
                html.P(f"2024: {dados_2024['QT'].sum():.0f}"),
                html.P(f"Crescimento: {(dados_2024['QT'].sum() - dados_2023['QT'].sum()) / dados_2023['QT'].sum() * 100:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'}),
            dbc.Col([
                html.H4("Quantidade de Clientes"),
                html.P(f"2023: {dados_2023['COD CLIENTE'].nunique()}"),
                html.P(f"2024: {dados_2024['COD CLIENTE'].nunique()}"),
                html.P(f"Crescimento: {(dados_2024['COD CLIENTE'].nunique() - dados_2023['COD CLIENTE'].nunique()) / dados_2023['COD CLIENTE'].nunique() * 100:.2f}%")
            ], style={'textAlign': 'center', 'border': '1px solid #F6C62D', 'padding': '10px'})
        ])
    ], style={'margin-bottom': '30px'}),
    
    # Seção de Filtros
    dbc.Container([
        html.H2("Filtros", style={'color': '#F6C62D'}),
        dbc.Row([
            dbc.Col([
                html.Label("COD CLIENTE", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-cod-cliente',
                    options=[{'label': str(i), 'value': str(i)} for i in sorted(dados_2023['COD CLIENTE'].unique())],
                    value='Todos',
                    style={'backgroundColor': '#F6C62D'}
                )
            ], width=2),
            dbc.Col([
                html.Label("RCA", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-rca',
                    options=[{'label': str(i), 'value': str(i)} for i in sorted(dados_2023['RCA'].unique())],
                    value='Todos',
                    style={'backgroundColor': '#F6C62D'}
                )
            ], width=2),
            dbc.Col([
                html.Label("Data Início", style={'color': '#F6C62D'}),
                dcc.DatePickerSingle(
                    id='filtro-data-inicio',
                    date=dados_2023['DT FAT'].min().date() if not dados_2023['DT FAT'].isnull().all() else None,
                    style={'backgroundColor': '#F6C62D'}
                )
            ], width=2),
            dbc.Col([
                html.Label("Data Fim", style={'color': '#F6C62D'}),
                dcc.DatePickerSingle(
                    id='filtro-data-fim',
                    date=dados_2023['DT FAT'].max().date() if not dados_2023['DT FAT'].isnull().all() else None,
                    style={'backgroundColor': '#F6C62D'}
                )
            ], width=2),
            dbc.Col([
                html.Label("SEGUIMENTO", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-seguimento',
                    options=[{'label': str(i), 'value': str(i)} for i in sorted(dados_2023['SEGUIMENTO'].unique())],
                    value='Todos',
                    style={'backgroundColor': '#F6C62D'}
                )
            ], width=2),
            dbc.Col([
                html.Label("DEPARTAMENTO", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-departamento',
                    options=[{'label': str(i), 'value': str(i)} for i in sorted(dados_2023['DEPARTAMENTO'].unique())],
                    value='Todos',
                    style={'backgroundColor': '#F6C62D'}
                )
            ], width=2),
            dbc.Col([
                html.Label("COD PRODUTO", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-cod-produto',
                    options=[{'label': str(i), 'value': str(i)} for i in sorted(dados_2023['COD PROD'].unique())],
                    value='Todos',
                    style={'backgroundColor': '#F6C62D'}
                )
            ], width=2),
            dbc.Col([
                html.Label("SUPERVISOR", style={'color': '#F6C62D'}),
                dcc.Dropdown(
                    id='filtro-supervisor',
                    options=[{'label': str(i), 'value': str(i)} for i in sorted(dados_2023['NOME SUPERVISOR'].unique())],
                    value='Todos',
                    style={'backgroundColor': '#F6C62D'}
                )
            ], width=2),
        ])
    ]),
    
    # Seção de Resultados (tabela)
    dbc.Container([
        html.H2("Resultados", style={'color': '#F6C62D'}),
        dbc.Row([
            dbc.Col(dash_table.DataTable(
                id='tabela-principal',
                style_header={'backgroundColor': '#151D52', 'color': '#FFFFFF'},
                                style_cell={'backgroundColor': '#111111', 'color': '#FFFFFF'},
                page_action='native',
                page_size=10,
                data=[],  # Inicialmente vazio
                columns=[
                    {"name": "CNPJ", "id": "CNPJ"},
                    {"name": "COD CLIENTE", "id": "COD CLIENTE"},
                    {"name": "NOME FANTASIA", "id": "NOME FANTASIA"},
                    {"name": "RAZÃO SOCIAL", "id": "RAZÃO SOCIAL"},
                    {"name": "BAIRRO", "id": "BAIRRO"},
                    {"name": "MUNICIPIO", "id": "MUNICIPIO"},
                    {"name": "COD PROD", "id": "COD PROD"},
                    {"name": "PRODUTO", "id": "PRODUTO"},
                    {"name": "EMBALAGEM", "id": "EMBALAGEM"},
                    {"name": "QT", "id": "QT"},
                    {"name": "TOTAL", "id": "TOTAL"},
                    {"name": "RCA", "id": "RCA"},
                    {"name": "NOME VENDEDOR", "id": "NOME VENDEDOR"},
                    {"name": "NOME SUPERVISOR", "id": "NOME SUPERVISOR"},
                    {"name": "COD DEPTO", "id": "COD DEPTO"},
                    {"name": "DEPARTAMENTO", "id": "DEPARTAMENTO"},
                    {"name": "COND VENDA", "id": "COND VENDA"},
                    {"name": "DT FAT", "id": "DT FAT"},
                    {"name": "SEGUIMENTO", "id": "SEGUIMENTO"},
                ],
                style_table={'overflowX': 'auto'}
            ), width=12)
        ])
    ])
])
