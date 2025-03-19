from flask import Flask
from flasgger import Swagger

def setup_swagger(app: Flask):
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/api/docs/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/api/docs/static",
        "swagger_ui": True,
        "specs_route": "/api/docs/swagger"
    }
    
    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "API Conector Oracle",
            "description": "API para interação com bancos de dados Oracle",
            "version": "1.0.0",
            "contact": {
                "email": "contato@exemplo.com"
            }
        },
        "basePath": "/",
        "schemes": [
            "http",
            "https"
        ],
        "securityDefinitions": {
            "Bearer": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Token de autenticação JWT no formato: Bearer {token}"
            }
        },
        "tags": [
            {
                "name": "status",
                "description": "Endpoints para verificação de status"
            },
            {
                "name": "oracle",
                "description": "Operações com o banco de dados Oracle"
            }
        ],
        "definitions": {
            "SuccessResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "success"
                    },
                    "message": {
                        "type": "string",
                        "example": "Operação realizada com sucesso"
                    },
                    "data": {
                        "type": "object"
                    }
                }
            },
            "ErrorResponse": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "example": "error"
                    },
                    "error": {
                        "type": "object",
                        "properties": {
                            "code": {
                                "type": "string",
                                "example": "BAD_REQUEST"
                            },
                            "message": {
                                "type": "string",
                                "example": "Dados inválidos ou incompletos"
                            },
                            "details": {
                                "type": "string",
                                "example": "Campo 'query' é obrigatório"
                            }
                        }
                    }
                }
            },
            "QueryRequest": {
                "type": "object",
                "required": ["query"],
                "properties": {
                    "query": {
                        "type": "string",
                        "example": "SELECT * FROM funcionarios WHERE departamento = :dept"
                    },
                    "params": {
                        "type": "object",
                        "example": {
                            "dept": "TI"
                        }
                    }
                }
            }
        }
    }
    
    return Swagger(app, config=swagger_config, template=swagger_template) 