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

# Carregar variáveis de ambienteS
load_dotenv(override=True)

app = Flask(__name__)

# Configurar logging do Flask
app.logger.setLevel(logging.DEBUG)

env_name = os.getenv('FLASK_ENV', 'default')
app.config.from_object(app_config.get(env_name, app_config['default']))

# Aviso se email não configurado
if not app.config.get('MAIL_USERNAME') or not app.config.get('MAIL_PASSWORD'):
    app.logger.warning('Configurações de email ausentes. Defina MAIL_USERNAME/MAIL_PASSWORD nas variáveis de ambiente.')

# Inicializar o Flask-Mail
mail = Mail(app)

app.secret_key = app.config.get('SECRET_KEY', 'uma_chave_muito_secreta_e_complexa_aqui')

# Inicializar extensões
db.init_app(app)
migrate = Migrate(app, db)

# Importar views DEPOIS de inicializar app e db
from views import *

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.logger.info("Aplicação Flask iniciando...")
    app.run(debug=True) 