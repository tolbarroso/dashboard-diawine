from dash import dcc, html, dash_table
import pandas as pd

# Carregar dados para uso no layout
data = pd.read_excel('data/dados_dia_wine.xls', sheet_name='planilha')

# Layout principal da aplicação, com estrutura dividida em seções
layout = html.Div(style={'backgroundColor': '#111111', 'color': '#FFFFFF'}, children=[
    html.H1("Dash Board Dia Wine", style={'textAlign': 'center'}),
    
    # Seção de Visão Geral
    html.Div([
        html.H2("Visão Geral"),
        html.Div([
            html.Div([
                html.H3("Faturamento Total"),
                html.P(f"2023: R${data['TOTAL'].sum():.2f}"),
                html.P(f"2024: R${data['TOTAL'].sum():.2f}"),
                html.P(f"Crescimento: {(data['TOTAL'].sum() - data['TOTAL'].sum()) / data['TOTAL'].sum() * 100:.2f}%")
            ]),
            html.Div([
                html.H3("Quantidade de Garrafas"),
                html.P(f"2023: {data['QT'].sum():.0f}"),
                html.P(f"2024: {data['QT'].sum():.0f}"),
                html.P(f"Crescimento: {(data['QT'].sum() - data['QT'].sum()) / data['QT'].sum() * 100:.2f}%")
            ]),
            html.Div([
                html.H3("Quantidade de Clientes"),
                html.P(f"2023: {data['COD CLIENTE'].nunique():.0f}"),
                html.P(f"2024: {data['COD CLIENTE'].nunique():.0f}")
            ])
        ])
    ]),
    
    # Seção de Filtros
    html.Div([
        html.H2("Filtros"),
        html.Div([
            html.Label("RCA"),
            dcc.Dropdown(
                id='filtro-rca',
                options=[{'label': i, 'value': i} for i in data['RCA'].unique()],
                value='Todos'
            ),
            html.Label("Código do Cliente"),
            dcc.Dropdown(
                id='filtro-cliente',
                options=[{'label': i, 'value': i} for i in data['COD CLIENTE'].unique()],
                value='Todos'
            ),
            html.Label("Data de Início"),
            dcc.DatePickerSingle(
                id='filtro-data-inicio',
                date=data['DT FAT'].min()
            ),
            html.Label("Data de Término"),
            dcc.DatePickerSingle(
                id='filtro-data-fim',
                date=data['DT FAT'].max()
            ),
            html.Label("Seguimento"),
            dcc.Dropdown(
                id='filtro-seguimento',
                options=[{'label': i, 'value': i} for i in data['SEGUIMENTO'].unique()],
                value='Todos'
            ),
            html.Label("Departamento"),
            dcc.Dropdown(
                id='filtro-departamento',
                options=[{'label': i, 'value': i} for i in data['DEPARTAMENTO'].unique()],
                value='Todos'
            ),
            html.Label("Código do Produto"),
            dcc.Dropdown(
                id='filtro-produto',
                options=[{'label': i, 'value': i} for i in data['COD PROD'].unique()],
                value='Todos'
            ),
            html.Label("Supervisor"),
            dcc.Dropdown(
                id='filtro-supervisor',
                options=[{'label': i, 'value': i} for i in data['NOME SUPERVISOR'].unique()],
                value='Todos'
            ),
            html.Label("Visualizar como"),
            dcc.RadioItems(
                id='tipo-visualizacao',
                options=[{'label': 'Gráfico', 'value': 'grafico'},
                         {'label': 'Lista de Dados', 'value': 'lista'}],
                value='grafico'
            )
        ])
    ]),

    # Seção de Resultados
    html.Div([
        html.H2("Resultados"),
        dcc.Graph(id='grafico-principal'),
        dash_table.DataTable(id='tabela-principal')
    ]),

    # Botões de Exportação
    html.Div([
        html.Button("Exportar em PDF", id="botao-pdf", n_clicks=0),
        html.Button("Exportar em Excel", id="botao-excel", n_clicks=0)
    ])
])
