from database import db
from datetime import datetime

class Remedio(db.Model):
    __tablename__ = 'remedios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    dosagem = db.Column(db.String(50), nullable=False)
    unidade = db.Column(db.String(20), nullable=False)
    frequencia_horas = db.Column(db.Integer, nullable=False)
    horario_inicio = db.Column(db.String(5), nullable=False)
    observacoes = db.Column(db.String(255), nullable=True)
    data_cadastro = db.Column(db.DateTime, default=datetime.now(datetime.timezone.utc))
    ativo = db.Column(db.Boolean, default=True)

    doses = db.relationship('Dose', back_populates='remedio', cascade='all, delete-orphan')
    
    def __init__(self, nome, dosagem, unidade, frequencia_horas, horario_inicio, observacoes=None):
        self.nome = nome
        self.dosagem = dosagem
        self.unidade = unidade
        self.frequencia_horas = frequencia_horas
        self.horario_inicio = horario_inicio
        self.observacoes = observacoes  
        