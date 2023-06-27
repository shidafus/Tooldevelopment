import smtplib
from email.mime.text import MIMEText
import markdown2

# 定义一些固定的信息
fixed_information = {
    "host": "smtp.163.com",
    "port": 25,
    "from_addr": "zjh13320020268@163.com",
    "email_passwd": "MZFOKBGIGZLJMYQN",
}


body = """ 黄河之水天上来 """
email_subject = """ 运维告警通知 """
mail_recipient = ["zjh13320020268@163.com", "641974154@qq.com"]

# 定义消息模板
messages = {
    "主题": email_subject,                                    # 后期写一个变量
    "正文": body,                                             # 后期做成一个变量
    "收件人": mail_recipient                                   # 后期写一个变量
}

#
# def Initialize_mail(body, email_subject, mail_recipient):
#     messages = {
#         "主题": email_subject,  # 后期写一个变量
#         "正文": body,  # 后期做成一个变量
#         "收件人": mail_recipient  # 后期写一个变量
#     }
#     return messages

# 吧文本转化成一个html格式的页面
html = markdown2.markdown(body)


def send_mail(message):
    msg = MIMEText(html, _subtype='html', _charset='UTF-8')
    # msg = MIMEText(message["正文"], 'plain', 'utf-8')
    msg['subject'] = message['主题']

    server = smtplib.SMTP(fixed_information["host"], fixed_information["port"])
    server.starttls()
    server.login(fixed_information["from_addr"], fixed_information["email_passwd"])
    result = server.sendmail(fixed_information["from_addr"], message["收件人"], msg.as_string())

    if not result:
        print("邮件发送成功!")
    else:
        print("邮件发送失败!")
    server.quit()


send_mail(messages)
