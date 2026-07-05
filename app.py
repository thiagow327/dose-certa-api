from flask import redirect
from flask_cors import CORS
from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError

from model import Session, Remedio, Dose
from logger import logger
from schemas import *

info = Info(title="Dose Certa API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
remedio_tag = Tag(name="Remédio", description="Cadastro, listagem, edição e remoção de remédios")
dose_tag = Tag(name="Dose", description="Registro e listagem de doses tomadas")


@app.get("/", tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação."""
    return redirect("/openapi")


@app.post("/remedio", tags=[remedio_tag],
          responses={"200": RemedioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_remedio(body: RemedioSchema):
    """Cadastra um novo remédio na base de dados."""
    remedio = Remedio(
        nome=body.nome,
        dosagem=body.dosagem,
        unidade=body.unidade,
        frequencia_horas=body.frequencia_horas,
        horario_inicio=body.horario_inicio,
        observacoes=body.observacoes
    )
    logger.debug(f"Adicionando remédio: '{remedio.nome}'")
    try:
        session = Session()
        session.add(remedio)
        session.commit()
        logger.debug(f"Remédio adicionado: '{remedio.nome}'")
        return apresenta_remedio(remedio), 200

    except IntegrityError:
        error_msg = "Remédio com esse nome já cadastrado."
        logger.warning(f"Erro ao adicionar remédio '{remedio.nome}': {error_msg}")
        return {"message": error_msg}, 409

    except Exception:
        error_msg = "Não foi possível cadastrar o remédio."
        logger.warning(f"Erro ao adicionar remédio '{remedio.nome}': {error_msg}")
        return {"message": error_msg}, 400


@app.get("/remedios", tags=[remedio_tag],
         responses={"200": ListagemRemediosSchema, "404": ErrorSchema})
def get_remedios():
    """Lista todos os remédios ativos."""
    logger.debug("Buscando todos os remédios")
    session = Session()
    remedios = session.query(Remedio).filter(Remedio.ativo == True).all()

    if not remedios:
        return {"remedios": []}, 200

    logger.debug(f"{len(remedios)} remédios encontrados")
    return apresenta_remedios(remedios), 200


@app.get("/remedio", tags=[remedio_tag],
         responses={"200": RemedioViewSchema, "404": ErrorSchema})
def get_remedio(query: RemedioBuscaSchema):
    """Busca um remédio pelo id."""
    logger.debug(f"Buscando remédio id: {query.id}")
    session = Session()
    remedio = session.query(Remedio).filter(Remedio.id == query.id).first()

    if not remedio:
        error_msg = "Remédio não encontrado."
        logger.warning(f"Erro ao buscar remédio id '{query.id}': {error_msg}")
        return {"message": error_msg}, 404

    return apresenta_remedio(remedio), 200


@app.delete("/remedio", tags=[remedio_tag],
            responses={"200": RemedioDelSchema, "404": ErrorSchema})
def del_remedio(query: RemedioBuscaSchema):
    """Inativa um remédio pelo id."""
    logger.debug(f"Inativando remédio id: {query.id}")
    session = Session()
    remedio = session.query(Remedio).filter(Remedio.id == query.id).first()

    if not remedio:
        error_msg = "Remédio não encontrado."
        logger.warning(f"Erro ao inativar remédio id '{query.id}': {error_msg}")
        return {"message": error_msg}, 404

    remedio.ativo = False
    session.commit()
    logger.debug(f"Remédio id '{query.id}' inativado")
    return {"message": "Remédio removido", "id": query.id}, 200


@app.put("/remedio", tags=[remedio_tag],
         responses={"200": RemedioViewSchema, "404": ErrorSchema, "409": ErrorSchema, "400": ErrorSchema})
def update_remedio(query: RemedioBuscaSchema, body: RemedioSchema):
    """Edita os dados de um remédio existente."""
    logger.debug(f"Editando remédio id: {query.id}")
    session = Session()
    remedio = session.query(Remedio).filter(Remedio.id == query.id).first()

    if not remedio:
        error_msg = "Remédio não encontrado."
        logger.warning(f"Erro ao editar remédio id '{query.id}': {error_msg}")
        return {"message": error_msg}, 404

    remedio.nome = body.nome
    remedio.dosagem = body.dosagem
    remedio.unidade = body.unidade
    remedio.frequencia_horas = body.frequencia_horas
    remedio.horario_inicio = body.horario_inicio
    remedio.observacoes = body.observacoes

    try:
        session.commit()
        logger.debug(f"Remédio id '{query.id}' editado")
        return apresenta_remedio(remedio), 200

    except IntegrityError:
        error_msg = "Remédio com esse nome já cadastrado."
        logger.warning(f"Erro ao editar remédio id '{query.id}': {error_msg}")
        return {"message": error_msg}, 409

    except Exception:
        error_msg = "Não foi possível editar o remédio."
        logger.warning(f"Erro ao editar remédio id '{query.id}': {error_msg}")
        return {"message": error_msg}, 400


@app.post("/dose", tags=[dose_tag],
          responses={"200": DoseViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def add_dose(body: DoseSchema):
    """Registra uma dose tomada."""
    logger.debug(f"Registrando dose para remédio id: {body.remedio_id}")
    session = Session()
    remedio = session.query(Remedio).filter(Remedio.id == body.remedio_id).first()

    if not remedio:
        error_msg = "Remédio não encontrado."
        logger.warning(f"Erro ao registrar dose: {error_msg}")
        return {"message": error_msg}, 404

    try:
        dose = Dose(remedio_id=body.remedio_id, observacoes=body.observacoes)
        session.add(dose)
        session.commit()
        logger.debug(f"Dose registrada para remédio id: {body.remedio_id}")
        return apresenta_dose(dose), 200

    except Exception:
        error_msg = "Não foi possível registrar a dose."
        logger.warning(f"Erro ao registrar dose: {error_msg}")
        return {"message": error_msg}, 400


@app.get("/doses", tags=[dose_tag],
         responses={"200": ListagemDosesSchema, "404": ErrorSchema})
def get_doses(query: RemedioBuscaSchema):
    """Lista todas as doses de um remédio pelo id."""
    logger.debug(f"Buscando doses do remédio id: {query.id}")
    session = Session()
    doses = session.query(Dose).filter(Dose.remedio_id == query.id).all()

    if not doses:
        return {"doses": []}, 200

    logger.debug(f"{len(doses)} doses encontradas")
    return apresenta_doses(doses), 200


if __name__ == "__main__":
    app.run(debug=True)