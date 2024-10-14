from dash import Input, Output
import pandas as pd
import plotly.express as px

# Carregar dados
data = pd.read_excel('data/dados_dia_wine.xls', sheet_name='planilha')

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

        # Seleção de visualização
        if tipo_visualizacao == 'grafico':
            figura = px.bar(dados_filtrados, x='NOME FANTASIA', y='TOTAL', color='RCA', title='Faturamento por Cliente')
            return figura, []
        else:
            dados_tabela = dados_filtrados.to_dict('records')
            return {}, dados_tabela
