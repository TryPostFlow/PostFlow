FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    DEBIAN_FRONTEND=noninteractive \
    TZ=Asia/Shanghai

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libffi-dev tzdata && \
    ln -snf /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo "${TZ}" > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip wheel "setuptools<81" && \
    pip install -r requirements.txt

EXPOSE 8000

CMD [ "postflow", "start", "-h", "0.0.0.0" ]
