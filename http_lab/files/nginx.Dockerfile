FROM nginx:latest


COPY nginx.conf /etc/nginx/conf.d/

# Gera um certificado ssl para testes, para acesso às páginas via https.
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/nginx/conf.d/mock.key \
    -out /etc/nginx/conf.d/mock.crt -subj "/CN=localhost"

EXPOSE 80
EXPOSE 443
