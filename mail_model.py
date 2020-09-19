import smtplib
import os
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from config import WORK_MAIL_LOGIN, WORK_MAIL_PASSWORD


def attach_file(msg: str, filepath: str) -> None:
    filename = os.path.basename(filepath)
    ctype, encoding = mimetypes.guess_type(filepath)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        with open(filepath) as fp:
            file = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'image':
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
    elif maintype == 'audio':
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
    else:
        with open(filepath, 'rb') as fp:
            file = MIMEBase(maintype, subtype)
            file.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(file)
    file.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(file)


def send_email(addr_to: str, msg_subj: str, msg_text: str, file: str = None) -> bool:
    #try:
    addr_from = WORK_MAIL_LOGIN
    password  = WORK_MAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From']    = addr_from
    msg['To']      = addr_to
    msg['Subject'] = msg_subj

    body = msg_text
    msg.attach(MIMEText(body, 'plain'))

    #process_attachement(msg, files)
    if file:
        attach_file(msg, file)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    #server.starttls()
    #server.set_debuglevel(True)
    server.login(addr_from, password)
    server.send_message(msg)
    server.quit()
    return True
    # except:
    #     return False


#send_email("zhozhpost@gmail.com", "subj", "text")