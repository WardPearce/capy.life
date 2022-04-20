FROM node AS builder
COPY . .

ARG VITE_URL_PROXIED

RUN touch /.env
RUN echo "VITE_URL_PROXIED=${VITE_URL_PROXIED}" > .env

RUN npm install && npm run build


FROM nginx:alpine
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*

RUN rm /etc/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx

COPY --from=builder ./dist .

ENTRYPOINT ["nginx", "-g", "daemon off;"]
