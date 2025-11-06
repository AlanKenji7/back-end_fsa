import os
from flask import Flask
from db import db
from flask_migrate import Migrate
import logging
from flask_mail import Mail
from dotenv import load_dotenv
from config import config as app_config

# Configurar logging básico
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv(override=True)

app = Flask(__name__)

# Configurar logging do Flask
app.logger.setLevel(logging.DEBUG)

# Detectar ambiente - Render usa variável RENDER_EXTERNAL_URL quando está em produção
env_name = os.getenv('FLASK_ENV', 'default')
# Se estiver no Render e não tiver FLASK_ENV definido, usar produção
if env_name == 'default' and os.getenv('RENDER_EXTERNAL_URL'):
    env_name = 'production'
    app.logger.info("🌐 Ambiente Render detectado - usando configuração de produção")
app.config.from_object(app_config.get(env_name, app_config['default']))

# Aviso se email não configurado
if not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
    app.logger.warning('=' * 60)
    app.logger.warning('⚠️ Configurações de email ausentes!')
    app.logger.warning('Defina MAIL_USERNAME/MAIL_PASSWORD nas variáveis de ambiente.')
    app.logger.warning('=' * 60)
else:
    app.logger.info('=' * 60)
    app.logger.info('✅ Configurações de email detectadas')
    app.logger.info(f'✅ MAIL_USERNAME: {app.config.get("MAIL_USERNAME")}')
    app.logger.info(f'✅ MAIL_SERVER: {app.config.get("MAIL_SERVER")}:{app.config.get("MAIL_PORT")}')
    app.logger.info('=' * 60)

# Inicializar o Flask-Mail
mail = Mail(app)

app.secret_key = app.config.get('SECRET_KEY', 'uma_chave_muito_secreta_e_complexa_aqui')

# Inicializar extensões
db.init_app(app)
migrate = Migrate(app, db)

# Criar tabelas do banco de dados se não existirem (importante para produção)
with app.app_context():
    try:
        db.create_all()
        app.logger.info("✅ Banco de dados inicializado com sucesso")
    except Exception as e:
        app.logger.error(f"❌ Erro ao inicializar banco de dados: {e}")

# Importar views DEPOIS de inicializar app e db
from views import *

if __name__ == '__main__':
    app.logger.info("Aplicação Flask iniciando em modo desenvolvimento...")
    app.run(debug=True) 