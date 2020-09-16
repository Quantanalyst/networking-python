# import SMTP library that enables you to connect to an email account
# and use SMTP protocol to send an email
import smtplib
import os

from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import COMMASPACE, formatdate



# create a mailing server, use your email provider SMTP server and the port that you want to use.
# For port, 25 is the default SMTP non-encrypted port.
# However, use other encrypted ports like 465 and 587
# For gmail, the server is "smtp.gmail.com"
server = smtplib.SMTP("mail.privateemail.com:587")

server.set_debuglevel(1)
# start the server
server.ehlo()
server.starttls()
server.ehlo()

with open('password.txt', 'r') as f:
    user = f.read()
    password = f.read()

server.login(user,password)

# Use MIMEMultipart to assign different parts of the email, e.g. from, to, subject, ...
msg = MIMEMultipart()
msg['From'] = 'Saeed Mohajeryami'
msg['To'] = 'justfortesting951@spaml.de'
msg['Subject'] = 'Just another test'

with open('message.txt', 'r') as f:
    message = f.read()

# add a message to the body of the email
msg.attach(MIMEText(message,'plain'))

# save your image name in a variable
filename = 'elasticbeanstalk.png'

# make sure that you have opened the file in a binary read mode
# it's not a text, it's an image and it must be read as a binary
attachment = open(filename, 'rb')

# create a payload
payload = MIMEBase('application','octet-stream')
payload.set_payload(attachment.read())

encoders.encode_base64(payload)
payload.add_header('Content-Disposition', f'attachment; filename={filename}')
msg.attach(payload)

text = msg.as_string()
server.sendmail(user,'justfortesting951@spaml.de', text)

server.quit()