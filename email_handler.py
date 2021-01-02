import smtplib, ssl
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send(recipient, subject, message):
    port = config.gmail["port"]
    smtp_server = config.gmail["smtp_server"]
    sender_email = config.gmail["address"]
    password = config.gmail["password"]
    
    MIMEmessage = MIMEMultipart("alternative")
    MIMEmessage["Subject"] = subject
    MIMEmessage["From"] = sender_email
    MIMEmessage["To"] = recipient

    html = """\
    <html>
      <body>
      {}
      </body>
    </html>
    """.format(message)
    part1 = MIMEText(html, "html")
    MIMEmessage.attach(part1)

    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, recipient, MIMEmessage.as_string())
        server.quit()
