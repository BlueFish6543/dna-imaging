import smtplib
import os.path
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

USERNAME = "YOUR_EMAIL"
PASSWORD = "YOUR_PASSWORD"

# https://stackoverflow.com/questions/3362600/how-to-send-email-attachments
def send_mail(send_from, send_to, subject, text, file_):
    assert isinstance(send_to, list)

    msg = MIMEMultipart()
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    with open(file_, "rb") as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(file_))
        part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(file_)
        msg.attach(part)

    smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp.login(USERNAME, PASSWORD)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()