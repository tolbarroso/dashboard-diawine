from dash import Input, Output
import pandas as pd
import plotly.express as px

# Carregar dados
data = pd.read_excel('data/dados_diawine23_24.xls', sheet_name='dados_diawine23_24')

# Função para registrar callbacks
def register_callbacks(app):
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
        dados_filtrados = data.copy()

        # Aplicar filtros
        if rca and rca != 'Todos':
            dados_filtrados = dados_filtrados[dados_filtrados['RCA'] == rca]
        if cliente and cliente != 'Todos':
            dados_filtrados = dados_filtrados[dados_filtrados['COD CLIENTE'] == cliente]
        if seguimento and seguimento != 'Todos':
            dados_filtrados = dados_filtrados[dados_filtrados['SEGUIMENTO'] == seguimento]
        if departamento and departamento != 'Todos':
            dados_filtrados = dados_filtrados[dados_filtrados['DEPARTAMENTO'] == departamento]
        if produto and produto != 'Todos':
            dados_filtrados = dados_filtrados[dados_filtrados['COD PROD'] == produto]
        if supervisor and supervisor != 'Todos':
            dados_filtrados = dados_filtrados[dados_filtrados['NOME SUPERVISOR'] == supervisor]

        dados_filtrados = dados_filtrados[
            (dados_filtrados['DT FAT'] >= pd.to_datetime(data_inicio)) &
            (dados_filtrados['DT FAT'] <= pd.to_datetime(data_fim))
        ]

        # Seleção de visualização
        if tipo_visualizacao == 'grafico':
            figura = px.bar(dados_filtrados, x='NOME FANTASIA', y='TOTAL', color='RCA', title='Faturamento por Cliente')
            return figura, []
        else:
            dados_tabela = dados_filtrados.to_dict('records')
            return {}, dados_tabela
