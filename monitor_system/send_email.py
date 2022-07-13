import smtplib
import ssl
from email.message import EmailMessage


def send_mail(receiver_email, message):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    password = 'bsnqqvkywuvjglgq'

    sender_email = "quocnguyen.testonline@gmail.com"

    # Create a secure SSL context
    context = ssl.create_default_context()

    msg = EmailMessage()
    msg.set_content(message)

    msg['Subject'] = 'Distracted Driver Detection System ALERT'
    msg['From'] = 'Distracted Driver Detection System'
    msg['To'] = receiver_email

    # Send the message via our own SMTP server.
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(sender_email, password)
    server.send_message(msg)
    server.quit()