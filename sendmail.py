from config import Email
import smtplib
from email.mime.text import MIMEText
from email.header import Header

def _format_msg(s,success):
    assert type(s) is str
    msg = MIMEText(s,'plain','utf-8')
    if success:
        msg['Subject'] = Header('驿动上传成功','utf-8').encode()
    else:
        msg['Subject'] = Header('驿动上传报错', 'utf-8').encode()
    return msg

def sendmail(s=None, success=True,to_addr=Email.to_addr):
    msg = _format_msg(s,success)
    server = smtplib.SMTP(Email.smtp_server, Email.smtp_port)
    server.set_debuglevel(1)
    server.starttls()
    server.login(Email.from_addr, Email.password)
    server.sendmail(Email.from_addr, [to_addr], msg.as_string())
    server.quit()
