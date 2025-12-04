from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, User, Relatorio, Referencia, Prova, Foto
from functools import wraps
from werkzeug.security import generate_password_hash
import secrets
import string
from audit_helpers import (log_criacao, log_atualizacao, log_exclusao,
                           log_reset_senha, log_mudanca_role,
                           AuditEntity, AuditAction)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Acesso negado. Área restrita para administradores.", "error")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def gerar_senha_aleatoria(tamanho=12):
    """Gera uma senha aleatória forte"""
    caracteres = string.ascii_letters + string.digits + "!@#$%&*"
    senha = ''.join(secrets.choice(caracteres) for _ in range(tamanho))
    return senha

def role_display(role):
    """Retorna o nome amigável do role"""
    roles = {
        'admin': 'Administrador',
        'gestor': 'Gestor',
        'usuario': 'Usuário'
    }
    return roles.get(role, 'Usuário')

@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    users_count = User.query.count()
    relatorios_count = Relatorio.query.count()
    referencias_count = Referencia.query.count()
    provas_count = Prova.query.count()
    
    return render_template('admin/dashboard.html', 
                           users_count=users_count,
                           relatorios_count=relatorios_count,
                           referencias_count=referencias_count,
                           provas_count=provas_count)

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """Lista todos os usuários do sistema"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users, role_display=role_display)

@admin_bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    """Cria um novo usuário com senha gerada"""
    if request.method == 'POST':
        try:
            username = request.form.get('username')
            email = request.form.get('email')
            nome_completo = request.form.get('nome_completo')
            role = request.form.get('role', 'usuario')

            # Validações
            if not username or not email:
                flash("Username e email são obrigatórios.", "error")
                return redirect(url_for('admin.create_user'))

            # Verificar se usuário já existe
            if User.query.filter_by(username=username).first():
                flash(f"Username '{username}' já está em uso.", "error")
                return redirect(url_for('admin.create_user'))

            if User.query.filter_by(email=email).first():
                flash(f"Email '{email}' já está em uso.", "error")
                return redirect(url_for('admin.create_user'))

            # Gerar senha aleatória
            senha_gerada = gerar_senha_aleatoria(12)

            # Criar usuário
            novo_usuario = User(
                username=username,
                email=email,
                nome_completo=nome_completo,
                password_hash=generate_password_hash(senha_gerada),
                role=role,
                is_admin=(role == 'admin'),
                is_active=True,
                senha_temporaria=True
            )

            db.session.add(novo_usuario)
            db.session.commit()

            # Log de criação de usuário
            log_criacao(
                entidade=AuditEntity.USUARIO,
                entidade_id=novo_usuario.id,
                descricao=f"Usuário '{username}' criado pelo admin",
                dados={
                    'username': username,
                    'email': email,
                    'nome_completo': nome_completo,
                    'role': role
                }
            )

            flash(f"Usuário '{username}' criado com sucesso! Senha temporária: {senha_gerada}", "success")
            return redirect(url_for('admin.users'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao criar usuário: {e}", "error")
            return redirect(url_for('admin.create_user'))

    return render_template('admin/create_user.html')

@admin_bp.route('/users/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    """Edita um usuário existente"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        try:
            # Capturar dados antigos
            dados_antes = {
                'username': user.username,
                'email': user.email,
                'nome_completo': user.nome_completo,
                'role': user.role,
                'is_active': user.is_active
            }
            role_antigo = user.role

            user.username = request.form.get('username')
            user.email = request.form.get('email')
            user.nome_completo = request.form.get('nome_completo')
            user.role = request.form.get('role', 'usuario')
            user.is_admin = (user.role == 'admin')
            user.is_active = request.form.get('is_active') == 'on'

            # Capturar dados novos
            dados_depois = {
                'username': user.username,
                'email': user.email,
                'nome_completo': user.nome_completo,
                'role': user.role,
                'is_active': user.is_active
            }

            db.session.commit()

            # Log de atualização
            log_atualizacao(
                entidade=AuditEntity.USUARIO,
                entidade_id=user.id,
                descricao=f"Usuário '{user.username}' atualizado",
                dados_antes=dados_antes,
                dados_depois=dados_depois
            )

            # Log específico para mudança de role
            if role_antigo != user.role:
                log_mudanca_role(user.id, role_antigo, user.role)

            flash(f"Usuário '{user.username}' atualizado com sucesso!", "success")
            return redirect(url_for('admin.users'))

        except Exception as e:
            db.session.rollback()
            flash(f"Erro ao atualizar usuário: {e}", "error")

    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/users/reset_password/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def reset_password(user_id):
    """Redefine a senha de um usuário"""
    user = User.query.get_or_404(user_id)

    try:
        # Gerar nova senha aleatória
        nova_senha = gerar_senha_aleatoria(12)
        user.password_hash = generate_password_hash(nova_senha)
        user.senha_temporaria = True

        db.session.commit()

        # Log de reset de senha
        log_reset_senha(user.id, user.username)

        flash(f"Senha do usuário '{user.username}' redefinida! Nova senha: {nova_senha}", "success")

    except Exception as e:
        db.session.rollback()
        flash(f"Erro ao redefinir senha: {e}", "error")

    return redirect(url_for('admin.users'))

@admin_bp.route('/users/toggle_active/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_active(user_id):
    """Ativa/desativa um usuário"""
    if user_id == current_user.id:
        flash("Você não pode desativar a si mesmo.", "error")
        return redirect(url_for('admin.users'))

    user = User.query.get_or_404(user_id)
    status_antigo = user.is_active
    user.is_active = not user.is_active
    db.session.commit()

    # Log de ativação/desativação
    log_atualizacao(
        entidade=AuditEntity.USUARIO,
        entidade_id=user.id,
        descricao=f"Usuário '{user.username}' {'ativado' if user.is_active else 'desativado'}",
        dados_antes={'is_active': status_antigo},
        dados_depois={'is_active': user.is_active}
    )

    status = "ativado" if user.is_active else "desativado"
    flash(f"Usuário '{user.username}' {status} com sucesso.", "success")
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Desativa um usuário (soft delete)"""
    if user_id == current_user.id:
        flash("Você não pode excluir a si mesmo.", "error")
        return redirect(url_for('admin.users'))

    user = User.query.get_or_404(user_id)

    # Log de exclusão (soft delete)
    log_exclusao(
        entidade=AuditEntity.USUARIO,
        entidade_id=user.id,
        descricao=f"Usuário '{user.username}' desativado (soft delete)",
        dados={
            'username': user.username,
            'email': user.email,
            'role': user.role
        }
    )

    user.is_active = False
    db.session.commit()
    flash(f"Usuário '{user.username}' desativado com sucesso.", "success")
    return redirect(url_for('admin.users'))
