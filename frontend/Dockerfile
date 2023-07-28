#stage 1
FROM node:latest as node
WORKDIR /app
COPY . .
RUN npm install
RUN npm install axios bootstrap
RUN npm run build --prod
#stage 2
FROM nginx:alpine
COPY --from=node /app/dist/meal-me /usr/share/nginx/html