import smtplib, ssl
from email.message import EmailMessage

with open('password.txt', 'r') as f:
    user = f.read()
    password = f.read()

msg = EmailMessage()
msg.set_content("TEST")
msg["Subject"] = "TEST"
msg["From"] = user
msg["To"] = "justfortesting951@spaml.de"

context=ssl.create_default_context()

with smtplib.SMTP("mail.privateemail.com:587") as smtp:
    smtp.starttls(context=context)
    smtp.login(user, password)
    smtp.send_message(msg)
