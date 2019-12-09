FROM python:3.6-alpine3.7 as base
FROM base as builder

RUN mkdir /install
WORKDIR /install

# Install dependencies
RUN apk add --no-cache  \
        gcc \
        libc-dev \
        linux-headers \
        mariadb-dev

RUN pip install --upgrade pip

# Add requirements.txt
COPY requirements.txt /tmp/

RUN pip wheel --wheel-dir=/tmp/wheelhouse -r /tmp/requirements.txt
RUN pip install --prefix=/install -r /tmp/requirements.txt --no-index --find-links=/tmp/wheelhouse --no-warn-script-location

FROM base

# Install dependencies
RUN apk add --no-cache \
        bash \
        mariadb-client-libs \
        netcat-openbsd

COPY --from=builder /install /usr/local

WORKDIR /code/

CMD ["gunicorn", "affo_deeplink.main:app", "-b", ":8000", "--worker-class", "aiohttp.GunicornWebWorker", "--reload", "-"]
