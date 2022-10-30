[English version en-us](https://github.com/LeandrodSouza/PythonOracleDockerExemple/blob/main/README-en-us.md).

# Exemplo simples de uma imagem  Docker Desktop no Windows usando Python, Flask e Oracle Client.
* certifique-se de que a pasta raiz todas as permissões.
* Neste exemplo, o caminho principal é C:\PythonOracleDockerExample
* adicione seu arquivo TNSNAMES.ORA em C:\PythonOracleDockerExemple\root\etc\oracle 
* Agora no arquivo ConnectorOracle.py na função connection() insira os valores para p_IP = '' p_PORT = '' p_SID = '' p_USER = '' p_PASS = ''
## No diretório C:\PythonOracleDockerExample executar:
 * Docker-compose up --build
## acesso
 * http://localhost/api


