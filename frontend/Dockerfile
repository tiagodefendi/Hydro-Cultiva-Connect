# Etapa 1: Construção
FROM node:16 AS build

# Definir o diretório de trabalho
WORKDIR /app

# Copiar o código da aplicação
COPY . .

# Construir a aplicação
RUN npm run build
