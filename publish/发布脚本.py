from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
import time,sys

env.hosts = ['192.168.11.130']
env.user = 'root'
env.port = '22'
env.password = '1qaz2WSX'

env.project_dev_source = r'D:\\Ubuntu\database'  # 开发机项目主目录
env.project_tar_source = r'D:\\Ubuntu\\'  # 开发机项目压缩储存目录
env.project_pack_name = 'release'  # 项目压缩包名前缀, 文件名为release.tar.gz

env.deploy_project_root = '/data/www/shenchan/'  # 生产环境项目的主目录
env.deploy_release_dir = 'release'  # 项目发布目录,位于主目录下面
env.deploy_current_dir = 'current'  # 对外服务的当前版本软连接
env.deploy_version = time.strftime("%Y-%m-%d-%H-%M-%S") + "v2"  # 版本号


@runs_once
def input_versionid():
    return prompt("Please input project rollback version ID:", default="")


@task
@runs_once
def tar_soure():  # 项目打包本地项目主目录,并将压缩包储存到本地压缩包目录
    print(yellow("Creating source package..."))
    os.chdir(env.project_dev_source)
    with lcd(env.project_dev_source):  # 因为是在windows环境似乎是失效了,切换目录
        print(yellow("Packing, please wait patiently..."))
        local("dir")
        local("tar -zcf  %s.tar.gz ./mongo-sharding/*" % (env.project_tar_source + env.project_pack_name))
    print(green("Creating source package success!"))


@task
def put_package():              # 上传任务函数
    print(yellow("Start put package..."))
    with settings(warn_only=True):
        with cd(env.deploy_project_root + env.deploy_release_dir):
            run("mkdir %s" % env.deploy_version)
    env.deploy_full_path = env.deploy_project_root + env.deploy_release_dir + "/" + env.deploy_version

    with settings(warn_only=True):
        result = put(env.project_tar_source  + env.project_pack_name + ".tar.gz", env.deploy_full_path)
    if result.failed and print("put file Failed, Continue[Y/n]?"):
        abort("Aborting file put task!")
    with cd(env.deploy_full_path):
        run("tar -zxvf %s.tar.gz" % env.project_pack_name)
        run("rm -rf %s.tar.gz" %  env.project_pack_name)
    print(green("Put  & untar package success!"))

@task
def make_symlink(): # 为当前版本目录做软连接
    print(yellow("update current symlink"))
    env.deploy_full_path = env.deploy_project_root + env.deploy_release_dir + "/" + env.deploy_version
    with settings(warn_only=True):
        # run("rm -rf %s" % env.deploy_project_root + env.deploy_current_dir)
        run("ln -snf --relative %s/*  %s " % (env.deploy_full_path, env.deploy_project_root + env.deploy_current_dir))
    print(green("make symlink success!"))


@task
def rollback():
    print(yellow("rollback project version"))
    versionid = input_versionid()            #获取用户输入的回滚版本号
    if versionid == '':
        abort("Project version ID errot, abort!")
    env.deploy_full_path = env.deploy_project_root + env.deploy_release_dir + "/" + versionid
    # run("rm -rf %s " % env.deploy_project_root + env.deploy_release_dir)
    run("ln -snf --relative %s/* %s " % (env.deploy_full_path, env.deploy_project_root + env.deploy_current_dir))    #删除软连接,重新创建并指定软连接目录,新版生效
    print(green("rollback succress!"))


@task
def go():
    # 保存执行记录到本地
    with open('../execute.txt', 'a', encoding='utf-8') as f:
        # sys.stdout = f  # 输出重定向到文件中 关闭状态
        select = input("You want to publish or roll back! (P/R)")
        if select == 'P':
            tar_soure()
            execute(put_package, hosts=env.hosts)
            execute(make_symlink, hosts=env.hosts)
        elif select == 'R':
            execute(rollback, hosts=env.hosts)
        else:
            print("你的输入有误!")


if __name__ == '__main__':
    go()

