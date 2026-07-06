import logging
from models.pedido_model import PedidoModel
from middlewares.error_handler import AppError
from config.settings import VALID_ORDER_STATUSES, DISCOUNT_TIERS

logger = logging.getLogger(__name__)

model = PedidoModel()


def criar_pedido(data):
    if not data:
        raise AppError("Dados invalidos", 400)

    usuario_id = data.get("usuario_id")
    itens = data.get("itens", [])

    if not usuario_id:
        raise AppError("Usuario ID e obrigatorio", 400)
    if not itens:
        raise AppError("Pedido deve ter pelo menos 1 item", 400)

    resultado = model.create(usuario_id, itens)

    if "erro" in resultado:
        raise AppError(resultado["erro"], 400)

    logger.info(
        "Pedido %d criado para usuario %d", resultado["pedido_id"], usuario_id
    )
    return {"dados": resultado, "sucesso": True, "mensagem": "Pedido criado com sucesso"}


def listar_pedidos_usuario(usuario_id):
    pedidos = model.get_by_user(usuario_id)
    return {"dados": pedidos, "sucesso": True}


def listar_todos_pedidos():
    pedidos = model.get_all()
    return {"dados": pedidos, "sucesso": True}


def atualizar_status_pedido(pedido_id, data):
    if not data:
        raise AppError("Dados invalidos", 400)

    novo_status = data.get("status", "")
    if novo_status not in VALID_ORDER_STATUSES:
        raise AppError("Status invalido", 400)

    model.update_status(pedido_id, novo_status)

    if novo_status == "aprovado":
        logger.info("Pedido %d aprovado - preparar envio", pedido_id)
    elif novo_status == "cancelado":
        logger.info("Pedido %d cancelado - devolver estoque", pedido_id)

    return {"sucesso": True, "mensagem": "Status atualizado"}


def relatorio_vendas():
    report = model.get_sales_report()
    faturamento = report["faturamento_bruto"]

    desconto = 0
    for threshold, rate in DISCOUNT_TIERS:
        if faturamento > threshold:
            desconto = faturamento * rate
            break

    report["faturamento_bruto"] = round(faturamento, 2)
    report["desconto_aplicavel"] = round(desconto, 2)
    report["faturamento_liquido"] = round(faturamento - desconto, 2)
    report["ticket_medio"] = (
        round(faturamento / report["total_pedidos"], 2)
        if report["total_pedidos"] > 0
        else 0
    )

    return {"dados": report, "sucesso": True}
