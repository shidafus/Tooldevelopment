# 本脚本批量执行  sed 's/ops ALL=(ALL) NOPASSWD: ALL/ops ALL=(ALL) NOPASSWD: \/bin\/whoami/g' /etc/sudoers  命令
# https://fabric-chs.readthedocs.io/zh_CN/chs/tutorial.html
import time

from fabric.api import *
from fabric.colors import *
from fabric.contrib.files import *
from fabric.contrib.project import *


env.hosts = ['192.168.11.200', '192.168.11.68', '192.168.11.50', '192.168.11.34', '192.168.11.33', '192.168.11.65',
             '192.168.11.32', '192.168.11.35', '192.168.11.63', '192.168.11.132', '192.168.11.17', '192.168.11.130',
             '192.168.11.100', '192.168.11.101', '192.168.11.120', '192.168.11.127', '192.168.11.209', '192.168.11.109',
             '192.168.11.211', '192.168.11.49', '192.168.11.123']
env.user = 'root'
env.port = '22'
env.password = '1qaz2WSX'

env.gateway = '192.168.11.130'
# 剔除某些主机
env.exclude_hosts = ['192.168.11.68', '192.168.11.123']

# 测试环境可以一样的密码,但是生产环境不建议,所以,我们可以吧每个hosts的用户和密码都写好
env.passwords = {
    'root@192.168.11.109:22': '1qaz2WSX'
}

# 通过角色去定义主机组
env.roledefs = {
    'web': ['192.168.11.200', '192.168.11.50', '192.168.11.34', '192.168.11.33', '192.168.11.65', '192.168.11.32',
            '192.168.11.35', '192.168.11.63', '192.168.11.132', '192.168.11.17', '192.168.11.130'],
    'web1': ['192.168.11.100', '192.168.11.101', '192.168.11.120', '192.168.11.127', '192.168.11.209',
             '192.168.11.109', '192.168.11.211', '192.168.11.49']
}

# 指定一些主机给让函数去调用
# @hosts(host1, host2)

# prefix 的作用是在你执行之前在每一个命令前面 加一个workon myvenv  && 接上你run的命令
# with cd('/path/to/app'):
#     with prefix('workon myvenv'):
#         run('./manage.py syncdb')
#         run('./manage.py loaddata myfixture')


# 强制要求任务并行执行,并设置并行数量
# @parallel(pool_size=5)


# @with_settings(warn_only=True)    也可以这么使用 但是个人觉得不好用
@parallel(pool_size=5)
def remote_sed_task():
    print(yellow("Start execution..."))
    with settings(warn_only=True):
        # 备份sudoers文件
        # run(r"cp /etc/sudoers /etc/sudoers.bak")
        # 修改/etc/sudoers文件
        # run(r"sed -i 's/ops ALL=(ALL) NOPASSWD: \/bin\/whoami/ops ALL=(ALL) NOPASSWD: ALL/g' /etc/sudoers")
        run("uname -s")
    print(green("Execution complete..."))


@parallel(pool_size=5)     # 貌似在windows系统上执行有点bug
def check_file():
    with settings(warn_only=True):
        result = exists('./1.txt')
        print(result)
        print(time.thread_time())


def rsync_get():
    rsync_project()


@runs_once
@task
def go():
    execute(remote_sed_task)
    execute(check_file)
