from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, User, Relatorio, Referencia, Prova, Foto
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Acesso negado. Área restrita para administradores.", "error")
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

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
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@admin_bp.route('/users/delete/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    if user_id == current_user.id:
        flash("Você não pode excluir a si mesmo.", "error")
        return redirect(url_for('admin.users'))
        
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"Usuário {user.username} excluído com sucesso.", "success")
    return redirect(url_for('admin.users'))

@admin_bp.route('/users/toggle_admin/<int:user_id>', methods=['POST'])
@login_required
@admin_required
def toggle_admin(user_id):
    if user_id == current_user.id:
        flash("Você não pode alterar seu próprio status de admin.", "error")
        return redirect(url_for('admin.users'))
        
    user = User.query.get_or_404(user_id)
    user.is_admin = not user.is_admin
    db.session.commit()
    status = "Administrador" if user.is_admin else "Usuário Comum"
    flash(f"Status de {user.username} alterado para {status}.", "success")
    return redirect(url_for('admin.users'))
