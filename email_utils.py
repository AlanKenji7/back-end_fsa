from flask_mail import Message
from main import mail
from flask import current_app
from main import mail, app
import logging

logger = logging.getLogger(__name__)

def enviar_email_confirmacao_consulta(paciente_email, nome_paciente, data_consulta, hora_consulta, profissional):
    """
    Envia um email de confirmação de consulta para o paciente
    
    Args:
        paciente_email (str): Email do paciente
        nome_paciente (str): Nome do paciente
        data_consulta (str): Data da consulta
        hora_consulta (str): Hora da consulta
        profissional (str): Nome do profissional
    """
    try:
        # Verificar se o email é válido
        if not paciente_email or '@' not in paciente_email:
            logger.warning(f"Email inválido: {paciente_email}")
            return False

        # Verificar configurações
        username = app.config.get('MAIL_USERNAME')
        password = app.config.get('MAIL_PASSWORD')
        
        if not username or not password:
            logger.warning("Credenciais de email não configuradas")
            return True

        logger.info(f"Tentando enviar email para: {paciente_email}")
        logger.info(f"Configuração atual do servidor de email: {current_app.config['MAIL_SERVER']}:{current_app.config['MAIL_PORT']}")
        logger.info(f"Usando servidor: {app.config.get('MAIL_SERVER')}:{app.config.get('MAIL_PORT')}")

        # Criar mensagem
        msg = Message(
            'Sua consulta foi confirmada!',
            sender=current_app.config['MAIL_USERNAME'],
            subject='Consulta Confirmada - FSA',
            sender=username,
            recipients=[paciente_email]
        )

        # Corpo do email
        msg.body = f"""
        Olá {nome_paciente},
Olá {nome_paciente},

        Sua consulta foi confirmada com sucesso!
Sua consulta foi confirmada!

        Detalhes da consulta:
        Data: {data_consulta}
        Horário: {hora_consulta}
        Profissional: {profissional}
Data: {data_consulta}
Horário: {hora_consulta}
Profissional: {profissional}

        Por favor, chegue com 15 minutos de antecedência.
        Em caso de necessidade de remarcação, entre em contato conosco.
Chegue com 15 minutos de antecedência.

        Atenciosamente,
        Equipe de Atendimento FSA
Equipe FSA
        """

        logger.info("Preparando para enviar o email...")
        # Enviar email
        mail.send(msg)
        logger.info("Email enviado com sucesso!")
        logger.info(f"✅ Email enviado com sucesso para {paciente_email}")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao enviar email: {str(e)}")
        logger.error(f"Detalhes do erro: {type(e).__name__}")
        return False

def configurar_email_simples():
    """
    Configuração simples do email - apenas para teste
    """
    try:
        # Configurações básicas para Gmail
        app.config['MAIL_SERVER'] = 'smtp.gmail.com'
        app.config['MAIL_PORT'] = 587
        app.config['MAIL_USE_TLS'] = True
        app.config['MAIL_USERNAME'] = 'fundacaofsaacex@gmail.com'  # Substitua pelo seu email
        app.config['MAIL_PASSWORD'] = 'zdmd efek cxjc lgtj'     # Substitua pela sua senha de app
        
        logger.info("Configuração de email carregada")
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar email: {str(e)}")
        logger.exception("Detalhes completos do erro:")
        logger.error(f"Erro na configuração: {e}")
        return False 
