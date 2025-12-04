from flask import render_template, request, jsonify
import logging

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Registra handlers para erros HTTP comuns"""

    @app.errorhandler(400)
    def bad_request(error):
        """Requisição inválida"""
        logger.warning(f"Bad Request: {request.url} - {error}")
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify(error="Requisição inválida"), 400
        return render_template('errors/400.html', error=error), 400

    @app.errorhandler(403)
    def forbidden(error):
        """Acesso proibido"""
        logger.warning(f"Forbidden: {request.url} - IP: {request.remote_addr}")
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify(error="Acesso negado"), 403
        return render_template('errors/403.html', error=error), 403

    @app.errorhandler(404)
    def not_found(error):
        """Página não encontrada"""
        logger.info(f"Not Found: {request.url}")
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify(error="Recurso não encontrado"), 404
        return render_template('errors/404.html'), 404

    @app.errorhandler(429)
    def too_many_requests(error):
        """Muitas requisições (Rate Limit)"""
        logger.warning(f"Rate Limit Exceeded: {request.remote_addr} - {request.url}")
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify(error="Muitas requisições. Tente novamente mais tarde."), 429
        return render_template('errors/429.html', error=error), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        """Erro interno do servidor"""
        logger.error(f"Internal Server Error: {request.url} - {error}", exc_info=True)
        if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
            return jsonify(error="Erro interno do servidor"), 500
        return render_template('errors/500.html'), 500
