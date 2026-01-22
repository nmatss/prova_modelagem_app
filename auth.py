from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, User
from audit_helpers import log_login, log_logout
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

def get_user_by_id(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember') == 'on'

        # Log para debug
        current_app.logger.info(f"Tentativa de login: username='{username}'")

        user = User.query.filter_by(username=username).first()

        if not user:
            current_app.logger.warning(f"Login falhou: usuário '{username}' não encontrado")
            flash('Login inválido. Verifique seu usuário e senha.', 'error')
            return render_template('login.html')

        # Verificar se o usuário está ativo
        if not user.is_active:
            current_app.logger.warning(f"Login falhou: usuário '{username}' está desativado")
            flash('Sua conta está desativada. Entre em contato com o administrador.', 'error')
            log_login(user, sucesso=False)
            return render_template('login.html')

        # Verificar senha
        if check_password_hash(user.password_hash, password):
            # Login bem-sucedido
            login_user(user, remember=remember)

            # Atualizar último acesso
            user.ultimo_acesso = datetime.utcnow()
            db.session.commit()

            # Log de login bem-sucedido
            log_login(user, sucesso=True)
            current_app.logger.info(f"Login bem-sucedido: '{username}'")

            return redirect(url_for('dashboard'))
        else:
            # Senha incorreta
            current_app.logger.warning(f"Login falhou: senha incorreta para '{username}'")
            log_login(user, sucesso=False)
            flash('Login inválido. Verifique seu usuário e senha.', 'error')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    # Log de logout
    log_logout(current_user)
    logout_user()
    return redirect(url_for('auth.login'))

@auth_bp.route('/esqueci-senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        email = request.form.get('email')
        # Por enquanto apenas simula o envio
        flash(f'Se o e-mail {email} estiver cadastrado, você receberá um link para redefinir sua senha.', 'info')
        return redirect(url_for('auth.login'))
        
    return render_template('esqueci_senha.html')
