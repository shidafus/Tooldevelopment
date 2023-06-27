import os
import subprocess

def menu():
    print("-------------------请选择要打开的程序----------------------")
    print("                   1. cmd 终端                           ")
    print("                   2. redisDesk                         ")
    print("                   3. xshell                            ")
    print("                   4. 内网通                             ")
    print("                   5. wps                               ")
    print("                   6. 钉钉                               ")
    print("                   7. 浏览器                             ")
    print("                   8. navicat                           ")
    print("                   9. postman                           ")
    print("                   10.VMware                            ")
    print("                   11.Foxmail                           ")
    print("                   12.OpenVPN                           ")
    print("                   13.PyCharm                           ")
    print("                   14.任务管理器                           ")
    print("                   15. 退出                             ")

switchs = {
    '1': r'cmd.exe',
    '2': r'E:\redis\RESP_app\resp.exe',
    '3': r'D:\xshell\Xshell 6\Xshell.exe',
    '4': r'D:\app\Nwt\ShiYeLine.exe',
    '5': r'D:\wps\WPS Office\ksolaunch.exe',
    '6': r'D:\DingTalk\DingDing\DingtalkLauncher.exe',
    '7': r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '8': r'D:\Navicat Premium 15\Navicat Premium 15\navicat.exe',
    '9': r'C:\Users\Administrator\AppData\Local\Postman\Postman.exe',
    '10': r'D:\VMware\vmware.exe',
    '11': r'D:\Program Files\Foxmail 7.2\Foxmail.exe',
    '12': r'C:\Program Files\OpenVPN\bin\openvpn-gui.exe',
    '13': r'E:\PyCharm\PyCharm 2023.1.2\bin\pycharm64.exe',
    '14': r'taskmgr.exe'
}

def caozuo(num):
    subprocess.Popen(switchs[num], creationflags=subprocess.CREATE_NEW_CONSOLE)


while True:
    try:
        menu()
        num = input("请输入你的选项:")
        if int(num) <= len(switchs):
            caozuo(num)
            os.system('cls' if os.name == 'nt' else 'clear')
        else:
            break
    except FileNotFoundError:
        print("该程序为安装或者是执行文件错误!\n"*3)