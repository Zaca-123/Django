
FROM python:3.12-alpine AS base
LABEL maintainer="Grupo 12 <grupo12@gmail.com>"
LABEL version="1.0"
LABEL description="cloudset"

RUN apk --no-cache add bash pango ttf-freefont py3-pip curl

FROM base AS builder
RUN apk --no-cache add \
    libpq-dev gcc musl-dev python3-dev postgresql-dev \
    py3-pillow py3-brotli py3-scipy py3-cffi \
    linux-headers autoconf automake libtool cmake \
    fortify-headers binutils libffi-dev wget openssl-dev libc-dev \
    g++ make musl-dev pkgconf libpng-dev openblas-dev build-base \
    font-noto terminus-font libffi

WORKDIR /install
COPY ./requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

FROM base
RUN mkdir /code
WORKDIR /code
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . /code
RUN ln -s /usr/share/zoneinfo/America/Cordoba /etc/localtime

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "app.wsgi"]

