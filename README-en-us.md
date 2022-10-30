Portuguese version available [here](https://github.com/LeandrodSouza/PythonOracleDockerExemple/blob/main/README.md).

# Simple example of an application using Python, Flask and Oracle Client or Docker Desktop on Windows.
* Make sure the root folder has all permissions.
* In this example the main path is C:\PythonOracleDockerExample
* add your TNSNAMES.ORA file in C:\PythonOracleDockerExemple\root\etc\oracle
* Now in the ConnectorOracle.py file in the connection() function enter the values ​​for p_IP = '' p_PORT = '' p_SID = '' p_USER = '' p_PASS = ''
## Run in this directory:
 * docker-compose up --build
## access
 * http://localhost/api