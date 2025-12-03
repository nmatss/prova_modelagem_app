from models import db, User
from werkzeug.security import generate_password_hash

def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            print("Criando usuário admin padrão...")
            admin = User(
                username='admin',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado: admin / admin123")
