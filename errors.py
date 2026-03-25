import logging

# Configuração de log
logging.basicConfig(
    filename="app_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Exceções personalizadas
class DataValidationError(Exception):
    """Erro de validação de dados (ex.: valores inválidos)."""
    pass

class FileProcessingError(Exception):
    """Erro ao ler ou processar arquivos (ex.: CSV, TXT)."""
    pass

class DatabaseConnectionError(Exception):
    """Erro de conexão com banco de dados."""
    pass

class BusinessLogicError(Exception):
    """Erro na lógica de negócio (ex.: cálculo incorreto)."""
    pass

# Função utilitária para logar erros
def log_error(error: Exception):
    logging.error(str(error))
