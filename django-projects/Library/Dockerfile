ARG PYTHON_VERSION_ARG=3.10.12
# Stage 1: Build Stage
FROM python:${PYTHON_VERSION_ARG}-slim-bullseye AS builder
ARG WORKDIR_ARG=/opt/web
ENV WORKDIR=${WORKDIR_ARG}
# 設置工作目錄
WORKDIR ${WORKDIR}
# 複製 Poetry 文件到容器中
COPY pyproject.toml poetry.lock ${WORKDIR}
# pip 安裝 Poetry
RUN pip install --no-cache-dir poetry
# apt 安裝相依套件
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Poetry 安裝依賴
RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction --no-ansi
# 複製專案文件到容器
COPY . ${WORKDIR}
# 使用 collectstatic 收集靜態文件
RUN chmod +x ${WORKDIR}/entrypoint.sh && \
    python manage.py collectstatic --noinput

# 啟動指令
CMD ["/bin/bash", "./entrypoint.sh"]