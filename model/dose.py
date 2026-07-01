from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Dose(Base):
    __tablename__ = "dose"

    id = Column(Integer, primary_key=True, autoincrement=True)
    remedio_id = Column(Integer, ForeignKey("remedio.id"), nullable=False)
    data_hora = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    observacoes = Column(String(200), nullable=True)

    remedio = relationship("Remedio", back_populates="doses")

    def __init__(self, remedio_id, observacoes=None):
        self.remedio_id = remedio_id
        self.observacoes = observacoes