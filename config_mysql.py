"""
Configuração para MySQL
Use este arquivo para alternar entre SQLite e MySQL
"""

import os

# Configurações do MySQL
MYSQL_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '',  # Altere conforme sua configuração
    'database': 'fsa_teste',
    'charset': 'utf8mb4'
}

def get_database_uri():
    """
    Retorna a URI do banco de dados
    Por padrão usa MySQL, mas pode ser alterado para SQLite
    """
    # Para usar MySQL (padrão)
    mysql_uri = f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}:{MYSQL_CONFIG['port']}/{MYSQL_CONFIG['database']}?charset={MYSQL_CONFIG['charset']}"
    
    # Para usar SQLite (comentado)
    # basedir = os.path.abspath(os.path.dirname(__file__))
    # sqlite_uri = 'sqlite:///' + os.path.join(basedir, 'instance', 'fsa_teste.db')
    
    return mysql_uri

def get_database_config():
    """Retorna configurações adicionais do banco"""
    return {
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SQLALCHEMY_ENGINE_OPTIONS': {
            'pool_pre_ping': True,
            'pool_recycle': 300,
        }
    }
