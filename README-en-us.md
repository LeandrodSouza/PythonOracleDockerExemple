 [Versão em Português -PT-BR](https://github.com/LeandrodSouza/PythonOracleDockerExemple/blob/main/README.md).

# Simple example of a Docker Desktop image on Windows using Python, Flask and Oracle Client.
* root - make sure the folder has all permissions.
* In this example the main path is C:\PythonOracleDockerExample
* your TNSNAMES.ORA file in C:\PythonOracleDockerExemple\root\etc\oracle
* Now in the ConnectorOracle.py file in the connection() function enter the values ​​for p_IP = '' p_PORT = '' p_SID = '' p_USER = '' p_PASS = ''
## No directory C:\PythonOracleDockerExample run:
 * docker-compose up --build
## access
 * http://localhost/api
