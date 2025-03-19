import cx_Oracle
import logging
from contextlib import contextmanager
from .config import ORACLE_CONFIG


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('oracle_connector')

class DatabaseError(Exception):
    """Exceção personalizada para erros de banco de dados"""
    def __init__(self, code, message):
        self.code = code
        self.message = message
        super().__init__(f"Erro de banco de dados: {code} - {message}")

@contextmanager
def get_connection():
    """
    Gerenciador de contexto para conexões Oracle.
    Garante que conexões sejam fechadas corretamente.
    """
    connection = None
    try:
        
        dsn = cx_Oracle.makedsn(
            ORACLE_CONFIG['host'], 
            ORACLE_CONFIG['port'], 
            sid=ORACLE_CONFIG['sid']
        )
        
        
        connection = cx_Oracle.connect(
            user=ORACLE_CONFIG['user'], 
            password=ORACLE_CONFIG['password'], 
            dsn=dsn
        )
        
        logger.info("Conexão com o banco de dados estabelecida com sucesso")
        yield connection
    
    except cx_Oracle.DatabaseError as e:
       
        error = e.args[0]
        if hasattr(error, 'message'):
            code, mesg = error.message[:-1].split(': ', 1)
            logger.error(f"Erro de conexão: {code} - {mesg}")
            raise DatabaseError(code, mesg)
        else:
            logger.error(f"Erro de conexão não especificado: {str(e)}")
            raise DatabaseError("UNKNOWN", str(e))
    
    finally:
        
        if connection:
            connection.close()
            logger.info("Conexão com o banco de dados fechada")

def test_connection():
    """
    Testa a conexão com o banco de dados Oracle.
    
    Returns:
        dict: Resultado do teste com status e mensagem
    """
    try:
        with get_connection() as _:
            return {'status': 'success', 'message': 'Conexão estabelecida com sucesso 🔥'}
    
    except DatabaseError as e:
        return {'status': 'error', 'message': f'🛠️ {e.code} | {e.message}'}
    
    except Exception as e:
        logger.error(f"Erro inesperado: {str(e)}")
        return {'status': 'error', 'message': f'Erro inesperado: {str(e)}'}

def execute_query(query, params=None):
    """
    Executa uma consulta SQL e retorna os resultados.
    
    Args:
        query (str): Consulta SQL a ser executada
        params (dict, optional): Parâmetros para a consulta
        
    Returns:
        list: Lista de dicionários com os resultados da consulta
    """
    try:
        with get_connection() as connection:
            cursor = connection.cursor()
            
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            
            if cursor.description:
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            
            
            connection.commit()
            return {'status': 'success', 'rows_affected': cursor.rowcount}
    
    except (DatabaseError, Exception) as e:
        logger.error(f"Erro ao executar consulta: {str(e)}")
        return {'status': 'error', 'message': str(e)}


def connection():
    """
    Função mantida para compatibilidade com o código existente.
    """
    result = test_connection()
    if result['status'] == 'success':
        return result['message']
    else:
        return result['message']
