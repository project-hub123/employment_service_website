from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, Vacancy, News, Message

# === Определение blueprint ===
main_bp = Blueprint('main', __name__)

# ===== Главная =====
@main_bp.route('/')
def index():
    news = News.query.order_by(News.date.desc()).limit(3).all()
    vacancies = Vacancy.query.order_by(Vacancy.date_added.desc()).limit(4).all()
    return render_template('index.html', news=news, vacancies=vacancies)


# ===== О службе =====
@main_bp.route('/about')
def about():
    return render_template('about.html')


# ===== Новости =====
@main_bp.route('/news')
def news():
    all_news = News.query.order_by(News.date.desc()).all()
    return render_template('news.html', news=all_news)


# ===== Вакансии =====
@main_bp.route('/vacancies')
def vacancies():
    all_vacancies = Vacancy.query.order_by(Vacancy.date_added.desc()).all()
    return render_template('vacancies.html', vacancies=all_vacancies)


# ===== Работодателям (форма вакансий) =====
@main_bp.route('/employers', methods=['GET', 'POST'])
@login_required
def employers():
    success = False
    if request.method == 'POST':
        company = request.form['company']
        position = request.form['position']
        city = request.form['city']
        salary = request.form['salary']
        description = request.form['description']
        new_vac = Vacancy(
            company=company,
            position=position,
            city=city,
            salary=salary,
            description=description
        )
        db.session.add(new_vac)
        db.session.commit()
        success = True
    return render_template('employers.html', success=success)


# ===== Контакты (форма обратной связи) =====
@main_bp.route('/contacts', methods=['GET', 'POST'])
def contacts():
    success = False
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        msg = Message(name=name, email=email, text=message)
        db.session.add(msg)
        db.session.commit()
        success = True
    return render_template('contacts.html', success=success)


# ===== Карта сайта =====
@main_bp.route('/site-map')
def site_map():
    return render_template('site_map.html')


# ===== Авторизация =====
@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return redirect(url_for('main.index'))  
        else:
            error = 'Неверный логин или пароль'
    return render_template('login.html', error=error)


# ===== Регистрация =====
@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    message = None
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm = request.form['confirm']

        if password != confirm:
            message = 'Пароли не совпадают!'
        elif User.query.filter_by(username=username).first():
            message = 'Такой логин уже зарегистрирован.'
        else:
            hashed_pw = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            message = 'Регистрация успешна! Теперь войдите в систему.'
    return render_template('register.html', message=message)


# ===== Профиль пользователя =====
@main_bp.route('/profile')
@login_required
def user_profile():
    return render_template('user_profile.html')


# ===== Выход =====
@main_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))  


# ===== Админ-панель =====
@main_bp.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        flash('Недостаточно прав для доступа к этой странице.')
        return redirect(url_for('main.index'))  
    return render_template('admin_panel.html')


# ===== Ошибка 404 =====
@main_bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
