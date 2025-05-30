"""
Módulo de autenticação e conexão com o banco de dados SQL Server.
"""
import pyodbc
import logging
from . import secret

# Configurando o log
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def get_connection(driver="ODBC Driver 17 for SQL Server", intent="ReadOnly"):
    """
    Estabelece conexão com o banco de dados SQL Server usando autenticação MFA.
    
    Args:
        driver (str): Driver ODBC a ser utilizado.
        intent (str): Intenção da aplicação (ReadOnly ou ReadWrite).
        
    Returns:
        pyodbc.Connection: Objeto de conexão com o banco de dados.
        
    Raises:
        Exception: Erro ao conectar ao banco de dados.
    """
    connection_string = (
        f"Driver={{{driver}}};"
        f"Server={secret.SERVIDOR};"
        f"Database={secret.DATA_BASE};"
        f"Authentication=ActiveDirectoryInteractive;"
        f"ApplicationIntent={intent};"
        "Encrypt=yes;"
        "TrustServerCertificate=no;"
    )

    try:
        logger.info("Tentando conectar ao banco de dados...")
        conn = pyodbc.connect(connection_string, timeout=10)  # Timeout de 10 segundos
        logger.info("Conexão estabelecida com sucesso.")
        return conn
    except pyodbc.Error as db_err:
        logger.error("Erro de banco de dados: %s", db_err)
        raise
    except Exception as e:
        logger.error("Erro inesperado ao conectar ao banco de dados: %s", e)
        raise
