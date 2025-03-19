from flask import Flask, jsonify, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from api.ConectorOracle import connection, test_connection, execute_query
from api.config import APP_CONFIG
from flask_cors import CORS
from http import HTTPStatus
from flasgger import swag_from
from api.swagger import setup_swagger

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('app')

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Configuração do Swagger
swagger = setup_swagger(app)

# Adiciona rate limiting para evitar ataques de força bruta
limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Códigos de erro padronizados
ERRORS = {
    'BAD_REQUEST': {
        'code': 'BAD_REQUEST',
        'message': 'Dados inválidos ou incompletos',
        'status_code': HTTPStatus.BAD_REQUEST
    },
    'NOT_FOUND': {
        'code': 'NOT_FOUND',
        'message': 'Recurso não encontrado',
        'status_code': HTTPStatus.NOT_FOUND
    },
    'UNAUTHORIZED': {
        'code': 'UNAUTHORIZED',
        'message': 'Não autorizado',
        'status_code': HTTPStatus.UNAUTHORIZED
    },
    'FORBIDDEN': {
        'code': 'FORBIDDEN',
        'message': 'Acesso proibido', 
        'status_code': HTTPStatus.FORBIDDEN
    },
    'INTERNAL_SERVER_ERROR': {
        'code': 'INTERNAL_SERVER_ERROR',
        'message': 'Erro interno do servidor',
        'status_code': HTTPStatus.INTERNAL_SERVER_ERROR
    },
    'DB_CONNECTION_ERROR': {
        'code': 'DB_CONNECTION_ERROR',
        'message': 'Erro de conexão com o banco de dados',
        'status_code': HTTPStatus.SERVICE_UNAVAILABLE
    }
}

def error_response(error_type, details=None):
    """Gera uma resposta de erro padronizada"""
    error = ERRORS.get(error_type, ERRORS['INTERNAL_SERVER_ERROR'])
    response = {
        'status': 'error',
        'error': {
            'code': error['code'],
            'message': error['message']
        }
    }
    
    if details:
        response['error']['details'] = details
    
    return jsonify(response), error['status_code']

def success_response(data=None, message=None):
    """Gera uma resposta de sucesso padronizada"""
    response = {
        'status': 'success'
    }
    
    if message:
        response['message'] = message
    
    if data:
        response['data'] = data
    
    return jsonify(response)

@app.route('/')
@swag_from({
    'tags': ['status'],
    'summary': 'Endpoint para verificar status da API',
    'responses': {
        '200': {
            'description': 'API funcionando corretamente',
            'schema': {
                '$ref': '#/definitions/SuccessResponse'
            }
        }
    }
})
def home():
    return success_response(message="API Oracle Connector 🔥")

@app.route('/api/connection')
@limiter.limit("10 per minute")
@swag_from({
    'tags': ['oracle'],
    'summary': 'Testa a conexão com o banco de dados Oracle',
    'responses': {
        '200': {
            'description': 'Conexão testada com sucesso',
            'schema': {
                '$ref': '#/definitions/SuccessResponse'
            }
        },
        '503': {
            'description': 'Erro de conexão com o banco de dados',
            'schema': {
                '$ref': '#/definitions/ErrorResponse'
            }
        }
    }
})
def api_connection():
    result = test_connection()
    
    if result['status'] == 'error':
        error_details = result['message']
        return error_response('DB_CONNECTION_ERROR', details=error_details)
    
    return success_response(message=result['message'])

@app.route('/api/query', methods=['POST'])
@limiter.limit("30 per minute")
@swag_from({
    'tags': ['oracle'],
    'summary': 'Executa consultas SQL no banco de dados Oracle',
    'parameters': [
        {
            'name': 'request_body',
            'in': 'body',
            'required': True,
            'schema': {
                '$ref': '#/definitions/QueryRequest'
            }
        }
    ],
    'responses': {
        '200': {
            'description': 'Consulta executada com sucesso',
            'schema': {
                '$ref': '#/definitions/SuccessResponse'
            }
        },
        '400': {
            'description': 'Dados da requisição inválidos',
            'schema': {
                '$ref': '#/definitions/ErrorResponse'
            }
        },
        '503': {
            'description': 'Erro ao executar consulta no banco de dados',
            'schema': {
                '$ref': '#/definitions/ErrorResponse'
            }
        }
    }
})
def api_query():
    data = request.get_json()
    
    if not data:
        return error_response('BAD_REQUEST', 'Corpo da requisição vazio ou mal formatado')
    
    if 'query' not in data:
        return error_response('BAD_REQUEST', 'É necessário fornecer uma consulta SQL')
    
    # Executa a consulta com os parâmetros fornecidos (se houver)
    result = execute_query(data['query'], data.get('params'))
    
    if isinstance(result, dict) and result.get('status') == 'error':
        return error_response('DB_CONNECTION_ERROR', details=result.get('message'))
    
    return success_response(data=result)

@app.errorhandler(404)
def not_found(e):
    return error_response('NOT_FOUND')

@app.errorhandler(429)
def rate_limit_exceeded(e):
    return error_response('FORBIDDEN', 'Limite de requisições excedido. Tente novamente mais tarde.')

@app.errorhandler(500)
def server_error(e):
    logger.error(f"Erro interno do servidor: {str(e)}")
    return error_response('INTERNAL_SERVER_ERROR')

# Rota para documentação da API (redirecionamento para Swagger UI)
@app.route('/api/docs')
def api_docs():
    from flask import redirect
    return redirect('/api/docs/swagger')

if __name__ == '__main__':
    # Para compatibilidade com código existente
    from api import *
    
    # Usa configurações do arquivo de configuração
    app.run(
        host=APP_CONFIG['host'],
        port=APP_CONFIG['port'],
        debug=APP_CONFIG['debug']
    )
