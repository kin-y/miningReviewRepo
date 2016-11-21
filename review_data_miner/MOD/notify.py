import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

class Notify:
    def __init__(self, toaddr, subject):
        self.fromaddr = "notify.xinyang@gmail.com"
        self.toaddr = toaddr
        self.subject = subject
		
        msg = MIMEMultipart()
        msg['From'] = self.fromaddr
        msg['To'] = self.toaddr
        msg['Subject'] = "Task " + self.subject
        body = """
		
		
		************ Note ************ 
		This e-mail has been sent automatically and represents a notification only. Please don't reply because your message will not be read.
		"""
        msg.attach(MIMEText(body, 'plain')) 
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.fromaddr, "100282yx")
        text = msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()
