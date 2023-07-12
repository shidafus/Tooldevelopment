#!/bin/bash
#################################################################################################################
##   create_time    : 2023/6/30                                                                                ##
##   Author         : Ops-DaBao                                                                                ##
##   Feature        : Backing up mysql Data                                                                    ##
##   Usage          : When executing the script, you can pass parameters.                                      ##
##                    If you do not pass parameters, the default is used                                       ##
##################################################################################################################


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


parameter_passing() {
	# 检查是否有参数传递，如果有则覆盖默认值
	while getopts ":d:u:p:" opt; do
	  case $opt in
	    d) backup_dir=$OPTARG;;
	    u) username=$OPTARG;;
	    p) password=$OPTARG;;
	    \?) echo "Invalid option: -$OPTARG" >&2;;
	  esac
	done
	echo "Backup directory: $backup_dir"
	echo "MySQL user: $username"
	echo "MySQL password: $password"
	#如果文件夹不存在则创建
	if [ ! -d $backup_dir ];
	then
	    mkdir -p $backup_dir;
	fi
}

backup_single_database() {
	# 开始备份数据，单个数据库独立备份
	for DB in $(docker exec  MySQL8 /bin/bash -c  "mysql -u $username -p$password  -e 'show databases' -s --skip-column-names"); do
	    docker exec MySQL8 /bin/bash -c "$tool -u $username -p$password --single-transaction  --set-gtid-purged=off --hex-blob --events --routines $DB" 1> $backup_dir/$dd-$DB.sql 2> /tmp/$dd-$DB.log;
	done
}

full_backup() {
	# 备份所有数据到同一份文件中
	docker exec MySQL* /bin/bash -c "$tool -u $username -p$password --single-transaction --set-gtid-purged=off --hex-blob --events --routines $database_name" 1> $backup_dir/$dd-$database_name.sql 2> /tmp/$dd-$database_name.log
}

spatial_optimization() {
	#找出需要删除的备份
	find /mysqlbackup/* -maxdepth 1 -type d -mtime +31 -exec rm -rf {} \;
}


parameter_passing;
backup_single_database;
spatial_optimization;