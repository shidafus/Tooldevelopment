from fabric.api import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
import time, sys

env.roledefs = {
    'test-kf1': ['192.168.11.109'], 'prod-kf1': ['192.168.101.131'],
    'test-kf2': ['192.168.11.120'], 'prod-kf2': ['192.168.101.100'],
    'test-im1': ['192.168.11.209'], 'prod-im1': ['192.168.101.130'],
    'test-im2': ['192.168.11.100'], 'prod-im2': ['192.168.101.101'],
}

env.user = 'root'
env.port = '22'

env.passwords = {
    'root@192.168.11.109:22': '1qaz2WSX',
    'root@192.168.11.120:22': '1qaz2WSX',
    'root@192.168.11.209:22': '1qaz2WSX',
    'root@192.168.11.100:22': '1qaz2WSX',
    'root@192.168.101.131:22': 'Szyw!2022',
    'root@192.168.101.100:22': 'Szyw!2022',
    'root@192.168.101.130:22': 'Szyw!2022',
    'root@192.168.101.101:22': 'Szyw!2022'
}

env.test_kf_109_project_test_source = '/data/docker/kefu'  # 开发机项目主目录
env.test_kf_109_project_jar_source = '/data/docker/kefu/webapps/'  # 开发机项目jar包目录
env.test_kf_109_project_jar_pack_name = 'kefuServer.jar'  # jar包名称
local_kf_109_jar_path = r'D:\Ubuntu\publish\kf_109'  # 109 kf jar包保存本地路径

env.deploy_kf_project_root = '/tmp/kefu'  # 生产环境项目的主目录
env.deploy_kf_release_dir = '/tmp/kefu/webapps/'  # 生产机项目jar包目录
env.deploy_kf_project_jar_pack_name = 'kefuServer.jar'  # jar包名称

test = input("你要发布什么？")

tkf = "test" + "-" + test
pkf = "prod" + "-" + test


@roles(tkf)
def get_jar():
    print(yellow("Pull the jar package of kf..."))
    local(f"del {local_kf_109_jar_path}\\{env.deploy_kf_project_jar_pack_name} ")
    # with settings(warn_only=True):
    get((env.test_kf_109_project_jar_source + env.test_kf_109_project_jar_pack_name), local_kf_109_jar_path)
    print(green("Download successfully ..."))


@roles(pkf)
def put_jar():
    print(yellow("Start uploading to kf_131..."))
    with settings(warn_only=True):
        with cd(env.deploy_kf_release_dir):
            run(f"mv {env.deploy_kf_project_jar_pack_name} {env.deploy_kf_project_jar_pack_name}.`date +%Y-%m-%d-%H-%M-%S`")
            result = put((local_kf_109_jar_path + "\\" + env.test_kf_109_project_jar_pack_name),
                         env.deploy_kf_release_dir)
            if result.failed and print("put file Failed, Continue[Y/n]?"):
                abort("Aborting file put task!")
            # print("Restart kf...")
            # run(f"docker-composer -f {env.deploy_kf_project_root}/docker-compose.yml up -d")


def delpoy():
    execute(get_jar)
    execute(put_jar)


if __name__ == "__main__":
    delpoy()
