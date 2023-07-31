#!/bin/bash
#################################################################################################################
##   create_time    : 2023/6/30                                                                                ##
##   Author         : Ops-DaBao                                                                                ##
##   Mail           : zjh13320020268@163.com                                                                   ##
##   Feature        : Backing up mongodb Data                                                                  ##
##   Usage          : When executing the script, you can pass parameters.                                      ##
##                    If you do not pass parameters, the default is used                                       ##
#################################################################################################################
# shellcheck disable=SC2034
red_color="\033[31m"
green_color="\033[32m"
text_end="\033[0m"
start_time=$(date +%s)
numberdays="31"
dd=`date +%Y-%m-%d-%H-%M-%S`
backup_dir=/data/backup/mongodb
username=""
password=""
database_name=""
tip="all"

usage() {
  echo "脚本使用方法: bash $0 <选项> <参数>"
  echo "选项说明:"
  echo " -f <目录路径>: 数据保存路径 （默认为 /data/backup/mongodb）"
  echo " -u <用户名>: 指定用户名 (默认为空)"
  echo " -p <密码>: 指定密码 (默认为空)"
  echo " -d <数据库名>: 指定数据库名 (默认为空)"
  echo " -t <备份方式>: single  or  all (默认为all)  当为all时，指定的数据库参数无效"
  echo " -n <天数>: 指定删除多少天前的无效数据 (默认为31天)"
  exit 1
}

backup_single_collection() {
	# 开始备份数据，单个数据库独立备份
	echo -e "${red_color}----------本次进行单库备份-----------$text_end"
	docker exec mongodb /bin/bash -c "mongodump -u $username -p$password --authenticationDatabase admin --archive --db $database_name" 1> $backup_dir/$database_name-$dd.archive 2> /tmp/$database_name-$dd.log;
	echo -e "${green_color}-----------${DB}数据库备份完毕-----------$text_end"
	echo -e "${green_color}-----------数据保存在 （$backup_dir/$database_name-$dd.archive） 中-----------$text_end"
}

full_backup() {
	# 备份所有数据到同一份文件中
	echo -e "${red_color}-----------本次进行全量备份-----------$text_end"
	docker exec mongodb /bin/bash -c "mongodump -u $username -p$password  --authenticationDatabase admin --archive" 1> $backup_dir/all-$dd.archive 2> /tmp/all-$dd.log
	echo -e "${green_color}----------备份完毕！-----------$text_end"
	echo -e "${green_color}-----------数据保存在 （$backup_dir/all-$dd.archive） 中-----------$text_end"
}

spatial_optimization() {
	#找出需要删除的备份
	echo -e "${red_color}----------开始查询${numberdays}天以前的数据并删除-----------$text_end"
	find $backup_dir/* -maxdepth 1 -type d -ctime +${numberdays} -exec rm -rf {} \;
	echo -e "${green_color}-----------过期数据清理完毕！-----------$text_end"
}

# 检查是否有参数传递，如果有则覆盖默认值
while getopts ":f:u:p:d:t:n:h:*:" opt; do
	case $opt in
	  f) backup_dir="$OPTARG";;
	  u) username="$OPTARG";;
	  p) password="$OPTARG";;
	  d) database_name="$OPTARG";;
	  t) tip="$OPTARG";;
	  n) numberdays="$OPTARG";;
	  *) echo "参数传入有误: -$OPTARG"; usage;;
	esac
done

# 如果文件夹不存在则创建
if [ ! -d $backup_dir ]; then
	  mkdir -p $backup_dir;
fi


case $tip in
    all)
      echo -e "${green_color}Mongo database_name: ${database_name}${text_end}"
      full_backup;
      spatial_optimization;
      ;;
    single)
      echo -e "${green_color}Mongo database_name: ${database_name}${text_end}"
      backup_single_collection;
      spatial_optimization;
      ;;
    *)
      echo -e "${red_color}暂时无法确认你要备份那些数据${text_end}"
esac

end_time=$(date +%s)
execution_time=$((end_time - start_time))

echo -e "${green_color}本次执行脚本耗时为：$execution_time 秒${text_end}"