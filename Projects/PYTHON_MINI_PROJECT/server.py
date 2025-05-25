# from http.server import HTTPServer, SimpleHTTPRequestHandler
# from urllib.parse import parse_qs
# import hashlib
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import random
# import string
# import os
# from config import *

# # In-memory storage for active OTPs
# active_otps = {}

# def generate_otp():
#     return ''.join(random.choices(string.digits, k=6))

# def send_otp_email(receiver_email, otp):
#     msg = MIMEMultipart()
#     msg['From'] = EMAIL_HOST_USER
#     msg['To'] = receiver_email
#     msg['Subject'] = "Your 2FA Verification Code"
    
#     body = f"""
#     Your verification code is: {otp}
    
#     This code will expire in 5 minutes.
#     If you didn't request this code, please ignore this email.
#     """
    
#     msg.attach(MIMEText(body, 'plain'))
    
#     try:
#         server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
#         server.starttls()
#         server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
#         server.send_message(msg)
#         server.quit()
#         return True
#     except Exception as e:
#         print(f"Error sending email: {e}")
#         return False

# class AuthHandler(SimpleHTTPRequestHandler):
#     def do_GET(self):
#         if self.path == '/':
#             self.path = '/templates/login.html'
#         elif self.path == '/register':
#             self.path = '/templates/register.html'
#         elif self.path == '/verify':
#             self.path = '/templates/verify.html'
            
#         try:
#             file_to_open = open(self.path[1:]).read()
#             self.send_response(200)
#             self.send_header('Content-type', 'text/html')
#             self.end_headers()
#             self.wfile.write(bytes(file_to_open, 'utf-8'))
#         except:
#             self.send_error(404)
            
#     def do_POST(self):
#         content_length = int(self.headers['Content-Length'])
#         post_data = self.rfile.read(content_length).decode('utf-8')
#         data = parse_qs(post_data)
        
#         if self.path == '/register':
#             self.handle_registration(data)
#         elif self.path == '/verify':
#             self.handle_verification(data)
#         else:
#             self.send_error(404)
            
#     def handle_registration(self, data):
#         email = data.get('email', [''])[0]
        
#         if not email:
#             self.send_error(400, "Email is required")
#             return
            
#         otp = generate_otp()
#         active_otps[email] = otp
        
#         if send_otp_email(email, otp):
#             self.send_response(302)
#             self.send_header('Location', '/verify')
#             self.end_headers()
#         else:
#             self.send_error(500, "Failed to send verification email")
            
#     def handle_verification(self, data):
#         email = data.get('email', [''])[0]
#         otp = data.get('otp', [''])[0]
        
#         stored_otp = active_otps.get(email)
        
#         if stored_otp and stored_otp == otp:
#             del active_otps[email]  # Remove used OTP
#             self.send_response(200)
#             self.end_headers()
#             self.wfile.write(b"Verification successful!")
#         else:
#             self.send_error(400, "Invalid or expired OTP")

# def run_server():
#     server_address = ('', 8000)
#     httpd = HTTPServer(server_address, AuthHandler)
#     print("Server running on port 8000...")
#     httpd.serve_forever()

# if __name__ == '__main__':
#     run_server()

from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
from urllib.parse import parse_qs
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
import string
import os
from config import *

# In-memory storage for active OTPs
active_otps = {}

class AuthHandler(SimpleHTTPRequestHandler):
    def get_template(self, template_name):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, 'templates', template_name)
        try:
            with open(template_path, 'r', encoding='utf-8') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def do_GET(self):
        if self.path == '/':
            content = self.get_template('login.html')
        elif self.path == '/register':
            content = self.get_template('register.html')
        elif self.path == '/verify':
            content = self.get_template('verify.html')
        else:
            self.send_error(404)
            return

        if content is not None:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        else:
            self.send_error(404)

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        data = parse_qs(post_data)
        
        if self.path == '/login':
            self.handle_login(data)
        elif self.path == '/register':
            self.handle_registration(data)
        elif self.path == '/verify':
            self.handle_verification(data)
        else:
            self.send_error(404)
            
    def handle_login(self, data):
        email = data.get('email', [''])[0]
        if not email:
            self.send_error(400, "Email is required")
            return
            
        # Generate and send OTP
        otp = ''.join(random.choices(string.digits, k=6))
        active_otps[email] = otp
        
        if self.send_otp_email(email, otp):
            self.send_response(302)
            self.send_header('Location', '/verify')
            self.end_headers()
        else:
            self.send_error(500, "Failed to send verification email")

    def handle_registration(self, data):
        email = data.get('email', [''])[0]
        if not email:
            self.send_error(400, "Email is required")
            return
            
        otp = ''.join(random.choices(string.digits, k=6))
        active_otps[email] = otp
        
        if self.send_otp_email(email, otp):
            self.send_response(302)
            self.send_header('Location', '/verify')
            self.end_headers()
        else:
            self.send_error(500, "Failed to send verification email")

    def send_otp_email(self, receiver_email, otp):
        msg = MIMEMultipart()
        msg['From'] = EMAIL_HOST_USER
        msg['To'] = receiver_email
        msg['Subject'] = "Your 2FA Verification Code"
        
        body = f"""
        Your verification code is: {otp}
        
        This code will expire in 5 minutes.
        If you didn't request this code, please ignore this email.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def handle_verification(self, data):
        email = data.get('email', [''])[0]
        otp = data.get('otp', [''])[0]
        
        stored_otp = active_otps.get(email)
        
        if stored_otp and stored_otp == otp:
            del active_otps[email]  # Remove used OTP
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            success_message = """
            <html>
                <body>
                    <h2>Verification Successful!</h2>
                    <p>Your email has been verified.</p>
                    <p><a href="/">Return to login</a></p>
                </body>
            </html>
            """
            self.wfile.write(success_message.encode())
        else:
            self.send_error(400, "Invalid or expired OTP")

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, AuthHandler)
    print("Server running on port 8000...")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()

    #http://localhost:8000/