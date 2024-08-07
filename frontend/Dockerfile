# Etapa 1: Construção
FROM node:16 AS build

# Definir o diretório de trabalho
WORKDIR /app

# Copiar arquivos de configuração e instalar dependências
COPY package.json package-lock.json ./
RUN npm install

# Copiar o código da aplicação
COPY . .

# Construir a aplicação
RUN npm run build

# Etapa 2: Serviço com Nginx
FROM nginx:alpine

# Copiar os arquivos construídos para o diretório do Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# Expor a porta que o Nginx usará
EXPOSE 80

# Comando para iniciar o Nginx
CMD ["nginx", "-g", "daemon off;"]
