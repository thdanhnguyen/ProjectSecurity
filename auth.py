"""
Authentication Service
Xử lý logic xác thực, băm mật khẩu, OTP
"""
import hashlib
import bcrypt
from datetime import datetime, timedelta
from utils import hash_password_md5, hash_password_sha256, verify_password

class AuthService:
    def __init__(self, database):
        self.db = database
    
    def register_user(self, username, email, password, phone=''):
        """Đăng ký user mới với mật khẩu băm"""
        # Băm mật khẩu với nhiều thuật toán
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        password_md5 = hash_password_md5(password)
        password_sha256 = hash_password_sha256(password)
        
        # Tạo user trong database
        result = self.db.create_user(
            username=username,
            email=email,
            password_hash=password_hash,
            password_md5=password_md5,
            password_sha256=password_sha256,
            phone=phone
        )
        
        return result
    
    def authenticate_user(self, email, password):
        """Xác thực user với email và mật khẩu"""
        user = self.db.get_user_by_email(email)
        
        if not user:
            return {'success': False, 'message': 'Email không tồn tại'}
        
        if not user['is_active']:
            return {'success': False, 'message': 'Tài khoản đã bị khóa'}
        
        # Verify password với bcrypt
        if verify_password(password, user['password_hash']):
            return {'success': True, 'user': user}
        else:
            return {'success': False, 'message': 'Mật khẩu không đúng'}
    
    def save_otp(self, user_id, otp_code, expiry_minutes=5):
        """Lưu mã OTP với thời gian hết hạn"""
        expires_at = datetime.now() + timedelta(minutes=expiry_minutes)
        self.db.save_otp(user_id, otp_code, expires_at)
    
    def verify_otp(self, user_id, otp_code):
        """Xác thực mã OTP"""
        otp_record = self.db.get_valid_otp(user_id, otp_code)
        
        if otp_record:
            # Đánh dấu OTP đã sử dụng
            self.db.mark_otp_used(otp_record['id'])
            return True
        
        return False
    
    def update_last_login(self, user_id):
        """Cập nhật thời gian đăng nhập cuối"""
        self.db.update_last_login(user_id)
    
    def change_password(self, user_id, current_password, new_password):
        """Đổi mật khẩu"""
        user = self.db.get_user_by_id(user_id)
        
        if not user:
            return {'success': False, 'message': 'User không tồn tại'}
        
        # Verify mật khẩu hiện tại
        if not verify_password(current_password, user['password_hash']):
            return {'success': False, 'message': 'Mật khẩu hiện tại không đúng'}
        
        # Băm mật khẩu mới
        password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        password_md5 = hash_password_md5(new_password)
        password_sha256 = hash_password_sha256(new_password)
        
        # Cập nhật database
        self.db.update_password(user_id, password_hash, password_md5, password_sha256)
        
        return {'success': True, 'message': 'Đổi mật khẩu thành công'}
    
    def get_password_hashes(self, user_id):
        """Lấy các hash của mật khẩu (để demo)"""
        user = self.db.get_user_by_id(user_id)
        if user:
            return {
                'bcrypt': user['password_hash'],
                'md5': user['password_md5'],
                'sha256': user['password_sha256']
            }
        return None
