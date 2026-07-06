import logging
from models.produto_model import ProdutoModel
from middlewares.error_handler import AppError
from config.settings import VALID_CATEGORIES

logger = logging.getLogger(__name__)

model = ProdutoModel()


def validate_produto_data(data):
    if not data:
        raise AppError("Dados invalidos", 400)

    nome = data.get("nome")
    preco = data.get("preco")
    estoque = data.get("estoque")

    if not nome:
        raise AppError("Nome e obrigatorio", 400)
    if preco is None:
        raise AppError("Preco e obrigatorio", 400)
    if estoque is None:
        raise AppError("Estoque e obrigatorio", 400)
    if preco < 0:
        raise AppError("Preco nao pode ser negativo", 400)
    if estoque < 0:
        raise AppError("Estoque nao pode ser negativo", 400)
    if len(nome) < 2:
        raise AppError("Nome muito curto", 400)
    if len(nome) > 200:
        raise AppError("Nome muito longo", 400)

    categoria = data.get("categoria", "geral")
    if categoria not in VALID_CATEGORIES:
        raise AppError(f"Categoria invalida. Validas: {VALID_CATEGORIES}", 400)


def listar_produtos():
    produtos = model.get_all()
    logger.info("Listando %d produtos", len(produtos))
    return {"dados": produtos, "sucesso": True}


def buscar_produto(produto_id):
    produto = model.get_by_id(produto_id)
    if not produto:
        raise AppError("Produto nao encontrado", 404)
    return {"dados": produto, "sucesso": True}


def criar_produto(data):
    validate_produto_data(data)
    produto_id = model.create(
        data["nome"],
        data.get("descricao", ""),
        data["preco"],
        data["estoque"],
        data.get("categoria", "geral"),
    )
    logger.info("Produto criado com ID: %d", produto_id)
    return {"dados": {"id": produto_id}, "sucesso": True, "mensagem": "Produto criado"}


def atualizar_produto(produto_id, data):
    existing = model.get_by_id(produto_id)
    if not existing:
        raise AppError("Produto nao encontrado", 404)

    validate_produto_data(data)
    model.update(
        produto_id,
        data["nome"],
        data.get("descricao", ""),
        data["preco"],
        data["estoque"],
        data.get("categoria", "geral"),
    )
    return {"sucesso": True, "mensagem": "Produto atualizado"}


def deletar_produto(produto_id):
    existing = model.get_by_id(produto_id)
    if not existing:
        raise AppError("Produto nao encontrado", 404)
    model.delete(produto_id)
    logger.info("Produto %d deletado", produto_id)
    return {"sucesso": True, "mensagem": "Produto deletado"}


def buscar_produtos(termo, categoria, preco_min, preco_max):
    resultados = model.search(termo, categoria, preco_min, preco_max)
    return {"dados": resultados, "total": len(resultados), "sucesso": True}
