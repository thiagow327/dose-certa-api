from datetime import time
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class RemedioSchema(BaseModel):
    """Dados necessários para cadastrar um remédio."""
    nome: str = Field(..., min_length=1, max_length=100)
    dosagem: float = Field(..., gt=0)
    unidade: str = Field(..., min_length=1, max_length=30)
    frequencia_horas: int = Field(..., gt=0)
    horario_inicio: str
    observacoes: Optional[str] = None

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value: str) -> str:
        return value.strip()

    @field_validator("horario_inicio")
    @classmethod
    def validar_horario_inicio(cls, value: str) -> str:
        try:
            hora, minuto = value.split(":")
            time(hour=int(hora), minute=int(minuto))
        except Exception as exc:
            raise ValueError("horario_inicio deve estar no formato HH:MM") from exc
        return value


class RemedioBuscaSchema(BaseModel):
    """Busca um remédio pelo id."""
    id: int


class RemedioDelSchema(BaseModel):
    """Resposta após deletar um remédio."""
    message: str
    id: int


class RemedioViewSchema(BaseModel):
    """Como um remédio é retornado pela API."""
    id: int
    nome: str
    dosagem: float
    unidade: str
    frequencia_horas: int
    horario_inicio: str
    observacoes: Optional[str] = None
    ativo: bool


class ListagemRemediosSchema(BaseModel):
    """Lista de remédios."""
    remedios: List[RemedioViewSchema]


def apresenta_remedio(remedio):
    """Retorna um remédio no formato definido por RemedioViewSchema."""
    return {
        "id": remedio.id,
        "nome": remedio.nome,
        "dosagem": remedio.dosagem,
        "unidade": remedio.unidade,
        "frequencia_horas": remedio.frequencia_horas,
        "horario_inicio": remedio.horario_inicio,
        "observacoes": remedio.observacoes,
        "ativo": remedio.ativo
    }


def apresenta_remedios(remedios):
    """Retorna uma lista de remédios."""
    return {"remedios": [apresenta_remedio(r) for r in remedios]}