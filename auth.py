from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, User
from audit_helpers import log_login, log_logout

auth_bp = Blueprint('auth', __name__)

def get_user_by_id(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            # Log de login bem-sucedido
            log_login(user, sucesso=True)
            return redirect(url_for('dashboard'))
        else:
            # Log de tentativa de login falhada
            if user:
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
