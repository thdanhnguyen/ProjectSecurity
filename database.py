"""
Database Module
Quản lý kết nối và thao tác với SQLite database
"""
import sqlite3
from datetime import datetime
import os

class Database:
    def __init__(self, db_name='secure_auth.db'):
        self.db_name = db_name
        self.conn = None
    
    def get_connection(self):
        """Tạo kết nối đến database"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def init_db(self):
        """Khởi tạo database và các bảng"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Bảng users
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone TEXT,
                password_hash TEXT NOT NULL,
                password_md5 TEXT NOT NULL,
                password_sha256 TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Bảng OTP
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS otp_codes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                otp_code TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                is_used BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Bảng login history
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS login_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ip_address TEXT,
                user_agent TEXT,
                status TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        print("✅ Database initialized successfully")
    
    def create_user(self, username, email, password_hash, password_md5, password_sha256, phone=''):
        """Tạo user mới"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO users (username, email, phone, password_hash, password_md5, password_sha256)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (username, email, phone, password_hash, password_md5, password_sha256))
            
            conn.commit()
            return {'success': True, 'user_id': cursor.lastrowid}
        except sqlite3.IntegrityError as e:
            if 'username' in str(e):
                return {'success': False, 'message': 'Tên đăng nhập đã tồn tại'}
            elif 'email' in str(e):
                return {'success': False, 'message': 'Email đã được sử dụng'}
            else:
                return {'success': False, 'message': 'Lỗi tạo tài khoản'}
        except Exception as e:
            return {'success': False, 'message': f'Lỗi: {str(e)}'}
    
    def get_user_by_email(self, email):
        """Lấy thông tin user theo email"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_user_by_id(self, user_id):
        """Lấy thông tin user theo ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def update_last_login(self, user_id):
        """Cập nhật thời gian đăng nhập cuối"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
        ''', (user_id,))
        conn.commit()
    
    def save_otp(self, user_id, otp_code, expires_at):
        """Lưu mã OTP"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO otp_codes (user_id, otp_code, expires_at)
            VALUES (?, ?, ?)
        ''', (user_id, otp_code, expires_at))
        conn.commit()
    
    def get_valid_otp(self, user_id, otp_code):
        """Lấy OTP hợp lệ"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM otp_codes 
            WHERE user_id = ? AND otp_code = ? AND is_used = 0 
            AND expires_at > CURRENT_TIMESTAMP
            ORDER BY created_at DESC LIMIT 1
        ''', (user_id, otp_code))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def mark_otp_used(self, otp_id):
        """Đánh dấu OTP đã sử dụng"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE otp_codes SET is_used = 1 WHERE id = ?', (otp_id,))
        conn.commit()
    
    def add_login_history(self, user_id, ip_address, user_agent, status):
        """Thêm lịch sử đăng nhập"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO login_history (user_id, ip_address, user_agent, status)
            VALUES (?, ?, ?, ?)
        ''', (user_id, ip_address, user_agent, status))
        conn.commit()
    
    def update_password(self, user_id, password_hash, password_md5, password_sha256):
        """Cập nhật mật khẩu"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users 
            SET password_hash = ?, password_md5 = ?, password_sha256 = ?
            WHERE id = ?
        ''', (password_hash, password_md5, password_sha256, user_id))
        conn.commit()
    
    def close(self):
        """Đóng kết nối database"""
        if self.conn:
            self.conn.close()
            self.conn = None
