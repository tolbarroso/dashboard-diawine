import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
from dash import dcc, html, dash_table


# Carregar dados
data = pd.read_excel(r'C:\Users\carol.barroso\Documents\GitHub\dashboard-diawine\dados_dia_wine.xls', sheet_name='planilha')


# Criar aplicação Dash
app = dash.Dash(__name__)

# Layout da aplicação
app.layout = html.Div(style={'backgroundColor': '#111111', 'color': '#FFFFFF'}, children=[
    # Visão Geral
    html.H1(children="Dash Board Dia Wine", style={'textAlign': 'center'}),
    html.Div(children=[
        html.H2(children="Visão Geral"),
        html.Div(children=[
            html.Div(children=[
                html.H3(children="Faturamento Total"),
                html.P(children=f"2023: R${data['TOTAL'].sum():.2f}"),
                html.P(children=f"2024: R${data['TOTAL'].sum():.2f}"),  # Substitua pelos dados corretos de 2024
                html.P(children=f"Crescimento: {(data['TOTAL'].sum() - data['TOTAL'].sum()) / data['TOTAL'].sum() * 100:.2f}%")  # Ajuste para calcular o crescimento corretamente
            ]),
            html.Div(children=[
                html.H3(children="Quantidade de Garrafas"),
                html.P(children=f"2023: {data['QT'].sum():.0f}"),
                html.P(children=f"2024: {data['QT'].sum():.0f}"),  # Substitua pelos dados corretos de 2024
                html.P(children=f"Crescimento: {(data['QT'].sum() - data['QT'].sum()) / data['QT'].sum() * 100:.2f}%")
            ]),
            html.Div(children=[
                html.H3(children="Quantidade de Clientes"),
                html.P(children=f"2023: {data['COD CLIENTE'].nunique():.0f}"),
                html.P(children=f"2024: {data['COD CLIENTE'].nunique():.0f}")  # Substitua pelos dados corretos de 2024
            ])
        ])
    ]),

    # Filtros
    html.Div(children=[
        html.H2(children="Filtros"),
        html.Div(children=[
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

    # Gráficos ou Lista de Dados
    html.Div(children=[
        html.H2(children="Resultados"),
        dcc.Graph(id='grafico-principal'),
        dash_table.DataTable(id='tabela-principal')
    ]),

    # Botões de Exportação
    html.Div(children=[
        html.Button("Exportar em PDF", id="botao-pdf", n_clicks=0),
        html.Button("Exportar em Excel", id="botao-excel", n_clicks=0)
    ])
])

# Callbacks para atualizar os gráficos ou tabela
@app.callback(
    [Output('grafico-principal', 'figure'),
     Output('tabela-principal', 'data')],
    [Input('filtro-rca', 'value'),
     Input('filtro-cliente', 'value'),
     Input('filtro-data-inicio', 'date'),
     Input('filtro-data-fim', 'date'),
     Input('filtro-seguimento', 'value'),
     Input('filtro-departamento', 'value'),
     Input('filtro-produto', 'value'),
     Input('filtro-supervisor', 'value'),
     Input('tipo-visualizacao', 'value')]
)
def atualizar_visualizacao(rca, cliente, data_inicio, data_fim, seguimento, departamento, produto, supervisor, tipo_visualizacao):
    # Filtrar dados com base nos parâmetros
    dados_filtrados = data.copy()
    
    if rca != 'Todos':
        dados_filtrados = dados_filtrados[dados_filtrados['RCA'] == rca]
    if cliente != 'Todos':
        dados_filtrados = dados_filtrados[dados_filtrados['COD CLIENTE'] == cliente]
    if seguimento != 'Todos':
        dados_filtrados = dados_filtrados[dados_filtrados['SEGUIMENTO'] == seguimento]
    if departamento != 'Todos':
        dados_filtrados = dados_filtrados[dados_filtrados['DEPARTAMENTO'] == departamento]
    if produto != 'Todos':
        dados_filtrados = dados_filtrados[dados_filtrados['COD PROD'] == produto]
    if supervisor != 'Todos':
        dados_filtrados = dados_filtrados[dados_filtrados['NOME SUPERVISOR'] == supervisor]
    dados_filtrados = dados_filtrados[(dados_filtrados['DT FAT'] >= data_inicio) & (dados_filtrados['DT FAT'] <= data_fim)]

    # Visualização por gráfico ou tabela
    if tipo_visualizacao == 'grafico':
        figura = px.bar(dados_filtrados, x='NOME FANTASIA', y='TOTAL', color='RCA', title='Faturamento por Cliente')
        return figura, []
    else:
        dados_tabela = dados_filtrados.to_dict('records')
        return {}, dados_tabela

# Rodar a aplicação
if __name__ == '__main__':
    app.run_server(debug=True)
