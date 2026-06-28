from database import db
from datetime import datetime, timezone

class Dose(db.Model):
    __tablename__ = 'dose'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    remedio_id = db.Column(db.Integer, db.ForeignKey('remedio.id'), nullable=False)
    data_hora = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    observacoes = db.Column(db.String(255), nullable=True)
    
    remedio = db.relationship('Remedio', back_populates='dose')
    
    def __init__(self, remedio_id, observacoes=None):
        self.remedio_id = remedio_id
        self.observacoes = observacoes
    