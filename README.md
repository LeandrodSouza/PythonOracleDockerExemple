Versão em ingles disponível [aqui](https://github.com/LeandrodSouza/PythonOracleDockerExemple/blob/main/README-en-us.md).

<<<<<<< HEAD
# Exemplo simples de um aplicativo executando Python, Flask e Oracle Client usando o Docker Desktop no Windows.
* Certifique-se de que a pasta raiz tenha todas as permissões.
* Neste exemplo, o caminho principal é C:\PythonOracleDockerExample
* Adicione em C:\PythonOracleDockerExemple\root\etc\oracle seu TNSNAMES.ORA
* Agora no arquivo ConectorOracle.py em def connection() insira os valores para p_IP = '' p_PORT = '' p_SID = '' p_USER = '' p_PASS = ''
## Execute neste diretório:
 * Docker-compose up --build
## acesso
 * http://localhost/api
=======
### First, install docker
 * https://docs.docker.com/desktop/windows/wsl/



 ##### Make sure the root folder has all permissions.
 ##### In this example, the main path is C:\PythonOracleDockerExample
 ##### Add your file TNSNAMES.ORA in C:\PythonOracleDockerExemple\root\etc\oracle 
 ##### Now in file ConectorOracle.py at def connection() insert the values for p_IP = '' p_PORT = '' p_SID = '' p_USER = '' p_PASS = ''

#### Run in this directory:
 * Docker-compose up --build

#### accessing 
 * http://localhost/api
>>>>>>> 3e24eda1e040c409ec0ce0a352d57fb73f1193a9
