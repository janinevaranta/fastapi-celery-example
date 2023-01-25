FROM node:lts AS build

WORKDIR /app

COPY ./package*.json ./

RUN npm install

COPY . /app

RUN npm run build

# Start a nginx proxy server to serve static files and direct api calls.
FROM nginx:1.23.0-alpine

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

COPY --from=build /app/dist/ /usr/share/nginx/html

CMD ["nginx", "-g", "daemon off;"]