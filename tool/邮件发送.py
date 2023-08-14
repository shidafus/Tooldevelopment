import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import markdown2


class OutgoingMailInterface:

    def __init__(self, from_addr, email_passwd, mail_recipient, subject, body):
        self.fixed_information = {
            "host": "smtp.163.com",
            "port": 25,
            "from_addr": from_addr,
            "email_passwd": email_passwd,
        }
        self.body = body
        self.email_subject = subject
        self.mail_recipient = mail_recipient
        self.message = {
            "主题": self.email_subject,
            "正文": self.body,
            "收件人": self.mail_recipient,
        }

    def html_conversion(self):
        html_text = markdown2.markdown(self.body)
        return html_text

    def send_mail(self, attachment_path=None):
        msg = MIMEMultipart()
        msg.attach(MIMEText(self.html_conversion(), _subtype='html', _charset='UTF-8'))
        msg['subject'] = self.message['主题']

        if attachment_path:
            filename = attachment_path.split("/")[-1]
            with open(attachment_path, mode="rb", encoding='utf-8') as attachment:
                attach_part = MIMEApplication(attachment.read(), Name=filename)
                attach_part["Content-Disposition"] = f'attachment; filename="{filename}"'
                msg.attach(attach_part)

        try:
            server = smtplib.SMTP(self.fixed_information["host"], self.fixed_information["port"])
            server.starttls()
            server.login(self.fixed_information["from_addr"], self.fixed_information["email_passwd"])
            result = server.sendmail(self.fixed_information["from_addr"], self.message["收件人"], msg.as_string())
            server.quit()

            if not result:
                print("邮件发送成功!")
            else:
                print("邮件发送失败!")
        except Exception as e:
            print("发送邮件时出现错误:", str(e))


if __name__ == "__main__":
    from_addr = "zjh13320020268@163.com"
    email_passwd = "MZFOKBGIGZLJMYQN"
    mail_recipient = ["zjh13320020268@163.com"]
    email_subject = "运维告警通知"
    email_body = "黄河之水天上来"
    attachment_path = "/home/kali/list.txt"

    one = OutgoingMailInterface(from_addr, email_passwd, mail_recipient, email_subject, email_body)
    one.send_mail(attachment_path)
