import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from config import PROF_MAIL, WORK_MAIL_LOGIN, WORK_MAIL_PASSWORD, ZHOZH_MAIL


def send_email(mail_text: str, filename: str) -> bool:
    try:
        message = MIMEMultipart()
        message["Subject"] = "TEST PROF MAIL"
        message["From"] = WORK_MAIL_LOGIN
        message["To"] = ZHOZH_MAIL

        message.attach(MIMEText(mail_text, "plain"))

        with open(filename, "rb") as attachment:
            
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            
            part.add_header("Content-Disposition", f"attachment; filename= {filename}")
            
            message.attach(part)

        text = message.as_string()
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(WORK_MAIL_LOGIN, WORK_MAIL_PASSWORD )
            server.sendmail(WORK_MAIL_LOGIN, ZHOZH_MAIL, text)
        
        return True
    except:
        return False
