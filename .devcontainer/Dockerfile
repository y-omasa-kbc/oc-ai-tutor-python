FROM mcr.microsoft.com/devcontainers/python:1-3.11

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      git \
 && rm -rf /var/lib/apt/lists/*

RUN groupadd -g 1000 vscode || true \
 && useradd -m -u 1000 -g vscode -s /bin/bash vscode || true

WORKDIR /workspace

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt \
 && rm /tmp/requirements.txt

USER vscode
