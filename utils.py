"""
Utility Functions
Các hàm tiện ích: băm mật khẩu, tạo OTP, validation
"""
import hashlib
import bcrypt
import random
import string
import re

def hash_password_md5(password):
    """Băm mật khẩu với MD5 (không an toàn, chỉ để demo)"""
    return hashlib.md5(password.encode('utf-8')).hexdigest()

def hash_password_sha256(password):
    """Băm mật khẩu với SHA-256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def hash_password_bcrypt(password):
    """Băm mật khẩu với bcrypt (an toàn nhất)"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed_password):
    """Xác thực mật khẩu với bcrypt"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    except:
        return False

def generate_otp(length=6):
    """Tạo mã OTP ngẫu nhiên"""
    return ''.join(random.choices(string.digits, k=length))

def verify_otp_code(otp_code, length=6):
    """Kiểm tra định dạng OTP"""
    return len(otp_code) == length and otp_code.isdigit()

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password_strength(password):
    """Kiểm tra độ mạnh mật khẩu"""
    if len(password) < 8:
        return {'valid': False, 'message': 'Mật khẩu phải có ít nhất 8 ký tự'}
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in string.punctuation for c in password)
    
    strength = sum([has_upper, has_lower, has_digit, has_special])
    
    if strength < 3:
        return {
            'valid': False, 
            'message': 'Mật khẩu cần có chữ hoa, chữ thường, số và ký tự đặc biệt'
        }
    
    return {'valid': True, 'message': 'Mật khẩu đủ mạnh'}

def sanitize_input(text):
    """Làm sạch input để tránh XSS"""
    if not text:
        return ''
    # Loại bỏ các ký tự nguy hiểm
    dangerous_chars = ['<', '>', '"', "'", '&', '/', '\\']
    for char in dangerous_chars:
        text = text.replace(char, '')
    return text.strip()
