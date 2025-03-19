[Versão em Português -PT-BR](README.md)

# 🚀 Oracle Connector API

A modern, secure, and efficient API for connecting and interacting with Oracle databases, fully containerized in Docker for easy deployment and scalability.

## 📋 Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Execution](#execution)
- [API Endpoints](#api-endpoints)
- [API Documentation](#api-documentation)
- [Usage Examples](#usage-examples)
- [Security](#security)
- [Local Development](#local-development)
- [Troubleshooting](#troubleshooting)
- [Collaboration](#collaboration)
- [License](#license)

## ✨ Features

- ✅ Complete REST API for Oracle database interaction
- ✅ Docker and Docker Compose containerization for easy deployment
- ✅ Enhanced security with environment variables for credentials
- ✅ Efficient connection management using context managers
- ✅ Protection against attacks with configurable rate limiting
- ✅ Detailed logging system for monitoring and auditing
- ✅ Robust error and exception handling
- ✅ Standardized HTTP status codes and consistent responses
- ✅ Interactive API documentation with Swagger
- ✅ Execution in non-privileged user mode for additional security
- ✅ Support for parameterized queries to prevent SQL Injection
- ✅ Comprehensive documentation and usage examples

## 📦 Requirements

- Docker and Docker Compose
- Oracle Instant Client 12.1+ (included in the Docker image)
- Access to an Oracle database

## 🏗️ Project Structure

```
.
├── api/                      # Main API package
│   ├── ConectorOracle.py     # Oracle connection implementation
│   ├── config.py             # Settings and variable loading
│   └── swagger.py            # Swagger configuration for documentation
├── root/                     # Files to be copied to the container
│   └── etc/oracle/           # Place to add TNSNAMES.ORA
├── Dockerfile                # Container configuration
├── docker-compose.yml        # Container orchestration configuration
├── app.py                    # Flask application entry point
├── .env.example              # Example environment variables
├── requirements.txt          # Python dependencies
└── oracle-instantclient*.rpm # Oracle Instant Client files
```

## ⚙️ Configuration

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/oracle-connector-api.git
   cd oracle-connector-api
   ```

2. **Set up the environment:**
   ```bash
   cp .env.example .env
   ```

3. **Edit the `.env` file with your Oracle credentials:**
   ```
   ORACLE_HOST=your_oracle_host
   ORACLE_PORT=1521
   ORACLE_SID=your_sid
   ORACLE_USER=your_username
   ORACLE_PASSWORD=your_password
   
   APP_DEBUG=False
   APP_HOST=0.0.0.0
   APP_PORT=5000
   ```

4. **Configure your TNSNAMES.ORA file (optional):**
   - Add your TNSNAMES.ORA file to the `root/etc/oracle/` directory
   - This is only necessary if you are using TNS Names connections

## 🚀 Execution

### Using Docker Compose (Recommended)

To start the application in production mode:

```bash
docker-compose up -d
```

To start with image rebuilding (after changes):

```bash
docker-compose up -d --build
```

To view container logs:

```bash
docker-compose logs -f
```

### Verification

The API will be available at:
- 🌐 `http://localhost:5000`
- 📚 Documentation: `http://localhost:5000/api/docs/swagger`

To verify that the API is working correctly:
```bash
curl http://localhost:5000/
```

Expected response:
```json
{
  "status": "success", 
  "message": "API Oracle Connector 🔥"
}
```

## 🔌 API Endpoints

### Main Routes

| Endpoint | Method | Description | Rate Limit | Status Codes |
|----------|--------|-------------|------------|--------------|
| `/` | GET | Check if the API is working | - | 200 |
| `/api/connection` | GET | Test the connection to the Oracle database | 10/min | 200, 503 |
| `/api/query` | POST | Execute SQL queries on the database | 30/min | 200, 400, 503 |
| `/api/docs` | GET | Redirect to Swagger documentation | - | 302 |
| `/api/docs/swagger` | GET | Swagger UI for interactive documentation | - | 200 |

## 📚 API Documentation

The API includes interactive documentation using Swagger UI, which allows you to explore and test all endpoints directly through your browser.

To access the documentation:
1. Start the application
2. Visit `http://localhost:5000/api/docs/swagger` in your browser

The Swagger documentation provides:
- Detailed description of each endpoint
- Expected parameters and their formats
- Request and response examples
- Possible status codes
- Interface to test endpoints directly

### Response Format

All responses follow a standardized format:

#### Success Responses
```json
{
  "status": "success",
  "message": "Informative message (optional)",
  "data": { ... } // Response data (optional)
}
```

#### Error Responses
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "General error description",
    "details": "Specific error details (optional)"
  }
}
```

### Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `BAD_REQUEST` | Invalid or incomplete data | 400 |
| `NOT_FOUND` | Resource not found | 404 |
| `UNAUTHORIZED` | Not authorized | 401 |
| `FORBIDDEN` | Access forbidden | 403 |
| `INTERNAL_SERVER_ERROR` | Internal server error | 500 |
| `DB_CONNECTION_ERROR` | Database connection error | 503 |

## 📝 Usage Examples

### Testing Database Connection

```bash
curl http://localhost:5000/api/connection
```

### Running a Query

```bash
curl -X POST \
  http://localhost:5000/api/query \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "SELECT * FROM employees WHERE department = :dept",
    "params": {
        "dept": "IT"
    }
  }'
```

### Running an INSERT

```bash
curl -X POST \
  http://localhost:5000/api/query \
  -H 'Content-Type: application/json' \
  -d '{
    "query": "INSERT INTO logs (message, date) VALUES (:msg, SYSDATE)",
    "params": {
        "msg": "Test insertion via API"
    }
  }'
```

## 🔒 Security

### Implemented Measures

- **Environment Variables**: All credentials are stored in environment variables
- **Parameterized Queries**: Prevention against SQL Injection
- **Rate Limiting**: Protection against brute force attacks
- **Non-Privileged User**: The application runs as a non-root user in Docker
- **Logging**: Detailed records for auditing and traceability
- **Multi-Stage Build**: Minimized Docker image with only what's necessary for production
- **Pinned Dependencies**: Specific versions to avoid vulnerabilities
- **CORS Configured**: Protection against cross-origin attacks
- **Standardized Responses**: Prevents sensitive information leakage

## 💻 Local Development

### Requirements

- Python 3.9+
- Oracle Instant Client 12.1+

### Environment Setup

```bash
# Clone the repository
git clone https://github.com/your-username/oracle-connector-api.git
cd oracle-connector-api

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit the .env file with your credentials

# Run the application
python app.py
```

## 🔧 Troubleshooting

### Common Issues

1. **Oracle Connection Error**
   - Check if the credentials in the `.env` file are correct
   - Confirm that the Oracle database is accessible from the container
   - Check logs with `docker-compose logs -f`

2. **Instant Client Issues**
   - Oracle Instant Client RPM files should be in the project root
   - Verify that the volumes in docker-compose.yml are configured correctly

3. **Insufficient Permissions**
   - Make sure the root folder has adequate permissions
   - On Windows, you may need to grant additional permissions for Docker

4. **Swagger Documentation Error**
   - Verify that `flasgger` and `apispec` dependencies are installed
   - Restart the container after changes to configuration files

## 👥 Collaboration

Contributions are welcome! Please feel free to submit pull requests or open issues to improve this project.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -m 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT license - see the [LICENSE](LICENSE) file for details.
