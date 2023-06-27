from wxpy import *

# 初始化机器人，选择运行环境: ConsoleBot / Bot
bot = Bot()


# 声明监听所有好友对话，并自动处理撤回事件
@bot.register(Friend, TEXT)
def reply_my_friend(msg):
    print(f"收到来自 {msg.sender.name} 的个人信息：{msg.text}")


    return "已成功接受您发送过来的文字~"

# 进入Python REPL(Read-Eval-Print Loop)即可开始交互。

embed()