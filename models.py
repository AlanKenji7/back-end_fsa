# models.py
from db import db
import datetime 

class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False) # Use db.Date para datas
    genero = db.Column(db.String(20), nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    numero_casa = db.Column(db.String(10), nullable=False)
    senha = db.Column(db.String(200), nullable=False) # Armazene hashes de senhas, não senhas em texto puro!

    def __repr__(self):
        return f'<Paciente {self.nome}>'
    
class Estagiario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    data_nascimento = db.Column(db.Date, nullable=False)
    RA = db.Column(db.String(10), unique=True, nullable=False) # RA geralmente é string
    cpf = db.Column(db.String(14), unique=True, nullable=False)
    # AQUI ESTÁ A CHAVE! Certifique-se de que esta linha existe e o nome é 'telefone'
    telefone_aluno = db.Column(db.String(20), nullable=False) 
    emailfsa = db.Column(db.String(100), unique=True, nullable=False)
    curso_periodo = db.Column(db.String(50), nullable=False)
    senha = db.Column(db.String(128), nullable=False) # Armazenar a senha hash

    def __repr__(self):
        return f'<Estagiario {self.nome} - RA: {self.RA}>'
class Disponibilidade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estagiario_id = db.Column(db.Integer, db.ForeignKey('estagiario.id'), nullable=False)
    dia_semana = db.Column(db.String(20), nullable=False)  # Ex: "Segunda-feira", "Terça-feira"
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    estagiario = db.relationship('Estagiario', backref=db.backref('disponibilidades', lazy=True))

    def __repr__(self):
        return f'<Disponibilidade {self.estagiario.nome} - {self.dia_semana}: {self.horario_inicio}-{self.horario_fim}>'

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paciente_id = db.Column(db.Integer, db.ForeignKey('paciente.id'), nullable=False)
    estagiario_id = db.Column(db.Integer, db.ForeignKey('estagiario.id'), nullable=True) # Pode ser nulo até um estagiário aceitar
    data_solicitacao = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    data_agendamento = db.Column(db.Date, nullable=True)
    horario_agendamento = db.Column(db.Time, nullable=True)
    status = db.Column(db.String(50), nullable=False, default='solicitado') # Status: solicitado, aceito, confirmado, recusado, concluido
    
    paciente = db.relationship('Paciente', backref=db.backref('agendamentos', lazy=True))
    estagiario = db.relationship('Estagiario', backref=db.backref('agendamentos', lazy=True))

    def __repr__(self):
        return f'<Agendamento {self.id} - Paciente: {self.paciente.nome} - Status: {self.status}>'