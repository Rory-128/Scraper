import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import render_template
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import sys

receiver_email = "roryshephard@gmail.com"
test_string = "Competitors Spreadsheet updated see <a href='https://docs.google.com/spreadsheets/d/1b7O4VyzMGNlmx5QRjLpVImpmQWglLDHcKKHVqk_oyjQ/edit?usp=sharing'>Competitors Analysis Spreadsheet!</a><br><br>Don't reply to this email."

report_num = random.randint(1,15)
subject_line = "Competitors Spreadsheet"
subject_line = subject_line + str(random.randint(1,20))  
# Email server code below:
sender_email = 'buzzlist3@gmail.com'
port = 465  # For SSL
smtp_server = "smtp.gmail.com"    
#password = input("Type your password and press enter: ")
password = 'clairerory1'
message = MIMEMultipart("alternative")
message["Subject"] = subject_line
message['From'] = formataddr(('Comps Spreadsheet', sender_email))
message["To"] = receiver_email
text = """\
"""
# Turn these into plain/html MIMEText objects
part1 = MIMEText(text, "plain")
part2 = MIMEText(test_string, "html")

###################################################################################
# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
message.attach(part1)
message.attach(part2)
text = message.as_string()

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, text
    )