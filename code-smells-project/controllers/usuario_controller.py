import logging
from models.usuario_model import UsuarioModel
from middlewares.error_handler import AppError

logger = logging.getLogger(__name__)

model = UsuarioModel()


def listar_usuarios():
    usuarios = model.get_all()
    return {"dados": usuarios, "sucesso": True}


def buscar_usuario(usuario_id):
    usuario = model.get_by_id(usuario_id)
    if not usuario:
        raise AppError("Usuario nao encontrado", 404)
    return {"dados": usuario, "sucesso": True}


def criar_usuario(data):
    if not data:
        raise AppError("Dados invalidos", 400)

    nome = data.get("nome", "")
    email = data.get("email", "")
    senha = data.get("senha", "")

    if not nome or not email or not senha:
        raise AppError("Nome, email e senha sao obrigatorios", 400)

    usuario_id = model.create(nome, email, senha)
    logger.info("Usuario criado: %s", email)
    return {"dados": {"id": usuario_id}, "sucesso": True}


def login(data):
    if not data:
        raise AppError("Dados invalidos", 400)

    email = data.get("email", "")
    senha = data.get("senha", "")

    if not email or not senha:
        raise AppError("Email e senha sao obrigatorios", 400)

    usuario = model.authenticate(email, senha)
    if usuario:
        logger.info("Login bem-sucedido: %s", email)
        return {"dados": usuario, "sucesso": True, "mensagem": "Login OK"}

    logger.info("Login falhou: %s", email)
    raise AppError("Email ou senha invalidos", 401)
