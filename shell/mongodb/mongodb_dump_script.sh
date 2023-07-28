#!/bin/bash
#################################################################################################################
##   create_time    : 2023/6/30                                                                                ##
##   Author         : Ops-DaBao                                                                                ##
##   Feature        : Backing up mongodb Data                                                                    ##
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
backup_dir=/mongobackup/$dd
#用户名
username="admin"
#密码
password="xqqwe123qwe123p0EW"
#将要备份的数据库 ,一个数组
database_name="log"



# 检查是否有参数传递，如果有则覆盖默认值
while getopts ":u:p:d:*" opt; do
	case $opt in
	  u) username="$OPTARG";;
	  p) password="$OPTARG";;
	  d) database_name="$OPTARG";;
	  *) echo "未知参数";;
	esac
done
echo "Mongo user: $username"
echo "Mongo password: $password"
echo "Mongo database_name: $database_name"

# 如果文件夹不存在则创建
if [ ! -d $backup_dir ]; then
	  mkdir -p $backup_dir;
fi


backup_single_collection() {
	# 开始备份数据，单个数据库独立备份
	echo -e "${red_color}----------本次进行单库备份-----------$text_end"
	docker exec mongodb /bin/bash -c "mongodump -u $username -p$password --authenticationDatabase admin --archive --db $database_name" 1> $backup_dir/$database_name.archive 2> /tmp/$dd-$database_name.log;
	echo -e "${green_color}-----------${DB}数据库备份完毕-----------$text_end"
}

full_backup() {
	# 备份所有数据到同一份文件中
	echo -e "${red_color}-----------本次进行全量备份-----------$text_end"
	docker exec mongodb /bin/bash -c "mongodump -u $username -p$password  --authenticationDatabase admin --archive" 1> $backup_dir/$dd-all.archive 2> /tmp/$dd-$collection_name.log
	echo -e "${green_color}----------备份完毕！-----------$text_end"
}

spatial_optimization() {
	#找出需要删除的备份
	echo -e "${red_color}----------开始查询过期数据-----------$text_end"
	find /mongobackup/* -maxdepth 1 -type d -ctime +31 -exec rm -rf {} \;
	echo -e "${green_color}-----------过期数据清理完毕！-----------$text_end"
}

backup_single_collection;
spatial_optimization;