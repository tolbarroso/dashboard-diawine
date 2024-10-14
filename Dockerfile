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
CMD ["python", "app.py"]