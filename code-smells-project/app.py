import logging
from flask import Flask, jsonify
from flask_cors import CORS
from config.settings import SECRET_KEY, DEBUG, PORT, HOST
from models.database import get_db
from views.produto_routes import produto_bp
from views.usuario_routes import usuario_bp
from views.pedido_routes import pedido_bp
from views.admin_routes import admin_bp
from middlewares.error_handler import register_error_handlers

logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    CORS(app)

    get_db()

    app.register_blueprint(produto_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(admin_bp)

    register_error_handlers(app)

    @app.route("/")
    def index():
        return jsonify({
            "mensagem": "Bem-vindo a API da Loja",
            "versao": "1.0.0",
            "endpoints": {
                "produtos": "/produtos",
                "usuarios": "/usuarios",
                "pedidos": "/pedidos",
                "login": "/login",
                "relatorios": "/relatorios/vendas",
                "health": "/health",
            },
        })

    return app


if __name__ == "__main__":
    app = create_app()
    logger.info("=" * 50)
    logger.info("SERVIDOR INICIADO")
    logger.info("Rodando em http://%s:%d", HOST, PORT)
    logger.info("=" * 50)
    app.run(host=HOST, port=PORT, debug=DEBUG)
