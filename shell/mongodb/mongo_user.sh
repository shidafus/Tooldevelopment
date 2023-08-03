#!/bin/bash
#################################################################################################################
##   create_time    : 2023/8/3                                                                                 ##
##   Author         : Ops-DaBao                                                                                ##
##   Mail           : zjh13320020268@163.com                                                                   ##
##   Feature        :  mongodb user                                                                            ##
##   Usage          : When executing the script, you can pass parameters.                                      ##
##                    If you do not pass parameters, the default is used                                       ##
#################################################################################################################


red_color="\033[31m"
green_color="\033[32m"
text_end="\033[0m"
# MongoDB连接信息
HOST=""
longrange="no"
crontainer="mongodb"
# MongoDB的超级管理员信息
ROOT_USER="root"
ROOT_PASS="qwertyuiop"
# 要创建/修改/删除的用户信息
DB_USER=""
DB_USER_PASS=""
DB_USER_ROLE="dbOwner"
DB_USER_DB=""
tip=""



# 创建用户
create_user() {
  if [ ${longrange} == "yes" ]
  then
    mongo --host ${HOST} -p ${PROT} --eval "db = db.getSiblingDB('${DB_USER_DB}'); db.createUser({user: '${DB_USER}', pwd: '${DB_USER_PASS}', roles: [{ role: '${DB_USER_ROLE}', db: '${DB_USER_DB}' }]})"  -u ${ROOT_USER} -p ${ROOT_PASS} --authenticationDatabase admin
  else
    docker exec  ${crontainer} /bin/bash -c "mongo --eval \"db = db.getSiblingDB('${DB_USER_DB}'); db.createUser({user: '${DB_USER}', pwd: '${DB_USER_PASS}', roles: [{ role: '${DB_USER_ROLE}', db: '${DB_USER_DB}' }]})\"  -u ${ROOT_USER} -p ${ROOT_PASS} --authenticationDatabase admin"
  fi
}

# 修改用户密码
change_password() {
  if [ ${longrange} == "yes" ]
  then
    mongo --host ${HOST} -p ${PROT} --eval "db = db.getSiblingDB('${DB_USER_DB}'); db.changeUserPassword( '${DB_USER}', '${DB_USER_PASS}')" -u ${ROOT_USER} -p ${ROOT_PASS} --authenticationDatabase admin
  else
    docker exec  ${crontainer} /bin/bash -c "mongo --eval \"db = db.getSiblingDB('${DB_USER_DB}'); db.changeUserPassword( '${DB_USER}', '${DB_USER_PASS}')\" -u ${ROOT_USER} -p ${ROOT_PASS} --authenticationDatabase admin"
  fi
}

# 删除用户
delete_user() {
  if [ ${longrange} == "yes" ]
  then
    mongo --host ${HOST} -p ${PROT}  --eval "db = db.getSiblingDB('${DB_USER_DB}'); db.dropUser('${DB_USER}')" -u ${ROOT_USER} -p ${ROOT_PASS} --authenticationDatabase admin
  else
    docker exec  ${crontainer} /bin/bash -c "mongo --eval \"db = db.getSiblingDB('${DB_USER_DB}'); db.dropUser('${DB_USER}')\" -u ${ROOT_USER} -p ${ROOT_PASS} --authenticationDatabase admin"
  fi

}

# 修改用户权限
update_user_roles() {
  if [ ${longrange} == "yes" ]
  then
    mongo --host ${HOST} -p ${PROT} --eval "db = db.getSiblingDB('${DB_USER_DB}'); db.updateUser('${DB_USER}', {roles: [{role: '${DB_USER_ROLE}', db: '${DB_USER_DB}'}]})" -u ${ROOT_USER} -p ${ROOT_PASS} --authenticationDatabase admin
  else
    docker exec  ${crontainer} /bin/bash -c "mongo --eval \"db = db.getSiblingDB('${DB_USER_DB}'); db.updateUser('${DB_USER}', {roles: [{role: '${DB_USER_ROLE}', db: '${DB_USER_DB}'}]})\" -u ${ROOT_USER} -p ${ROOT_PASS} --authenticationDatabase admin"
  fi

}

# 获取用户信息
get_user_message() {
  if [ ${longrange} == "yes" ]
  then
    mongo --host ${HOST} -p ${PROT} --eval "db = db.getSiblingDB('${DB_USER_DB}'); db.getUsers()" -u ${ROOT_USER} -p ${ROOT_PASS} --authenticationDatabase admin
  else
    docker exec  ${crontainer} /bin/bash -c "mongo --eval \"db = db.getSiblingDB('${DB_USER_DB}'); db.getUsers()\" -u ${ROOT_USER} -p ${ROOT_PASS} --authenticationDatabase admin"
  fi
}


usage() {
  echo -e "${green_color}脚本使用方法: bash $0 <选项> <参数> ...${text_end}"
  echo -e "${green_color}选项说明:${text_end}"
  echo -e "${green_color} -y    <是否为远程> yes|no (默认为no)${text_end}"
  echo -e "${green_color} -i    <容器名称> （默认为mongodb）${text_end}"
  echo -e "${green_color} -h    <主机地址>:（默认为 127.0.0.1）${text_end}"
  echo -e "${green_color} -P    <端口>:（默认为 27017）${text_end}"
  echo -e "${green_color} -u    <用户名>: 指定查创建的用户名 (默认为空)${text_end}"
  echo -e "${green_color} -p    <密码>: 指定用户名的密码 (默认为空)${text_end}"
  echo -e "${green_color} -d    <数据库名>: 指定数据库名 (默认为空)${text_end}"
  echo -e "${green_color} -t    <创建， 删除， 修改密码， 修改权限， 查看>: create  delete   chanpass  modmission (read readWrite dbAdmin userAdmin clusterAdmin backup restore)  view ${text_end}"
  echo -e "${green_color} -r    <角色> 指定创建用户的角色 (默认为dbOwner)${text_end}"
  exit 1
}

# 检查是否有参数传递，如果有则覆盖默认值
while getopts ":y:i:h:P:u:p:d:t:r:" opt; do
	case $opt in
	  y) longrange="$OPTARG";;
	  i) crontainer="$OPTARG";;
	  h) HOST="$OPTARG";;
	  P) PROT="$OPTARG";;
	  u) DB_USER="$OPTARG";;
	  p) DB_USER_PASS="$OPTARG";;
	  d) DB_USER_DB="$OPTARG";;
	  t) tip="$OPTARG";;
	  r) DB_USER_ROLE="$OPTARG";;
	  *) echo "参数传入有误: -$OPTARG"; usage;;
	esac
done


case $tip in
    create)
      create_user;
      ;;
    delete)
      delete_user;
      ;;
    chanpass)
      change_password;
      ;;
    modmission)
      update_user_roles;
      ;;
    view)
      get_user_message;
      ;;
    *)
      echo -e "${red_color}您为输入需要执行的操作！${text_end}"
esac