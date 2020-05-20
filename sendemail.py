import smtplib

gmail_user = 'REPLACE WITH GMAIL BOT ADDRESS'
gmail_password = 'REPLACE WITH GMAIL BOT PASSWORD'

receiver = 'REPLACE WITH RECEIVER EMAIL ADDRESS'

message = """\
Subject: Gradebook update

"""

def send_email(content):
	s = smtplib.SMTP('smtp.gmail.com', 587)

	# start TLS for security
	s.starttls()

	# Authentication
	s.login(gmail_user, gmail_password)

	# sending the mail
	msg = message + content
	s.sendmail(gmail_user, receiver, msg)

	# terminating the session
	s.quit()
