"""
Helpers para sistema de auditoria
Facilita o registro de logs em todo o sistema

NOTA: Funções desabilitadas temporariamente (AuditLog não existe no banco)
"""
import json
from flask import request
from flask_login import current_user
from models import db
from datetime import datetime

# Constantes de Ações
class AuditAction:
    # Autenticação
    LOGIN = 'LOGIN'
    LOGOUT = 'LOGOUT'
    LOGIN_FAILED = 'LOGIN_FAILED'

    # CRUD
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'
    VIEW = 'VIEW'

    # Aprovações
    APPROVE = 'APPROVE'
    REJECT = 'REJECT'
    SUBMIT = 'SUBMIT'

    # Usuários
    PASSWORD_RESET = 'PASSWORD_RESET'
    PASSWORD_CHANGE = 'PASSWORD_CHANGE'
    ROLE_CHANGE = 'ROLE_CHANGE'
    USER_ACTIVATE = 'USER_ACTIVATE'
    USER_DEACTIVATE = 'USER_DEACTIVATE'

    # Arquivos
    FILE_UPLOAD = 'FILE_UPLOAD'
    FILE_DELETE = 'FILE_DELETE'
    FILE_DOWNLOAD = 'FILE_DOWNLOAD'

    # Exportações
    EXPORT_PDF = 'EXPORT_PDF'
    EXPORT_CSV = 'EXPORT_CSV'

# Constantes de Entidades
class AuditEntity:
    USUARIO = 'Usuario'
    RELATORIO = 'Relatorio'
    REFERENCIA = 'Referencia'
    PROVA = 'Prova'
    FOTO = 'Foto'
    SISTEMA = 'Sistema'

# Constantes de Categorias
class AuditCategory:
    AUTENTICACAO = 'AUTENTICACAO'
    USUARIOS = 'USUARIOS'
    RELATORIOS = 'RELATORIOS'
    PROVAS = 'PROVAS'
    APROVACOES = 'APROVACOES'
    ARQUIVOS = 'ARQUIVOS'
    SISTEMA = 'SISTEMA'
    EXPORTACOES = 'EXPORTACOES'

# Constantes de Severidade
class AuditSeverity:
    INFO = 'INFO'
    WARNING = 'WARNING'
    CRITICAL = 'CRITICAL'

def registrar_log(
    acao,
    entidade,
    descricao,
    entidade_id=None,
    dados_antes=None,
    dados_depois=None,
    categoria=None,
    severidade=AuditSeverity.INFO,
    usuario=None
):
    """
    Registra uma ação no log de auditoria

    NOTA: Desabilitada temporariamente (AuditLog não existe no banco)
    """
    # No-op: não faz nada, apenas retorna
    pass

def log_login(usuario, sucesso=True):
    """Registra tentativa de login"""
    if sucesso:
        registrar_log(
            acao=AuditAction.LOGIN,
            entidade=AuditEntity.SISTEMA,
            descricao=f"Login realizado com sucesso",
            usuario=usuario,
            severidade=AuditSeverity.INFO
        )
    else:
        registrar_log(
            acao=AuditAction.LOGIN_FAILED,
            entidade=AuditEntity.SISTEMA,
            descricao=f"Tentativa de login falhou",
            usuario=usuario,
            severidade=AuditSeverity.WARNING
        )

def log_logout(usuario):
    """Registra logout"""
    registrar_log(
        acao=AuditAction.LOGOUT,
        entidade=AuditEntity.SISTEMA,
        descricao="Logout realizado",
        usuario=usuario,
        severidade=AuditSeverity.INFO
    )

def log_criacao(entidade, entidade_id, descricao, dados=None, usuario=None):
    """Registra criação de entidade"""
    registrar_log(
        acao=AuditAction.CREATE,
        entidade=entidade,
        entidade_id=entidade_id,
        descricao=descricao,
        dados_depois=dados,
        severidade=AuditSeverity.INFO,
        usuario=usuario
    )

def log_atualizacao(entidade, entidade_id, descricao, dados_antes=None, dados_depois=None, usuario=None):
    """Registra atualização de entidade"""
    registrar_log(
        acao=AuditAction.UPDATE,
        entidade=entidade,
        entidade_id=entidade_id,
        descricao=descricao,
        dados_antes=dados_antes,
        dados_depois=dados_depois,
        severidade=AuditSeverity.INFO,
        usuario=usuario
    )

