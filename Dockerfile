FROM python:3.9-slim as base

# Variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ORACLE_HOME=/usr/lib/oracle/12.1/client64 \
    PATH=$PATH:/usr/lib/oracle/12.1/client64/bin \
    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/oracle/12.1/client64/lib

# Cria usuário não-privilegiado para rodar a aplicação
RUN addgroup --system app && adduser --system --group app

# Fase de construção para instalar dependências
FROM base as builder

# Instala dependências necessárias para instalar pacotes Python
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libaio1 \
    alien \
    wget \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Adiciona arquivos Oracle Instant Client
COPY oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm /tmp/
COPY oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.x86_64.rpm /tmp/
COPY oracle-instantclient12.1-devel-12.1.0.2.0-1.x86_64.rpm /tmp/

# Instala Oracle Instant Client
RUN alien -i /tmp/oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm \
    && alien -i /tmp/oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.x86_64.rpm \
    && alien -i /tmp/oracle-instantclient12.1-devel-12.1.0.2.0-1.x86_64.rpm \
    && rm -rf /tmp/*.rpm

# Configura diretórios Oracle
RUN ln -snf /usr/lib/oracle/12.1/client64 /opt/oracle \
    && mkdir -p /opt/oracle/network/admin \
    && mkdir -p /etc/oracle

# Copia arquivo TNSNAMES.ORA do projeto para o diretório Oracle
COPY root/etc/oracle/* /etc/oracle/

# Define diretório de trabalho
WORKDIR /app

# Copia apenas os arquivos necessários para instalar dependências
COPY requirements.txt .

# Instala dependências Python
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn

# Fase final com aplicação mínima
FROM base

# Copia arquivos e bibliotecas do Oracle da etapa de build
COPY --from=builder /usr/lib/oracle /usr/lib/oracle
COPY --from=builder /opt/oracle /opt/oracle
COPY --from=builder /etc/oracle /etc/oracle

# Copia a raiz personalizada, se necessário
COPY root /

# Instala apenas as dependências de runtime necessárias
RUN apt-get update && apt-get install -y --no-install-recommends \
    libaio1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Define diretório de trabalho
WORKDIR /app

# Copia os pacotes Python instalados do builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copia a aplicação
COPY . /app/

# Cria arquivo .env vazio para evitar erros
RUN touch .env

# Define usuário não-privilegiado
USER app

# Expõe porta
EXPOSE 5000

# Comando para iniciar a aplicação com Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]