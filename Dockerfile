# Use uma imagem base
FROM python:3.9-slim

# Crie uma pasta para o app
WORKDIR /app

# Copie os arquivos necessários
COPY . /app

# Instale as dependências
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Exponha a porta para o Dash
EXPOSE 8050

# Defina o comando para iniciar a aplicação usando o Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8050", "app:server"]
