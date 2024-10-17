from dash import Input, Output
import pandas as pd
import plotly.express as px

# Carregar dados de 2023 e 2024 separadamente
dados_2023 = pd.read_excel('data/dados_2023.xlsx', sheet_name='dados_2023')
dados_2024 = pd.read_excel('data/dados_2024.xlsx', sheet_name='dados_2024')

# Combinar os dados para visualização
data = pd.concat([dados_2023, dados_2024], ignore_index=True)

# Função para registrar callbacks
def register_callbacks(app):
    @app.callback(
        [Output('grafico1', 'figure'),
         Output('grafico2', 'figure'),
         Output('grafico3', 'figure'),
         Output('grafico4', 'figure'),
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

        # Criar gráficos
        fig1 = px.bar(dados_filtrados, x='NOME FANTASIA', y='TOTAL', color='RCA', title='Faturamento por Cliente')
        fig2 = px.line(dados_filtrados, x='DT FAT', y='TOTAL', color='RCA', title='Faturamento ao longo do Tempo')
        fig3 = px.pie(dados_filtrados, names='NOME FANTASIA', values='TOTAL', title='Participação por Cliente')
        fig4 = px.scatter(dados_filtrados, x='QT', y='TOTAL', color='RCA', title='Quantidade vs. Faturamento')

        # Seleção de visualização
        if tipo_visualizacao == 'grafico':
            return fig1, fig2, fig3, fig4, []
        else:
            dados_tabela = dados_filtrados.to_dict('records')
            return {}, {}, {}, {}, dados_tabela