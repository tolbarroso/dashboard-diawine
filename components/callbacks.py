from dash import Output, Input, ctx
import pandas as pd

# Função para registrar callbacks
def register_callbacks(app):
    @app.callback(
        Output('tabela-principal', 'data'),
        [
            Input('filtro-cod-cliente', 'value'),
            Input('filtro-rca', 'value'),
            Input('filtro-data-inicio', 'date'),
            Input('filtro-data-fim', 'date'),
            Input('filtro-seguimento', 'value'),
            Input('filtro-departamento', 'value'),
            Input('filtro-cod-produto', 'value'),
            Input('filtro-supervisor', 'value'),
        ]
    )
    def update_table(cod_cliente, rca, data_inicio, data_fim, seguimento, departamento, cod_produto, supervisor):
        # Carregar dados
        dados_2023 = pd.read_excel('data/dados_2023.xlsx', sheet_name='dados_2023')
        dados_2024 = pd.read_excel('data/dados_2024.xlsx', sheet_name='dados_2024')
        
        # Combinar dados de 2023 e 2024
        dados_combinados = pd.concat([dados_2023, dados_2024])

        # Aplicar filtros
        if cod_cliente and cod_cliente != 'Todos':
            dados_combinados = dados_combinados[dados_combinados['COD CLIENTE'] == cod_cliente]

        if rca and rca != 'Todos':
            dados_combinados = dados_combinados[dados_combinados['RCA'] == rca]

        if data_inicio:
            dados_combinados = dados_combinados[dados_combinados['DT FAT'] >= data_inicio]

        if data_fim:
            dados_combinados = dados_combinados[dados_combinados['DT FAT'] <= data_fim]

        if seguimento and seguimento != 'Todos':
            dados_combinados = dados_combinados[dados_combinados['SEGUIMENTO'] == seguimento]

        if departamento and departamento != 'Todos':
            dados_combinados = dados_combinados[dados_combinados['DEPARTAMENTO'] == departamento]

        if cod_produto and cod_produto != 'Todos':
            dados_combinados = dados_combinados[dados_combinados['COD PROD'] == cod_produto]

        if supervisor and supervisor != 'Todos':
            dados_combinados = dados_combinados[dados_combinados['NOME SUPERVISOR'] == supervisor]

        # Retornar os dados filtrados para a tabela
        return dados_combinados.to_dict('records')
