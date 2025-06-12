# Dockerfile (dans ./waf)
FROM nginx:1.25.3

# Installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    git build-essential libtool libpcre3 libpcre3-dev zlib1g zlib1g-dev \
    libssl-dev curl ca-certificates libxml2 libxml2-dev libyajl-dev \
    pkgconf libgeoip-dev automake autoconf wget

# Cloner et compiler ModSecurity v3
WORKDIR /opt
RUN git clone --depth 1 -b v3.0.9 https://github.com/SpiderLabs/ModSecurity && \
    cd ModSecurity && \
    git submodule init && git submodule update && \
    ./build.sh && ./configure && make && make install

# Cloner et compiler le module nginx
RUN git clone --depth 1 https://github.com/SpiderLabs/ModSecurity-nginx.git

# Télécharger les sources de nginx
RUN wget http://nginx.org/download/nginx-1.25.3.tar.gz && \
    tar zxvf nginx-1.25.3.tar.gz

# Compiler le module en tant que module dynamique
RUN cd nginx-1.25.3 && \
    ./configure --with-compat --add-dynamic-module=../ModSecurity-nginx && \
    make modules && cp objs/ngx_http_modsecurity_module.so /etc/nginx/modules/

# Copier la config nginx + modsecurity
COPY waf.conf /etc/nginx/conf.d/waf.conf
COPY modsecurity.conf /etc/nginx/modsecurity.conf
COPY crs-setup.conf /etc/nginx/crs-setup.conf
COPY rules /etc/nginx/rules 

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
