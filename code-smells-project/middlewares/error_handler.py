import logging
from flask import jsonify

logger = logging.getLogger(__name__)


class AppError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


def register_error_handlers(app):
    @app.errorhandler(AppError)
    def handle_app_error(error):
        logger.warning("App error: %s", error)
        return jsonify({"erro": str(error), "sucesso": False}), error.status_code

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"erro": "Requisicao invalida", "sucesso": False}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"erro": "Recurso nao encontrado", "sucesso": False}), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error("Internal error: %s", error)
        return jsonify({"erro": "Erro interno do servidor", "sucesso": False}), 500
