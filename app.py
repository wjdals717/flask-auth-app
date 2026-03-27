from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User # 모델과 db 객체 불러오기

app = Flask(__name__)
app.secret_key = "secret-key"

# SQLite 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# DB 초기화
db.init_app(app)

with app.app_context():
    db.create_all()

# 홈
@app.route('/')
def home():
    # 로그인한 경우
    if 'user' in session:
        return f"""
        <h1>{session['user']}님 환영합니다 👋</h1>
        <a href='/logout'>로그아웃</a>
        """
    # 로그인 안 한 경우
    return """
    <h1>Home</h1>
    <a href='/signin'>로그인</a> | <a href='/signup'>회원가입</a>
    """

# 회원가입
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        # 중복 체크
        if User.query.filter_by(username=username).first():
            return "이미 존재하는 사용자"

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/signin')
    return render_template('/signup.html')

# 로그인
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()

        if user and check_password_hash(user.password, request.form['password']):
            session['user'] = user.username
            return redirect('/')

        return "로그인 실패"

    return render_template('/signin.html')

# 로그아웃
@app.route('/logout')
def logout():
    session.pop('username', None)   # 세션 제거
    return redirect('/signin')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)