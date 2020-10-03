import smtplib, ssl, os, mimetypes
#import yagmail

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
    addr_from = ""
    password  = ""

    #msg = MIMEMultipart()
    #msg['From']    = addr_from
    #msg['To']      = addr_to
    #msg['Subject'] = msg_subj

    #body = msg_text
    #msg.attach(MIMEText(body, 'plain'))

    #process_attachement(msg, files)
    if file:
        attach_file(msg, file)
    
    context = ssl.create_default_context()
    msg = "hello"
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        #server.set_debuglevel(True)
        server.login(addr_from, password)
        server.sendmail(addr_from, addr_to, msg)
        #server.quit()
    return True
    # except:
    #     return False


def send_email_20():
    #import smtplib, ssl

    port = 25  # For starttls
    smtp_server = "localhost"
    sender_email = from_addr
    receiver_email = to_addr
    password = password
    message = """\
    Subject: Hi there

    This message is sent from Python."""

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        #server.helo()
        server.ehlo()  # Can be omitted
        #server.starttls(context=context)
        #server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)


def send_email_30():
    server = smtplib.SMTP('smtp.gmail.com', 25)
    #server.connect("smtp.gmail.com", 465)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(login, password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()


def send_mail_40():
    #def sendMail(to, fro, subject, text, files=[],server="localhost"):
    #assert type(to)==list
    #assert type(files)==list


    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    #msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = "hello"

    msg.attach( MIMEText("hey") )

    #for file in files:
    #    part = MIMEBase('application', "octet-stream")
    #    part.set_payload( open(file,"rb").read() )
    #    Encoders.encode_base64(part)
    #    part.add_header('Content-Disposition', 'attachment; filename="%s"'
    #                   % os.path.basename(file))
    #    msg.attach(part)

    smtp = smtplib.SMTP("localhost")
    smtp.sendmail(from_addr, to_addr, msg.as_string() )
    smtp.close()

#send_mail_40()
#send_email_30()
#send_email_20()
send_email("", "subj", "text")
