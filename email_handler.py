import smtplib, ssl
import config
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send(recipient, subject, message):
    print("1")
    port = config.gmail["port"]
    smtp_server = config.gmail["smtp_server"]
    sender_email = config.gmail["address"]
    password = config.gmail["password"]
    
    print("1")
    MIMEmessage = MIMEMultipart("alternative")
    MIMEmessage["Subject"] = subject
    MIMEmessage["From"] = sender_email
    MIMEmessage["To"] = recipient

    print("1")
    html = """\
    <html>
      <body>
      {}
      </body>
    </html>
    """.format(message)
    part1 = MIMEText(html, "html")
    MIMEmessage.attach(part1)

    print("3")
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()
        print("a1")
        server.starttls()
        print("a3")
        server.login(sender_email, password)
        print("a4")
        server.sendmail(sender_email, recipient, MIMEmessage.as_string())
        print("a5")
        server.quit()
send("pisu.maru@gmail.com", "sgg", "asdfsasdf")