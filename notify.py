import smtplib
import ssl
from email.message import EmailMessage


class EmailNotifier:
    def __init__(self, smtp_server="10thframe.com", port=587, sender_email="overwatch@10thframe.com",
                 password="Nigh1tcrawler"):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password
        self.receiver_email = '"brian@10thframe.com", "6507404848@txt.att.net"'
        self.message = EmailMessage()
        #self.message['Subject'] = 'PlexPing Alert'
        self.message['From'] = sender_email
        # self.message['To'] = 'brian@10thframe.com'
        self.message['To'] = self.receiver_email
        self.message.preamble = 'You will not see this in a MIME-aware mail reader.\n'
        self.message.set_content("Another test from python")

    def set_recipients(self, recipients):
        self.receiver_email = recipients

    def set_subject(self, subject):
        self.message['Subject'] = subject

    def set_content(self, content):
        self.message.set_content(content)

    def notify(self, m, subject='PlexPing Alert'):
        context = ssl.create_default_context()
        # Try to log in to server and send email
        server = None
        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.ehlo()  # Can be omitted
            server.starttls(context=context)  # Secure the connection
            server.ehlo()  # Can be omitted
            server.login(self.sender_email, self.password)
            # TODO: Send email here
            self.set_subject(subject)
            self.set_content(m)
            server.send_message(self.message)
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            if server is not None:
                server.quit()


class EmailNotifierDebug(EmailNotifier):
    def __init__(self, smtp_server="localhost", port=1025, sender_email="overwatch@10thframe.com",
                 password="Nigh1tcrawler"):
        super(EmailNotifierDebug, self).__init__(smtp_server, port, sender_email, password)

    def notify(self, m, subject='PlexPing Alert'):
        # Try to log in to server and send email
        server = None
        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            # TODO: Send email here
            self.set_subject(subject)
            self.set_content(m)
            server.send_message(self.message)
        except Exception as e:
            # Print any error messages to stdout
            print(e)
        finally:
            if server is not None:
                server.quit()


def notify(msg, subj):
    em = EmailNotifier()
    # em = EmailNotifierDebug()
    em.notify(msg, subj)


'''
email_cfg = {
    "smtp_server": "10thframe.com",
    "port": 587,    # For starttls
    "sender_email": "overwatch@10thframe.com",
    "password": "Nigh1tcrawler"
}

smtp_server = "10thframe.com"
# smtp_server = "localhost"
# port = 465  # For SSL
# port = 1025  # For SSL
port = 587  # For starttls
# password = input("Type your password and press enter: ")
password = "Nigh1tcrawler"
# Create a secure SSL context
context = ssl.create_default_context()

sender_email = "overwatch@10thframe.com"
receiver_email = "brian@10thframe.com"
# receiver_email = "byuchino@gmail.com"
message = """\
Subject: Hi there

This message was sent from python."""

# msg = MIMEText('This is a test email')
msg = EmailMessage()

msg['Subject'] = 'Test mail'
msg['From'] = 'overwatch@10thframe.com'
msg['To'] = 'brian@10thframe.com'
#msg['To'] = 'byuchino@gmail.com'
msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
msg.set_content("Another test from python")

def notify_old(m):
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        # server.login("my@gmail.com", password)
        # TODO: Send email here
        server.sendmail(sender_email, receiver_email, msg.as_string())


def notify_new(m):
    # Create a secure SSL context
    context = ssl.create_default_context()

    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtp_server, port)
        server.ehlo()  # Can be omitted
        server.starttls(context=context)  # Secure the connection
        server.ehlo()  # Can be omitted
        server.login(sender_email, password)
        # TODO: Send email here
        # server.sendmail(sender_email, receiver_email, message)
        server.send_message(msg)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()
'''
