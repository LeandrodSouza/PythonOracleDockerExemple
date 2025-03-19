# 🚀 API Conector Oracle

Uma API moderna, segura e eficiente para conexão e interação com bancos de dados Oracle, completamente containerizada em Docker para facilitar implantação e escalabilidade.

## 📋 Índice
- [Características](#características)
- [Requisitos](#requisitos)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Configuração](#configuração)
- [Execução](#execução)
- [Endpoints da API](#endpoints-da-api)
- [Documentação da API](#documentação-da-api)
- [Exemplos de Uso](#exemplos-de-uso)
- [Segurança](#segurança)
- [Desenvolvimento Local](#desenvolvimento-local)
- [Solução de Problemas](#solução-de-problemas)
- [Colaboração](#colaboração)
- [Licença](#licença)
- [Versão em Inglês](#versão-em-inglês)

## ✨ Características

- ✅ API REST completa para interação com bancos de dados Oracle
- ✅ Containerização com Docker e Docker Compose para fácil implantação
- ✅ Segurança reforçada com variáveis de ambiente para credenciais
- ✅ Gerenciamento eficiente de conexões usando context managers
- ✅ Proteção contra ataques com rate limiting configurável
- ✅ Sistema de logs detalhados para monitoramento e auditoria
- ✅ Tratamento robusto de erros e exceções
- ✅ Códigos de status HTTP padronizados e respostas consistentes
- ✅ Documentação interativa da API com Swagger
- ✅ Execução em modo de usuário não-privilegiado para segurança adicional
- ✅ Suporte a consultas parametrizadas para evitar SQL Injection
- ✅ Documentação abrangente e exemplos de uso

## 📦 Requisitos

- Docker e Docker Compose
- Oracle Instant Client 12.1+ (incluído na imagem Docker)
- Acesso a um banco de dados Oracle

## 🏗️ Estrutura do Projeto

```
.
├── api/                      # Pacote principal da API
│   ├── ConectorOracle.py     # Implementação da conexão Oracle
│   ├── config.py             # Configurações e carregamento de variáveis
│   └── swagger.py            # Configuração do Swagger para documentação
├── root/                     # Arquivos que serão copiados para o container
│   └── etc/oracle/           # Local para adicionar o TNSNAMES.ORA
├── Dockerfile                # Configuração do container
├── docker-compose.yml        # Configuração da orquestração de containers
├── app.py                    # Ponto de entrada da aplicação Flask
├── .env.example              # Exemplo de variáveis de ambiente
├── requirements.txt          # Dependências Python
└── oracle-instantclient*.rpm # Arquivos do Oracle Instant Client
```

## ⚙️ Configuração

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/LeandrodSouza/PythonOracleDockerExemple.git
   cd oracle-connector-api
   ```

2. **Configure o ambiente:**
   ```bash
   cp .env.example .env
   ```

3. **Edite o arquivo `.env` com suas credenciais Oracle:**
   ```
   ORACLE_HOST=seu_host_oracle
   ORACLE_PORT=1521
   ORACLE_SID=seu_sid
   ORACLE_USER=seu_usuario
   ORACLE_PASSWORD=sua_senha
   
   APP_DEBUG=False
   APP_HOST=0.0.0.0
   APP_PORT=5000
   ```

4. **Configure seu arquivo TNSNAMES.ORA (opcional):**
   - Adicione seu arquivo TNSNAMES.ORA no diretório `root/etc/oracle/`
   - Isso é necessário apenas se você estiver usando conexões via TNS Names

## 🚀 Execução

### Usando Docker Compose (Recomendado)

Para iniciar a aplicação em modo produção:

```bash
docker-compose up -d
```

Para iniciar com reconstrução da imagem (após alterações):

```bash
docker-compose up -d --build
```

Para visualizar os logs do container:

```bash
docker-compose logs -f
```

### Verificação

A API estará disponível em:
- 🌐 `http://localhost:5000`
- 📚 Documentação: `http://localhost:5000/api/docs/swagger`

Para verificar se a API está funcionando corretamente:
```bash
curl http://localhost:5000/
```

Resposta esperada:
```json
{
  "status": "success", 
  "message": "API Oracle Connector 🔥"
}
```

## 🔌 Endpoints da API

### Rotas Principais

| Endpoint | Método | Descrição | Rate Limit | Códigos de Status |
|----------|--------|-----------|------------|-------------------|
| `/` | GET | Verifica se a API está funcionando | - | 200 |
| `/api/connection` | GET | Testa a conexão com o banco de dados Oracle | 10/min | 200, 503 |
| `/api/query` | POST | Executa consultas SQL no banco de dados | 30/min | 200, 400, 503 |
| `/api/docs` | GET | Redireciona para a documentação Swagger | - | 302 |
| `/api/docs/swagger` | GET | Interface Swagger para documentação interativa | - | 200 |

## 📚 Documentação da API

A API inclui documentação interativa usando Swagger UI, que permite explorar e testar todos os endpoints diretamente pelo navegador.

Para acessar a documentação:
1. Inicie a aplicação
2. Acesse `http://localhost:5000/api/docs/swagger` em seu navegador

A documentação Swagger fornece:
- Descrição detalhada de cada endpoint
- Parâmetros esperados e seus formatos
- Exemplos de requisições e respostas
- Códigos de status possíveis
- Interface para testar os endpoints diretamente

### Formato de Respostas

Todas as respostas seguem um formato padronizado:

#### Respostas de Sucesso
```json
{
  "status": "success",
  "message": "Mensagem informativa (opcional)",
  "data": { ... } // Dados da resposta (opcional)
}
```

#### Respostas de Erro
```json
{
  "status": "error",
  "error": {
    "code": "CÓDIGO_DO_ERRO",
    "message": "Descrição geral do erro",
    "details": "Detalhes específicos do erro (opcional)"
  }
}
```

### Códigos de Erro

| Código | Descrição | Status HTTP |
|--------|-----------|-------------|
| `BAD_REQUEST` | Dados inválidos ou incompletos | 400 |
| `NOT_FOUND` | Recurso não encontrado | 404 |
| `UNAUTHORIZED` | Não autorizado | 401 |
| `FORBIDDEN` | Acesso proibido | 403 |
| `INTERNAL_SERVER_ERROR` | Erro interno do servidor | 500 |
| `DB_CONNECTION_ERROR` | Erro de conexão com o banco de dados | 503 |

## 📝 Exemplos de Uso

### Testando a Conexão com o Banco de Dados

```bash
curl http://localhost:5000/api/connection
```

### Executando uma Consulta

```bash
curl -X POST \
  http://localhost:5000/api/query \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "SELECT * FROM funcionarios WHERE departamento = :dept",
    "params": {
        "dept": "TI"
    }
  }'
```

### Executando um INSERT

```bash
curl -X POST \
  http://localhost:5000/api/query \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "INSERT INTO logs (mensagem, data) VALUES (:msg, SYSDATE)",
    "params": {
        "msg": "Teste de inserção via API"
    }
  }'
```

## 🔒 Segurança

### Medidas Implementadas

- **Variáveis de Ambiente**: Todas as credenciais são armazenadas em variáveis de ambiente
- **Consultas Parametrizadas**: Prevenção contra SQL Injection
- **Rate Limiting**: Proteção contra ataques de força bruta
- **Usuário Não-Privilegiado**: A aplicação roda como usuário não-root no Docker
- **Logging**: Registros detalhados para auditoria e rastreabilidade
- **Multi-Stage Build**: Imagem Docker minimizada com apenas o necessário para produção
- **Dependências Fixadas**: Versões específicas para evitar vulnerabilidades
- **CORS Configurado**: Proteção contra ataques de cross-origin
- **Respostas Padronizadas**: Evita vazamento de informações sensíveis

## 💻 Desenvolvimento Local

### Requisitos

- Python 3.9+
- Oracle Instant Client 12.1+

### Configuração do Ambiente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/oracle-connector-api.git
cd oracle-connector-api

# Crie e ative um ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows use: venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas credenciais

# Execute a aplicação
python app.py
```

## 🔧 Solução de Problemas

### Problemas Comuns

1. **Erro de Conexão com o Oracle**
   - Verifique se as credenciais no arquivo `.env` estão corretas
   - Confirme se o banco de dados Oracle está acessível a partir do container
   - Verifique logs com `docker-compose logs -f`

2. **Problemas com o Instant Client**
   - Os arquivos RPM do Oracle Instant Client devem estar na raiz do projeto
   - Verifique se os volumes no docker-compose.yml estão configurados corretamente

3. **Permissões Insuficientes**
   - Certifique-se de que a pasta raiz tem permissões adequadas
   - No Windows, pode ser necessário conceder permissões adicionais para o Docker

4. **Erro na Documentação Swagger**
   - Verifique se as dependências `flasgger` e `apispec` estão instaladas
   - Reinicie o container após alterações em arquivos de configuração

## 👥 Colaboração

Contribuições são bem-vindas! Por favor, sinta-se à vontade para submeter pull requests ou abrir issues para melhorar este projeto.

1. Faça um fork do projeto
2. Crie sua branch de feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🌐 Versão em Inglês

[English-EN-US version](README-en-us.md)