def log_exclusao(entidade, entidade_id, descricao, dados=None, usuario=None):
    """Registra exclusão de entidade"""
    registrar_log(
        acao=AuditAction.DELETE,
        entidade=entidade,
        entidade_id=entidade_id,
        descricao=descricao,
        dados_antes=dados,
        severidade=AuditSeverity.WARNING,
        usuario=usuario
    )

def log_aprovacao(prova_id, status, motivo=None):
    """Registra aprovação ou rejeição de prova"""
    acao = AuditAction.APPROVE if status == 'Aprovada' else AuditAction.REJECT
    descricao = f"Prova {status.lower()}"
    if motivo:
        descricao += f": {motivo}"

    registrar_log(
        acao=acao,
        entidade=AuditEntity.PROVA,
        entidade_id=prova_id,
        descricao=descricao,
        dados_depois={'status': status, 'motivo': motivo},
        severidade=AuditSeverity.INFO
    )

def log_mudanca_role(usuario_id, role_antigo, role_novo):
    """Registra mudança de permissão de usuário"""
    registrar_log(
        acao=AuditAction.ROLE_CHANGE,
        entidade=AuditEntity.USUARIO,
        entidade_id=usuario_id,
        descricao=f"Nível de acesso alterado de '{role_antigo}' para '{role_novo}'",
        dados_antes={'role': role_antigo},
        dados_depois={'role': role_novo},
        categoria=AuditCategory.USUARIOS,
        severidade=AuditSeverity.WARNING
    )

def log_reset_senha(usuario_id, usuario_nome):
    """Registra reset de senha"""
    registrar_log(
        acao=AuditAction.PASSWORD_RESET,
        entidade=AuditEntity.USUARIO,
        entidade_id=usuario_id,
        descricao=f"Senha resetada para o usuário '{usuario_nome}'",
        categoria=AuditCategory.USUARIOS,
        severidade=AuditSeverity.WARNING
    )

def log_exportacao(tipo, entidade, entidade_id=None):
    """Registra exportação de dados"""
    acao = AuditAction.EXPORT_PDF if tipo == 'PDF' else AuditAction.EXPORT_CSV
    registrar_log(
        acao=acao,
        entidade=entidade,
        entidade_id=entidade_id,
        descricao=f"Exportação em {tipo}",
        categoria=AuditCategory.EXPORTACOES,
        severidade=AuditSeverity.INFO
    )

def get_acao_display(acao):
    """Retorna texto amigável para a ação"""
    mapping = {
        'LOGIN': 'Login',
        'LOGOUT': 'Logout',
        'LOGIN_FAILED': 'Login Falhou',
        'CREATE': 'Criação',
        'UPDATE': 'Atualização',
        'DELETE': 'Exclusão',
        'APPROVE': 'Aprovação',
        'REJECT': 'Rejeição',
        'PASSWORD_RESET': 'Reset de Senha',
        'ROLE_CHANGE': 'Mudança de Permissão',
        'USER_ACTIVATE': 'Usuário Ativado',
        'USER_DEACTIVATE': 'Usuário Desativado',
        'FILE_UPLOAD': 'Upload de Arquivo',
        'EXPORT_PDF': 'Exportação PDF',
        'EXPORT_CSV': 'Exportação CSV',
    }
    return mapping.get(acao, acao)

def get_categoria_display(categoria):
    """Retorna texto amigável para a categoria"""
    mapping = {
        'AUTENTICACAO': 'Autenticação',
        'USUARIOS': 'Usuários',
        'RELATORIOS': 'Relatórios',
        'PROVAS': 'Provas',
        'APROVACOES': 'Aprovações',
        'ARQUIVOS': 'Arquivos',
        'SISTEMA': 'Sistema',
        'EXPORTACOES': 'Exportações',
    }
    return mapping.get(categoria, categoria)

def get_severidade_badge(severidade):
    """Retorna classe CSS para badge de severidade"""
    mapping = {
        'INFO': 'bg-info',
        'WARNING': 'bg-warning',
        'CRITICAL': 'bg-danger',
    }
    return mapping.get(severidade, 'bg-secondary')
