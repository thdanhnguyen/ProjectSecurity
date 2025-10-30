# 🔐 Ứng Dụng Xác Thực OTP & Mật Khẩu Băm

Hệ thống xác thực người dùng an toàn với OTP và mật khẩu băm (MD5/SHA-256/Bcrypt)

## 📋 Tính Năng

### Bảo Mật
- ✅ **Mật khẩu băm đa lớp**: MD5, SHA-256, Bcrypt
- ✅ **Xác thực 2 lớp (2FA)**: OTP qua email
- ✅ **Session management**: Secure cookies, HttpOnly, SameSite
- ✅ **Password strength validation**: Kiểm tra độ mạnh mật khẩu
- ✅ **SQL Injection protection**: Parameterized queries
- ✅ **XSS protection**: Input sanitization

### Chức Năng
- 📝 Đăng ký tài khoản
- 🔑 Đăng nhập với OTP
- 👤 Quản lý hồ sơ
- 🔒 Đổi mật khẩu
- 📊 Dashboard người dùng
- 📧 Gửi OTP qua email

## 🚀 Cài Đặt

### 1. Cài đặt Python packages

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. Chạy ứng dụng

\`\`\`bash
python app.py
\`\`\`

Truy cập: http://localhost:5000

## 📁 Cấu Trúc Project

```
secure-auth-app/
├── app.py                 # Main application
├── database.py            # Database operations
├── auth.py               # Authentication logic
├── email_service.py      # Email OTP service
├── utils.py              # Utility functions
├── requirements.txt      # Python dependencies
├── README.md            # Documentation
├── templates/           # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── verify_otp.html
│   ├── dashboard.html
│   ├── profile.html
│   ├── security.html
│   ├── 404.html
│   └── 500.html
└── static/              # Static files
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## 🔐 Thuật Toán Băm Mật Khẩu

### 1. MD5 (Message Digest 5)
- **Độ dài**: 128-bit (32 ký tự hex)
- **Tốc độ**: Rất nhanh
- **Bảo mật**: ❌ Không an toàn (dễ bị brute force)
- **Sử dụng**: Chỉ để demo, không dùng trong production

### 2. SHA-256 (Secure Hash Algorithm)
- **Độ dài**: 256-bit (64 ký tự hex)
- **Tốc độ**: Nhanh
- **Bảo mật**: ⚠️ Tốt hơn MD5 nhưng vẫn có thể bị tấn công
- **Sử dụng**: Có thể dùng với salt

### 3. Bcrypt (Blowfish Crypt)
- **Độ dài**: 60 ký tự
- **Tốc độ**: Chậm (có thể điều chỉnh)
- **Bảo mật**: ✅ Rất an toàn (có salt tự động, cost factor)
- **Sử dụng**: **Khuyến nghị cho production**

## 📱 Xác Thực 2 Lớp (2FA) với OTP

### Quy Trình
1. User nhập email & password
2. Hệ thống xác thực thông tin
3. Tạo mã OTP 6 chữ số ngẫu nhiên
4. Gửi OTP qua email
5. User nhập OTP để hoàn tất đăng nhập
6. OTP có hiệu lực 5 phút

### Bảo Mật OTP
- ✅ Mã ngẫu nhiên 6 chữ số
- ✅ Thời gian hết hạn 5 phút
- ✅ Chỉ sử dụng 1 lần
- ✅ Lưu trữ an toàn trong database

## 🛡️ Các Biện Pháp Bảo Mật

### 1. Password Security
- Minimum 8 ký tự
- Yêu cầu chữ hoa, chữ thường, số, ký tự đặc biệt
- Băm với Bcrypt (cost factor 12)
- Không lưu plain text

### 2. Session Security
- Secure cookies (HTTPS only)
- HttpOnly flag (chống XSS)
- SameSite protection (chống CSRF)
- Session timeout 30 phút

### 3. Database Security
- Parameterized queries (chống SQL Injection)
- Password hashing
- Secure connection

### 4. Input Validation
- Email format validation
- Password strength checking
- XSS protection
- CSRF protection

## 📊 Database Schema

### Table: users
\`\`\`sql
- id (INTEGER PRIMARY KEY)
- username (TEXT UNIQUE)
- email (TEXT UNIQUE)
- phone (TEXT)
- password_hash (TEXT) -- Bcrypt
- password_md5 (TEXT) -- MD5 (demo)
- password_sha256 (TEXT) -- SHA-256 (demo)
- created_at (TIMESTAMP)
- last_login (TIMESTAMP)
- is_active (BOOLEAN)
\`\`\`

### Table: otp_codes
\`\`\`sql
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER FOREIGN KEY)
- otp_code (TEXT)
- created_at (TIMESTAMP)
- expires_at (TIMESTAMP)
- is_used (BOOLEAN)
\`\`\`

### Table: login_history
\`\`\`sql
- id (INTEGER PRIMARY KEY)
- user_id (INTEGER FOREIGN KEY)
- login_time (TIMESTAMP)
- ip_address (TEXT)
- user_agent (TEXT)
- status (TEXT)
\`\`\`

## 🎨 Giao Diện

- **Design**: Modern, gradient, responsive
- **Colors**: Purple gradient (#667eea → #764ba2)
- **Framework**: Custom CSS (không dùng Bootstrap/Tailwind)
- **Icons**: Unicode emoji
- **Animations**: Smooth transitions

## 🧪 Testing

### Test Cases
1. ✅ Đăng ký với mật khẩu yếu → Reject
2. ✅ Đăng ký với email trùng → Reject
3. ✅ Đăng nhập sai password → Reject
4. ✅ Đăng nhập đúng → Gửi OTP
5. ✅ Nhập OTP sai → Reject
6. ✅ Nhập OTP đúng → Success
7. ✅ OTP hết hạn → Reject
8. ✅ Đổi mật khẩu → Success

## 🔧 Mở Rộng

### Tính Năng Có Thể Thêm
- [ ] OTP qua SMS (Twilio)
- [ ] OAuth (Google, Facebook)
- [ ] Biometric authentication
- [ ] Password reset via email
- [ ] Account lockout after failed attempts
- [ ] Login history tracking
- [ ] Admin dashboard
- [ ] User roles & permissions
- [ ] API endpoints (REST/GraphQL)
- [ ] Mobile app (React Native)

## 📚 Tài Liệu Tham Khảo

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bcrypt](https://github.com/pyca/bcrypt/)
- [OWASP Password Storage](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)
- [Two-Factor Authentication](https://www.twilio.com/docs/verify/2fa)

## 👨‍💻 Tác Giả

Đồ án Bảo Mật An Ninh Thông Tin

**⚠️ Disclaimer**: Đây là project học tập. Trong production, cần thêm nhiều biện pháp bảo mật khác.
\`\`\`
