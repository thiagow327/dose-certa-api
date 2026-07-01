from pydantic import BaseModel
from typing import Optional, List


class DoseSchema(BaseModel):
    """Dados necessários para registrar uma dose tomada."""
    remedio_id: int
    observacoes: Optional[str] = None


class DoseViewSchema(BaseModel):
    """Como uma dose é retornada pela API."""
    id: int
    remedio_id: int
    data_hora: str
    observacoes: Optional[str] = None


class ListagemDosesSchema(BaseModel):
    """Lista de doses."""
    doses: List[DoseViewSchema]


def apresenta_dose(dose):
    """Retorna uma dose no formato definido por DoseViewSchema."""
    return {
        "id": dose.id,
        "remedio_id": dose.remedio_id,
        "data_hora": dose.data_hora.strftime("%d/%m/%Y %H:%M"),
        "observacoes": dose.observacoes
    }


def apresenta_doses(doses):
    """Retorna uma lista de doses."""
    return {"doses": [apresenta_dose(d) for d in doses]}