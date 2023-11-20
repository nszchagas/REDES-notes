FROM debian:latest

# Instala as dependências para buildar o curl para os testes (última versão para usar o http3)
# Fonte: https://codedamn.com/news/backend/leveraging-http3-with-nginx
RUN apt-get update && apt-get install -y \
    build-essential libpcre3-dev zlib1g-dev libssl-dev wget checkinstall \
    libcurl4-openssl-dev \
    nghttp2 libnghttp2-dev


RUN mkdir -p /tmp/curl_compile
WORKDIR /tmp/curl_compile

RUN wget https://curl.se/download/curl-7.80.0.tar.gz  
RUN tar -xzvf curl-7.80.0.tar.gz 
RUN cd curl-7.80.0  
# RUN /bin/bash ./configure --with-ssl --with-nghttp2 --enable-ssl --enable-http2 --with-quiche 
# RUN make clean
# RUN make 
# RUN make install
