import smtplib
from email.mime.text import MIMEText
from getpass import getpass


def send_email(token):
    msg = MIMEText("http://localhost:8000/accounts/login/req/" + token
                   + "\n 위 주소를 복사+붙여넣기 해주세요")
    msg['Subject'] = '로그인 인증 메일입니다'
    msg['From'] = 'darkdakku@naver.com'
    msg['To'] = 'darkdakku@naver.com'
    password = getpass('Password : ')
    server = smtplib.SMTP("smtp.naver.com", 587)
    server.ehlo()
    server.starttls()
    server.login('darkdakku@naver.com', password)
    server.send_message(msg)
    server.close()

if __name__ == '__main__':
    send_email()
