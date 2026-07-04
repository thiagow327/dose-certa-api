from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.orm import relationship
from database.db import Base

class Remedio(Base):
    __tablename__ = "remedio"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False, unique=True)
    dosagem = Column(Float, nullable=False)
    unidade = Column(String(30), nullable=False)
    frequencia_horas = Column(Integer, nullable=False)
    horario_inicio = Column(String(5), nullable=False)
    observacoes = Column(String(200), nullable=True)
    data_cadastro = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    ativo = Column(Boolean, default=True)

    doses = relationship("Dose", back_populates="remedio", cascade="all, delete-orphan")

    def __init__(self, nome, dosagem, unidade, frequencia_horas, horario_inicio, observacoes=None):
        self.nome = nome
        self.dosagem = float(dosagem)
        self.unidade = unidade
        self.frequencia_horas = frequencia_horas
        self.horario_inicio = horario_inicio
        self.observacoes = observacoes