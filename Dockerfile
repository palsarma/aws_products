FROM frolvlad/alpine-python3

RUN apk update \
    && apk add py3-lxml \
    && pip3 install requests && \
    rm -rf /var/cache/apk/*
    
WORKDIR /app
COPY . /app


ENTRYPOINT [ "python3", "aws_products.py" ]


