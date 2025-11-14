FROM mcr.microsoft.com/devcontainers/python:3.14

USER root

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*

ENV UV_INSTALL_DIR=/usr/local/bin
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

USER vscode
WORKDIR /workspaces
