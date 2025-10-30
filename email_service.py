"""
Email Service
Gửi OTP qua email
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os

load_dotenv()

class EmailService:
    def __init__(self):
        # Cấu hình email - Thay đổi thông tin này
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', os.getenv('EMAIL'))
        self.sender_password = os.getenv('SENDER_PASSWORD', os.getenv('PASSWORD'))
        self.sender_name = 'Secure Auth System'
    
    def send_otp_email(self, recipient_email, username, otp_code):
        """Gửi mã OTP qua email"""
        try:
            # Tạo email
            message = MIMEMultipart('alternative')
            message['Subject'] = f'Mã OTP đăng nhập - {otp_code}'
            message['From'] = f'{self.sender_name} <{self.sender_email}>'
            message['To'] = recipient_email
            
            # Nội dung email HTML
            html_content = f'''
            <!DOCTYPE html>
            <html>
            <head>
                <style>
                    body {{
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                        background-color: #f4f4f4;
                        margin: 0;
                        padding: 0;
                    }}
                    .container {{
                        max-width: 600px;
                        margin: 40px auto;
                        background-color: #ffffff;
                        border-radius: 10px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                        overflow: hidden;
                    }}
                    .header {{
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        color: white;
                        padding: 30px;
                        text-align: center;
                    }}
                    .header h1 {{
                        margin: 0;
                        font-size: 24px;
                    }}
                    .content {{
                        padding: 40px 30px;
                    }}
                    .otp-box {{
                        background-color: #f8f9fa;
                        border: 2px dashed #667eea;
                        border-radius: 8px;
                        padding: 20px;
                        text-align: center;
                        margin: 30px 0;
                    }}
                    .otp-code {{
                        font-size: 36px;
                        font-weight: bold;
                        color: #667eea;
                        letter-spacing: 8px;
                        margin: 10px 0;
                    }}
                    .warning {{
                        background-color: #fff3cd;
                        border-left: 4px solid #ffc107;
                        padding: 15px;
                        margin: 20px 0;
                        border-radius: 4px;
                    }}
                    .footer {{
                        background-color: #f8f9fa;
                        padding: 20px;
                        text-align: center;
                        color: #6c757d;
                        font-size: 14px;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🔐 Xác Thực Đăng Nhập</h1>
                    </div>
                    <div class="content">
                        <p>Xin chào <strong>{username}</strong>,</p>
                        <p>Bạn đã yêu cầu đăng nhập vào hệ thống. Đây là mã OTP của bạn:</p>
                        
                        <div class="otp-box">
                            <p style="margin: 0; color: #6c757d;">Mã OTP của bạn</p>
                            <div class="otp-code">{otp_code}</div>
                            <p style="margin: 0; color: #6c757d; font-size: 14px;">Có hiệu lực trong 5 phút</p>
                        </div>
                        
                        <div class="warning">
                            <strong>⚠️ Lưu ý bảo mật:</strong>
                            <ul style="margin: 10px 0 0 0; padding-left: 20px;">
                                <li>Không chia sẻ mã này với bất kỳ ai</li>
                                <li>Mã OTP chỉ có hiệu lực trong 5 phút</li>
                                <li>Nếu bạn không yêu cầu đăng nhập, vui lòng bỏ qua email này</li>
                            </ul>
                        </div>
                        
                        <p style="margin-top: 30px;">Trân trọng,<br><strong>Secure Auth System</strong></p>
                    </div>
                    <div class="footer">
                        <p>Email này được gửi tự động, vui lòng không trả lời.</p>
                        <p>© 2025 Secure Auth System. All rights reserved.</p>
                    </div>
                </div>
            </body>
            </html>
            '''
            
            # Attach HTML content
            html_part = MIMEText(html_content, 'html')
            message.attach(html_part)
            
            # Gửi email
            # Chế độ demo: In ra console thay vì gửi thật
            print(f"\n{'='*60}")
            print(f"📧 EMAIL OTP (DEMO MODE)")
            print(f"{'='*60}")
            print(f"To: {recipient_email}")
            print(f"Subject: Mã OTP đăng nhập - {otp_code}")
            print(f"OTP Code: {otp_code}")
            print(f"{'='*60}\n")

            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return True
            
        except Exception as e:
            print(f"❌ Lỗi gửi email: {str(e)}")
            return False
