Versão em ingles disponível [aqui](https://github.com/LeandrodSouza/PythonOracleDockerExemple/blob/main/README-en-us.md).

# Exemplo simples de um aplicativo executando Python, Flask e Oracle Client usando o Docker Desktop no Windows.
* Certifique-se de que a pasta raiz tenha todas as permissões.
* Neste exemplo, o caminho principal é C:\PythonOracleDockerExample
* Adicione em C:\PythonOracleDockerExemple\root\etc\oracle seu TNSNAMES.ORA
* Agora no arquivo ConectorOracle.py em def connection() insira os valores para p_IP = '' p_PORT = '' p_SID = '' p_USER = '' p_PASS = ''
## Execute neste diretório:
 * Docker-compose up --build
## acesso
 * http://localhost/api