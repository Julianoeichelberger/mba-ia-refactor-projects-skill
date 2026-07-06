import logging
from flask import Blueprint, jsonify
from models.database import get_db

logger = logging.getLogger(__name__)

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/health", methods=["GET"])
def health_check():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 1")
    cursor.execute("SELECT COUNT(*) as c FROM produtos")
    produtos = cursor.fetchone()["c"]
    cursor.execute("SELECT COUNT(*) as c FROM usuarios")
    usuarios = cursor.fetchone()["c"]
    cursor.execute("SELECT COUNT(*) as c FROM pedidos")
    pedidos = cursor.fetchone()["c"]

    return jsonify({
        "status": "ok",
        "database": "connected",
        "counts": {
            "produtos": produtos,
            "usuarios": usuarios,
            "pedidos": pedidos,
        },
        "versao": "1.0.0",
    }), 200
