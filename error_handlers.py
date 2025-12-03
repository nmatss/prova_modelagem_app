from flask import render_template, request
import traceback

def register_error_handlers(app):
    """Registra handlers de erro customizados"""
    
    @app.errorhandler(404)
    def not_found_error(error):
        """Página não encontrada"""
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden_error(error):
        """Acesso negado"""
        return render_template('errors/403.html'), 403
    
    @app.errorhandler(500)
    def internal_error(error):
        """Erro interno do servidor"""
        # Log do erro
        app.logger.error(f'Erro 500: {error}')
        app.logger.error(traceback.format_exc())
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(413)
    def request_entity_too_large(error):
        """Arquivo muito grande"""
        return render_template('errors/413.html'), 413
    
    @app.errorhandler(Exception)
    def handle_exception(error):
        """Handler genérico para exceções não tratadas"""
        app.logger.error(f'Exceção não tratada: {error}')
        app.logger.error(traceback.format_exc())
        
        # Em produção, não mostrar detalhes do erro
        if app.config.get('DEBUG'):
            raise error
        
        return render_template('errors/500.html'), 500
