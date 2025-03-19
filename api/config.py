import os
from dotenv import load_dotenv


load_dotenv()


ORACLE_CONFIG = {
    'host': os.getenv('ORACLE_HOST', ''),
    'port': os.getenv('ORACLE_PORT', ''),
    'sid': os.getenv('ORACLE_SID', ''),
    'user': os.getenv('ORACLE_USER', ''),
    'password': os.getenv('ORACLE_PASSWORD', '')
}


APP_CONFIG = {
    'debug': os.getenv('APP_DEBUG', 'False').lower() in ('true', '1', 't'),
    'host': os.getenv('APP_HOST', '0.0.0.0'),
    'port': int(os.getenv('APP_PORT', '5000'))
} 