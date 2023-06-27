import os.path

import paramiko

hostname = '192.168.11.130'
username = 'root'
password = '1qaz2WSX'
#
paramiko.util.log_to_file('syslogin.log')

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
# privatekey = os.path.expanduser(r'C:\Users\zjh13\.ssh\id_rsa')      # 公钥要手动上传
# key = paramiko.RSAKey.from_private_key_file(privatekey)

ssh.connect(hostname=hostname, username=username, password=password)
stdin, stdout, stder = ssh.exec_command('docker ps -a')
print(stdout.read().decode('utf-8'))
# print(stdin.read().decode('utf-8'))
# print(stder.read().decode('utf-8'))
ssh.close()

# t = paramiko.Transport((f"{hostname}", 22))
# t.connect(username=username, password=password)
# sftp = paramiko.SFTPClient.from_transport(t)


# 上传文件到服务器
# put_localpath = r'./邮件发送.py'
# put_remotepath = r'/root/send_mail.back1.py'
# sftp.put(put_localpath, put_remotepath)

# 下载服务器上面文件
# get_localpath = r'./docker-file.tar.gz'
# get_remotepath = r'/root/docker-file.tar.gz'
# sftp.get(get_remotepath, get_localpath)

# 在服务器上创建文件
# sftp.mkdir("/root/ab", mode=777)     # 创建目录的时候权限有点奇怪,不好控制
# sftp.rmdir('/root/ab')               # 删除目录
# sftp.remove()                        # 删除文件
# sftp.rename()                        # 可以给文件或目录重命名
# stat = sftp.stat("/root/pexpect-get.py")    # 只能获取文件的信息,不能获取目录的信息
# stat = sftp.listdir("/root")                # 获取指定目录的列表返回 list的形式
# for i in stat:
#     print(i)

