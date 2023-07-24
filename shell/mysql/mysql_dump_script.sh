#!/bin/bash
#################################################################################################################
##   create_time    : 2023/6/30                                                                                ##
##   Author         : Ops-DaBao                                                                                ##
##   Feature        : Backing up mysql Data                                                                    ##
##   Usage          : When executing the script, you can pass parameters.                                      ##
##                    If you do not pass parameters, the default is used                                       ##
##################################################################################################################
# shellcheck disable=SC2034
red_color="\033[31m"
green_color="\033[32m"
text_end="\033[0m"

#保存备份个数，备份31天数据
number=31
#日期
dd=`date +%Y-%m-%d-%H-%M-%S`
#备份保存路径
backup_dir=/mysqlbackup/$dd
#备份工具
tool=mysqldump
#用户名
username="root"
#密码
password="root"
#将要备份的数据库
database_name=mydatabase


# 检查是否有参数传递，如果有则覆盖默认值
while getopts "d:u:p:*" opt; do
  case $opt in
    d) backup_dir="$OPTARG";;
    u) username="$OPTARG";;
    p) password="$OPTARG";;
    *) echo "未知参数";;
  esac
done
echo "Backup directory: $backup_dir"
echo "MySQL user: $username"
echo "MySQL password: $password"
#如果文件夹不存在则创建
if [ ! -d $backup_dir ]; then
    mkdir -p $backup_dir;
fi

backup_single_database() {
	# 开始备份数据，单个数据库独立备份
	echo -e "${red_color}----------本次进行全量单库for循环备份-----------$text_end"
	for DB in $(docker exec  MySQL8 /bin/bash -c  "mysql -u $username -p$password  -e 'show databases' -s --skip-column-names"); do
	    docker exec MySQL8 /bin/bash -c "$tool -u $username -p$password --single-transaction  --set-gtid-purged=off --hex-blob --events --routines $DB" 1> $backup_dir/$dd-$DB.sql 2> /tmp/$dd-$DB.log;
	    echo -e "${green_color}-----------${DB}数据库备份完毕-----------$text_end"
	done
	echo -e "${green_color}-----------全部备份完毕！-----------$text_end"
}

full_backup() {
	# 备份所有数据到同一份文件中
	echo -e "${red_color}-----------本次进行全量备份-----------$text_end"
	docker exec MySQL* /bin/bash -c "$tool -u $username -p$password --single-transaction --set-gtid-purged=off --hex-blob --events --routines $database_name" 1> $backup_dir/$dd-$database_name.sql 2> /tmp/$dd-$database_name.log
	echo -e "${green_color}----------备份完毕！-----------$text_end"
}

spatial_optimization() {
	#找出需要删除的备份
	echo -e "${red_color}----------开始查询过期数据-----------$text_end"
	find /mysqlbackup/* -maxdepth 1 -type d -mtime +31 -exec rm -rf {} \;
	echo -e "${green_color}-----------过期数据清理完毕！-----------$text_end"
}


backup_single_database;
spatial_optimization;