# Imagem base
FROM python:3.9

# Diretório de trabalho
WORKDIR /app

# Copiar arquivos
COPY . /app

# Instalar dependências
RUN pip install -r requirements.txt

# Expor a porta e iniciar a aplicação
EXPOSE 8050

# Usar Gunicorn para a execução do servidor em produção
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]