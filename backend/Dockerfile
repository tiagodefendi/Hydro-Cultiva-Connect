# Usar uma imagem base oficial do Python
FROM python:3.12

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o arquivo de requisitos e instalar dependências
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Expor a porta que o Django usará
EXPOSE 8000


WORKDIR /app/backend/src
# Comando para iniciar o servidor DjangoCMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
WORKDIR /app
