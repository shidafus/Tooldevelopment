from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *


env.roledefs = {
    'test-kf1': ['192.168.11.109'], 'prod-kf1': ['192.168.101.131'],
    'test-kf2': ['192.168.11.120'], 'prod-kf2': ['192.168.101.100'],
}


env.user = 'root'

port = {
    '192.168.11.109': '22',
    '192.168.11.120': '22',
    '192.168.101.131': '2222',
    '192.168.101.100': '2223',
}

env.passwords = {
    'root@192.168.11.109:22': '1qaz2WSX',
    'root@192.168.11.120:22': '1qaz2WSX',
    'root@192.168.101.131:22': 'Szyw!2022',
    'root@192.168.101.100:22': 'Szyw!2022',

}

env.test_kf_109_project_test_source = '/data/docker/kefu'  # 开发机项目主目录
env.test_kf_109_project_jar_source = '/data/docker/kefu/webapps/'  # 开发机项目jar包目录
env.test_kf_109_project_jar_pack_name = 'kefuServer.jar'  # jar包名称
local_kf_109_jar_path = r'/tmp/publish'  # 109 kf jar包保存本地路径

env.deploy_kf_project_root = '/data/docker/kefu'  # 生产环境项目的主目录
env.deploy_kf_release_dir = '/data/docker/kefu/webapps/'  # 生产机项目jar包目录
env.deploy_kf_project_jar_pack_name = 'kefuServer.jar'  # jar包名称

test = input("你要发布什么？")

tkf = "test" + "-" + test
pkf = "prod" + "-" + test


@roles(tkf)
def get_jar():
    env.port=port[env.host_string]
    print(yellow("Pull the jar package of kf..."))
    local(f"rm -rf  {local_kf_109_jar_path}/* ")
    # with settings(warn_only=True):
    get((env.test_kf_109_project_jar_source + env.test_kf_109_project_jar_pack_name), local_kf_109_jar_path)
    print(green("Download successfully ..."))


@roles(pkf)
def put_jar():
    env.port = port[env.host_string]
    env.host_string = '127.0.0.1'
    print(yellow("Start uploading to kf_131..."))
    with settings(warn_only=True):
        with cd(env.deploy_kf_release_dir):
            run(f"mv {env.deploy_kf_project_jar_pack_name} {env.deploy_kf_project_jar_pack_name}.`date +%Y-%m-%d-%H-%M-%S`")
            result = put((local_kf_109_jar_path + "/" + env.test_kf_109_project_jar_pack_name),
                         env.deploy_kf_release_dir)
            if result.failed and print("put file Failed, Continue[Y/n]?"):
                abort("Aborting file put task!")
            else:
                print(green("Put file successfully ..."))
            with cd(env.deploy_kf_project_root):
                print("Restart KF...")
                run("docker-compose down && docker-compose up -d")
                print(green("Release success..."))

@task
def delpoy():
    execute(get_jar)
    execute(put_jar)
