from flask_mail import Message
from main import mail
from flask import current_app
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
        logger.info(f"Tentando enviar email para: {paciente_email}")
        logger.info(f"Configuração atual do servidor de email: {current_app.config['MAIL_SERVER']}:{current_app.config['MAIL_PORT']}")
        
        msg = Message(
            'Sua consulta foi confirmada!',
            sender=current_app.config['MAIL_USERNAME'],
            recipients=[paciente_email]
        )
        
        msg.body = f"""
        Olá {nome_paciente},

        Sua consulta foi confirmada com sucesso!

        Detalhes da consulta:
        Data: {data_consulta}
        Horário: {hora_consulta}
        Profissional: {profissional}

        Por favor, chegue com 15 minutos de antecedência.
        Em caso de necessidade de remarcação, entre em contato conosco.

        Atenciosamente,
        Equipe de Atendimento FSA
        """
        
        logger.info("Preparando para enviar o email...")
        mail.send(msg)
        logger.info("Email enviado com sucesso!")
        return True
    except Exception as e:
        logger.error(f"Erro ao enviar email: {str(e)}")
        logger.exception("Detalhes completos do erro:")
        return False 