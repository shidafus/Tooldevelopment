from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *


test = input("你要发布什么？")

tim = "test" + "-" + test
pim = "prod" + "-" + test

print(" api3   imserver   upload   push  manager")
data = input("具体的服务？")


env.roledefs = {
    'test-im1': ['192.168.11.209'], 'prod-im1': ['192.168.101.130'],
    'test-im2': ['192.168.11.100'], 'prod-im2': ['192.168.101.101'],
}

env.user = 'root'

port = {
    '192.168.11.209': '22',
    '192.168.11.100': '22',
    '192.168.101.130': '2224',
    '192.168.101.101': '2225',
}

env.passwords = {
    'root@192.168.11.209:22': '1qaz2WSX',
    'root@192.168.11.100:22': '1qaz2WSX',
    'root@192.168.101.130:22': 'Szyw!2022',
    'root@192.168.101.101:22': 'Szyw!2022'
}

env.test_im_project_source = '/data/docker'  # 开发机项目主目录
env.test_im_jar_source = f'/data/docker/api2/webapps/'  # 开发机项目jar包目录
local_im_jar_path = r'/tmp/publish'  # im jar包保存本地路径
env.deploy_im_project_source= f'/data/docker/{data}'
env.deploy_im_jar_source = f'/data/docker/{data}/webapps/'  # 开发机项目jar包目录
env.im_jar_packname = ''
if data == "api3":
    env.im_jar_packname = 'webApi.jar'  # 开发机项目jar包目录
elif data == "imserver":
    env.im_jar_packname = 'imServer.jar'  # 开发机项目jar包目录
elif data == "manager":
    env.im_jar_packname = 'im-manager.jar'  # 开发机项目jar包目录
elif data == "push":
    env.im_jar_packname = 'imPush.jar'  # 开发机项目jar包目录



@roles(tim)
def get_jar():
    env.port=port[env.host_string]
    print(yellow("Pull the jar package of im..."))
    local(f"rm  -rf  {local_im_jar_path}/* ")
    # with settings(warn_only=True):
    get((env.deploy_im_jar_source + env.im_jar_packname), local_im_jar_path)
    print(green("Download successfully ..."))


@roles(pim)
def put_jar():
    env.port=port[env.host_string]
    env.host_string = '127.0.0.1'
    print(yellow("Start uploading to im..."))
    with settings(warn_only=True):
        with cd(env.deploy_im_jar_source):
            run(f"mv {env.im_jar_packname} {env.im_jar_packname}.`date +%Y-%m-%d-%H-%M-%S`")
            result = put((local_im_jar_path + "/" + env.im_jar_packname),
                         env.deploy_im_jar_source)
            if result.failed and print("put file Failed, Continue[Y/n]?"):
                abort("Aborting file put task!")
            else:
                print(green("Put file successfully ..."))
            with cd(env.deploy_im_project_source):
                print("Restart IM...")
                run("docker-compose down && docker-compose up -d")
                print(green("Release success..."))

@task
def delpoy():
    execute(get_jar)
    execute(put_jar)

