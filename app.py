"""
Main Application File
Ứng dụng Flask chính với các route và cấu hình
"""
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
import os
from datetime import timedelta

from database import Database
from auth import AuthService
from email_service import EmailService
from utils import generate_otp, verify_otp_code

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Khởi tạo services
db = Database()
auth_service = AuthService(db)
email_service = EmailService()

def login_required(f):
    """Decorator để bảo vệ các route cần đăng nhập"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để tiếp tục', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Trang chủ"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Đăng ký tài khoản mới"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        phone = request.form.get('phone', '')
        
        # Validation
        if not all([username, email, password, confirm_password]):
            flash('Vui lòng điền đầy đủ thông tin', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Mật khẩu xác nhận không khớp', 'error')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('Mật khẩu phải có ít nhất 8 ký tự', 'error')
            return render_template('register.html')
        
        # Đăng ký user
        result = auth_service.register_user(username, email, password, phone)
        
        if result['success']:
            flash('Đăng ký thành công! Vui lòng đăng nhập', 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'error')
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Đăng nhập - Bước 1: Xác thực mật khẩu"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not all([email, password]):
            flash('Vui lòng điền đầy đủ thông tin', 'error')
            return render_template('login.html')
        
        # Xác thực mật khẩu
        result = auth_service.authenticate_user(email, password)
        
        if result['success']:
            user = result['user']
            
            # Tạo OTP và gửi email
            otp_code = generate_otp()
            auth_service.save_otp(user['id'], otp_code)
            
            # Gửi OTP qua email
            email_sent = email_service.send_otp_email(user['email'], user['username'], otp_code)
            
            if email_sent:
                # Lưu thông tin tạm vào session
                session['temp_user_id'] = user['id']
                session['temp_email'] = user['email']
                flash('OTP đã được gửi đến email của bạn', 'info')
                return redirect(url_for('verify_otp'))
            else:
                flash('Không thể gửi OTP. Vui lòng thử lại', 'error')
        else:
            flash(result['message'], 'error')
    
    return render_template('login.html')

@app.route('/verify-otp', methods=['GET', 'POST'])
def verify_otp():
    """Đăng nhập - Bước 2: Xác thực OTP"""
    if 'temp_user_id' not in session:
        flash('Phiên làm việc hết hạn. Vui lòng đăng nhập lại', 'warning')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        otp_code = request.form.get('otp')
        user_id = session.get('temp_user_id')
        
        if not otp_code:
            flash('Vui lòng nhập mã OTP', 'error')
            return render_template('verify_otp.html')
        
        # Xác thực OTP
        if auth_service.verify_otp(user_id, otp_code):
            # Đăng nhập thành công
            user = db.get_user_by_id(user_id)
            session.permanent = True
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            
            # Xóa thông tin tạm
            session.pop('temp_user_id', None)
            session.pop('temp_email', None)
            
            # Cập nhật last login
            auth_service.update_last_login(user_id)
            
            flash(f'Chào mừng {user["username"]}!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Mã OTP không đúng hoặc đã hết hạn', 'error')
    
    return render_template('verify_otp.html', email=session.get('temp_email'))

@app.route('/resend-otp', methods=['POST'])
def resend_otp():
    """Gửi lại mã OTP"""
    if 'temp_user_id' not in session:
        return jsonify({'success': False, 'message': 'Phiên làm việc hết hạn'})
    
    user_id = session.get('temp_user_id')
    user = db.get_user_by_id(user_id)
    
    # Tạo OTP mới
    otp_code = generate_otp()
    auth_service.save_otp(user_id, otp_code)
    
    # Gửi email
    email_sent = email_service.send_otp_email(user['email'], user['username'], otp_code)
    
    if email_sent:
        return jsonify({'success': True, 'message': 'OTP mới đã được gửi'})
    else:
        return jsonify({'success': False, 'message': 'Không thể gửi OTP'})

@app.route('/dashboard')
@login_required
def dashboard():
    """Trang dashboard sau khi đăng nhập"""
    user = db.get_user_by_id(session['user_id'])
    return render_template('dashboard.html', user=user)

@app.route('/profile')
@login_required
def profile():
    """Trang thông tin cá nhân"""
    user = db.get_user_by_id(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/security')
@login_required
def security():
    """Trang cài đặt bảo mật"""
    user = db.get_user_by_id(session['user_id'])
    return render_template('security.html', user=user)

@app.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Đổi mật khẩu"""
    current_password = request.form.get('current_password')
    new_password = request.form.get('new_password')
    confirm_password = request.form.get('confirm_password')
    
    if not all([current_password, new_password, confirm_password]):
        flash('Vui lòng điền đầy đủ thông tin', 'error')
        return redirect(url_for('security'))
    
    if new_password != confirm_password:
        flash('Mật khẩu mới không khớp', 'error')
        return redirect(url_for('security'))
    
    if len(new_password) < 8:
        flash('Mật khẩu mới phải có ít nhất 8 ký tự', 'error')
        return redirect(url_for('security'))
    
    # Đổi mật khẩu
    result = auth_service.change_password(session['user_id'], current_password, new_password)
    
    if result['success']:
        flash('Đổi mật khẩu thành công', 'success')
    else:
        flash(result['message'], 'error')
    
    return redirect(url_for('security'))

@app.route('/logout')
@login_required
def logout():
    """Đăng xuất"""
    username = session.get('username', 'User')
    session.clear()
    flash(f'Tạm biệt {username}!', 'info')
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Khởi tạo database
    db.init_db()
    
    # Chạy app
    print("🚀 Server đang chạy tại http://localhost:5000")
    print("📧 Cấu hình email trong email_service.py để gửi OTP")
    app.run(debug=True, host='0.0.0.0', port=5000)
