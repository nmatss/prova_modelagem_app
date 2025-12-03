from app import app
from models import db, User
from werkzeug.security import generate_password_hash

def create_admin_user():
    with app.app_context():
        username = 'admin'
        password = 'admin123'
        
        user = User.query.filter_by(username=username).first()
        
        if user:
            print(f"✗ Usuário '{username}' já existe.")
            if not user.is_admin:
                print(f"  Atualizando '{username}' para admin...")
                user.is_admin = True
                db.session.commit()
                print(f"✓ '{username}' agora é um administrador.")
        else:
            print(f"Criando usuário '{username}'...")
            new_user = User(username=username, password_hash=generate_password_hash(password), is_admin=True)
            db.session.add(new_user)
            db.session.commit()
            print(f"✓ Usuário criado com sucesso!")
            print(f"  Username: {username}")
            print(f"  Password: {password}")

if __name__ == "__main__":
    create_admin_user()
