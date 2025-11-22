# -------------------------
# 1) Build da aplicação
# -------------------------
FROM node:20 AS build

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install

COPY . .
RUN yarn build

# -------------------------
# 2) Servir com Nginx
# -------------------------
FROM nginx:stable

COPY --from=build /app/dist /usr/share/nginx/html

# Remove a config padrão do Nginx
RUN rm /etc/nginx/conf.d/default.conf

# Adiciona nossa config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 5173

CMD ["nginx", "-g", "daemon off;"]
