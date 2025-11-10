import os
from flask import Flask
from db import db
from flask_migrate import Migrate
import logging
from flask_mail import Mail, Message
from dotenv import load_dotenv

# Configurar logging básico
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambienteS
load_dotenv(override=True)

app = Flask(__name__)

# Configurar logging do Flask
app.logger.setLevel(logging.DEBUG)

# Configurações do Flask-Mail
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# Verificação e logging de configuração de email
mail_username = app.config.get('MAIL_USERNAME')
mail_password = app.config.get('MAIL_PASSWORD')

if mail_username and mail_password:
    app.logger.info("=" * 60)
    app.logger.info("✅ Configurações de email detectadas")
    app.logger.info(f"✅ MAIL_USERNAME: {mail_username}")
    app.logger.info(f"✅ MAIL_SERVER: {app.config['MAIL_SERVER']}:{app.config['MAIL_PORT']}")
    app.logger.info("=" * 60)
else:
    app.logger.warning("=" * 60)
    app.logger.warning("⚠️ Configurações de email ausentes!")
    app.logger.warning("Defina MAIL_USERNAME/MAIL_PASSWORD nas variáveis de ambiente.")
    app.logger.warning("No Render: Environment Variables > Add Environment Variable")
    app.logger.warning("=" * 60)

# Inicializar o Flask-Mail
mail = Mail(app)

# Obtenha o caminho absoluto do diretório onde main.py está
basedir = os.path.abspath(os.path.dirname(__file__))

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'instance', 'fsa_teste.db')
app.secret_key = 'uma_chave_muito_secreta_e_complexa_aqui' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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