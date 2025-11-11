from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

# ===== Пользователь =====
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='user')  # user / admin

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ===== Вакансии =====
class Vacancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(120), nullable=False)
    position = db.Column(db.String(120), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    salary = db.Column(db.String(50))
    description = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Vacancy {self.position}>'


# ===== Новости =====
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    short_text = db.Column(db.String(300))
    full_text = db.Column(db.Text)
    image = db.Column(db.String(120))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<News {self.title}>'


# ===== Сообщения (форма обратной связи) =====
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    text = db.Column(db.Text)
    date_sent = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Message from {self.name}>'
