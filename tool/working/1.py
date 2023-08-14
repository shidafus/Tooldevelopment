# 导入模块
import itchat, sys

# 获取登陆二维码
itchat.auto_login(enableCmdQR=True)
# 获取自己的微信号
self_name = itchat.get_friends()[0]['UserName']
# 发送消息
itchat.send('Hello, 微信！', toUserName=self_name)
# 获取最近聊天记录
chat_logs = itchat.get_chatrooms(update=True)[0]['MemberList']
# 获取好友信息
friend_infos = itchat.search_friends(name='我的好友')
