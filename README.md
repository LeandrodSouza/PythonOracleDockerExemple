# Simple example of an application running Python, Flask and Oracle Client using Docker Desktop on Windows.

 ##### Make sure the root folder has all permissions.
 ##### In this example, the main path is C:\PythonOracleDockerExample
 ##### Add your file TNSNAMES.ORA in C:\PythonOracleDockerExemple\root\etc\oracle 
 ##### Now in file ConectorOracle.py at def connection() insert the values for p_IP = '' p_PORT = '' p_SID = '' p_USER = '' p_PASS = ''

## Run in this directory:
 * Docker-compose up --build

## accessing 
 * http://localhost/api
