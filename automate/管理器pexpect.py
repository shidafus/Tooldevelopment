import pexpect

PROMPT = ['#', '>>>', '>', '\\$']


def send_command(child, cmd, timeout=3600):  # 传递命令
    child.sendline(cmd)
    child.expect(PROMPT, timeout=timeout)  # 期望获得的命令提示符
    print(child.before)  # 打印从SSH会话得到的结果


def connect(user, host, password):
    ssh_newkeys = "Are you sure you want to continue connecting"
    connstr = 'ssh ' + user + '@' + host
    child = pexpect.spawn(connstr, encoding='utf-8', logfile=open(r'file.html', 'w', encoding='utf-8'))  # 实例化连接
    ret = child.expect([pexpect.TIMEOUT, ssh_newkeys, '[P|p]assword:'])  # 捕获 ssh_newkeys
    if ret == 0:  # 判断捕获的信息
        print('[-] Error Connecting')
        return
    if ret == 1:  # 捕获了ssh_newkey的消息
        child.sendline('yes')  # 发送yes
        ret = child.expect([pexpect.TIMEOUT, ssh_newkeys, '[P|p]assword:'])
        if ret == 0:
            print('[-] Error Connecting')
            return
    child.sendline(password)
    child.expect(PROMPT)  # 捕获命令提示符
    return child


def main():
    host = "192.168.11.24"
    user = "root"
    password = "root"
    child = connect(user, host, password)
    # 打包数据
    send_command(child, '/bin/bash -c "tar -zcf  /root/docker-file.tar.gz -C /root docker-file"',
                 timeout=1800)  # 这里不能使用$PWD有点问题,可能是不兼容


if __name__ == '__main__':
    main()
