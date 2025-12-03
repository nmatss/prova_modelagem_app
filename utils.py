import os
from werkzeug.utils import secure_filename
from flask import current_app, flash
from config import allowed_file, Config
from PIL import Image

def save_file(file_storage, max_size_mb=16):
    """
    Salva um arquivo com validações de segurança
    
    Args:
        file_storage: FileStorage object do Flask
        max_size_mb: Tamanho máximo em MB
    
    Returns:
        str: Nome do arquivo salvo ou None se falhar
    """
    if not file_storage or file_storage.filename == '':
        return None
    
    filename = file_storage.filename
    
    # Validar extensão
    if not allowed_file(filename):
        flash(f'Tipo de arquivo não permitido: {filename}. Use apenas: {", ".join(Config.ALLOWED_EXTENSIONS)}', 'error')
        return None
    
    # Sanitizar nome do arquivo
    filename = secure_filename(filename)
    
    # Verificar tamanho (adicional ao MAX_CONTENT_LENGTH do Flask)
    file_storage.seek(0, os.SEEK_END)
    file_size = file_storage.tell()
    file_storage.seek(0)
    
    max_size_bytes = max_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        flash(f'Arquivo muito grande: {filename}. Máximo: {max_size_mb}MB', 'error')
        return None
    
    # Gerar nome único se arquivo já existir
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        name, ext = os.path.splitext(filename)
        counter = 1
        while os.path.exists(filepath):
            filename = f"{name}_{counter}{ext}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            counter += 1
    
    # Salvar arquivo
    try:
        file_storage.save(filepath)
        
        # Se for imagem, validar que é realmente uma imagem
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            try:
                img = Image.open(filepath)
                img.verify()  # Verifica se é uma imagem válida
            except Exception as e:
                os.remove(filepath)  # Remove arquivo inválido
                flash(f'Arquivo de imagem inválido: {filename}', 'error')
                return None
        
        return filename
    except Exception as e:
        flash(f'Erro ao salvar arquivo: {str(e)}', 'error')
        return None

def delete_file(filename):
    """
    Deleta um arquivo do sistema de forma segura
    
    Args:
        filename: Nome do arquivo a deletar
    
    Returns:
        bool: True se deletado com sucesso
    """
    if not filename:
        return False
    
    try:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception as e:
        print(f"Erro ao deletar arquivo {filename}: {e}")
    
    return False

def get_file_size_mb(filename):
    """Retorna o tamanho do arquivo em MB"""
    try:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(filepath):
            size_bytes = os.path.getsize(filepath)
            return round(size_bytes / (1024 * 1024), 2)
    except:
        pass
    return 0

def create_thumbnail(filename, size=(150, 150)):
    """
    Cria uma thumbnail de uma imagem
    
    Args:
        filename: Nome do arquivo de imagem
        size: Tupla (largura, altura) da thumbnail
    
    Returns:
        str: Nome do arquivo thumbnail ou None
    """
    if not filename or not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        return None
    
    try:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(filepath):
            return None
        
        # Criar nome do thumbnail
        name, ext = os.path.splitext(filename)
        thumb_filename = f"{name}_thumb{ext}"
        thumb_filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], thumb_filename)
        
        # Criar thumbnail
        img = Image.open(filepath)
        img.thumbnail(size, Image.Resampling.LANCZOS)
        img.save(thumb_filepath, optimize=True, quality=85)
        
        return thumb_filename
    except Exception as e:
        print(f"Erro ao criar thumbnail para {filename}: {e}")
        return None
