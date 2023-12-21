FROM debian:latest

# Instala as dependências para buildar o curl para os testes (última versão para usar o http3)
RUN apt-get update && apt-get install -y \
    build-essential libpcre3-dev zlib1g-dev libssl-dev wget checkinstall \
    libcurl4-openssl-dev \
    nghttp2 libnghttp2-dev

RUN mkdir -p /tmp/curl_compile
WORKDIR /tmp/curl_compile

RUN wget https://curl.se/download/curl-7.80.0.tar.gz  && \ 
    tar -xzvf curl-7.80.0.tar.gz && cd curl-7.80.0 && \
    /bin/bash ./configure --with-ssl --with-nghttp2 --enable-ssl --enable-http2 --with-quiche \
    &&  make clean &&  make  &&  make install 