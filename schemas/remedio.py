from pydantic import BaseModel
from typing import Optional, List


class RemedioSchema(BaseModel):
    """Dados necessários para cadastrar um remédio."""
    nome: str
    dosagem: str
    unidade: str
    frequencia_horas: int
    horario_inicio: str
    observacoes: Optional[str] = None


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
    dosagem: str
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