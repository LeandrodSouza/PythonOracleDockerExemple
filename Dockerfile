FROM python:3.6
ENV PYTHONHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN pip install -r requirements.txt
ENV ORACLE_HOME=/usr/lib/oracle/12.1/client64
ENV PATH=$PATH:$ORACLE_HOME/bin
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$ORACLE_HOME/lib
ADD oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm /tmp/
ADD oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.x86_64.rpm /tmp/
ADD oracle-instantclient12.1-devel-12.1.0.2.0-1.x86_64.rpm /tmp/
# Configuração local, client Oracle e Python
RUN apt-get update \
    && apt-get -y install alien libaio1 \
    && alien -i /tmp/oracle-instantclient12.1-basic-12.1.0.2.0-1.x86_64.rpm \
    && alien -i /tmp/oracle-instantclient12.1-sqlplus-12.1.0.2.0-1.x86_64.rpm \
    && alien -i /tmp/oracle-instantclient12.1-devel-12.1.0.2.0-1.x86_64.rpm \
    && ln -snf /usr/lib/oracle/12.1/client64 /opt/oracle \
    && mkdir -p /opt/oracle/network \
    && ln -snf /etc/oracle /opt/oracle/network/admin \
    && pip install cx_oracle \
    && apt-get clean && rm -rf /var/cache/apt/* /var/lib/apt/lists/* /tmp/* /var/tmp/*
ADD root /


EXPOSE 5000

ENTRYPOINT ["python3"]
CMD ["app.py"]