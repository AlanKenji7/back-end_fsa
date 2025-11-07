import os
import logging
from dotenv import load_dotenv

# 💡 MELHOR PRÁTICA: Carrega variáveis de ambiente de um arquivo .env 
# (Útil para desenvolvimento local. Em produção, o Render cuida disso)
load_dotenv() 

# ----------------------------------------------------------------------
# 🔑 Classe Base: Configurações Compartilhadas e Seguras
# ----------------------------------------------------------------------
class Config:
    """Configuração Base Comum a Todos os Ambientes."""
    
    # Busca a chave secreta; essencial para segurança do Flask (sessões, tokens, etc.)
    # ATENÇÃO: Nunca use o valor 'default' em produção.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mude_esta_chave_secreta_em_producao!'
    
    # Desabilita o rastreamento de modificações para evitar overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de Email (Padrão Gmail)
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
    
    # 🚨 PONTO CRÍTICO: Não define valor default para credenciais!
    # Se a V.E. não existir no Render, será 'None', forçando a checagem no email_utils.py.
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Remetente padrão: usa o MAIL_USERNAME como padrão, ou um fallback
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_USERNAME') or 'sistema-coep@fsa.com' 

    @staticmethod
    def init_app(app):
        """Função estática para inicialização (usado em Application Factory)."""
        pass

# ----------------------------------------------------------------------
# ⚙️ Configuração de Desenvolvimento
# ----------------------------------------------------------------------
class DevelopmentConfig(Config):
    """Configurações para Ambiente de Desenvolvimento Local."""
    DEBUG = True
    LOGGING_LEVEL = logging.DEBUG
    
    # Configuração de Banco de Dados SQLite local
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_dir = os.path.join(basedir, 'instance')
    if not os.path.exists(instance_dir):
        os.makedirs(instance_dir)
    db_path = os.path.join(instance_dir, 'fsa_teste.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or f'sqlite:///{db_path}'
    
    # Se o email falhar no dev, não vai parar a aplicação
    MAIL_FAIL_SILENTLY = True 


# ----------------------------------------------------------------------
# 🚀 Configuração de Produção
# ----------------------------------------------------------------------
class ProductionConfig(Config):
    """Configurações para Ambiente de Produção (ex: Render, PythonAnywhere)."""
    DEBUG = False
    LOGGING_LEVEL = logging.INFO
    
    # A URL do banco de dados DEVE vir de uma Variável de Ambiente
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Garante que o SECRET_KEY seja buscado (deve ser definido no Render)
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    
    # Em produção, queremos saber se o email falhou
    MAIL_FAIL_SILENTLY = False 

    # 🚨 Checagem de segurança em produção
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        if not app.config.get('fundacaofsaacex@gmail.com'') or not app.config.get('zdmd efek cxjc lgtj'):
            app.logger.error("❌ ERRO GRAVE: Credenciais de email não definidas em Produção!")
        if not app.config.get('DATABASE_URL'):
             app.logger.error("❌ ERRO GRAVE: DATABASE_URL não definida em Produção!")
             

# ----------------------------------------------------------------------
# 🗺️ Mapeamento de Configurações
# ----------------------------------------------------------------------
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig # Define o desenvolvimento como padrão se nada for especificado
}
