#!/bin/bash
##################################################################################################################
##   Create_time     : 2023/6/30                                                                                ##
##   Author          : Ops-DaBao                                                                                ##
##   Feature         : restore mongodb Data                                                                       ##
##   Usage           : When executing the script, you can pass parameters.                                      ##
##                     If you do not pass parameters, the default is used                                       ##
##################################################################################################################
# shellcheck disable=SC2034
red_color="\033[31m"
green_color="\033[32m"
text_end="\033[0m"

# 定义默认值
backup_file="/mongobackup/2023-07-03-15-00-33/2023-07-03-15-00-33-mydatabase.sql"
username="admin"
password="root"
database_name="mydatabase"
collection_name="student"

parameter_passing() {
	# 检查是否有参数传递，如果有则覆盖默认值
	while getopts ":f:u:p:d:t:" opt; do
	  case $opt in
	    f) backup_file=$OPTARG;;
	    u) username=$OPTARG;;
	    p) password=$OPTARG;;
	    d) database_name=$OPTARG;;
	    t) collection_name=$OPTARG;;
	    \?) echo "Invalid option: -$OPTARG" >&2;;
	  esac
	done

	# 检查备份文件是否存在
	if [ ! -f "$backup_file" ]; then
	  echo "Backup file not found: $backup_file"
	  exit 1
	fi
}

restore_single_table_data() {
	# 还原单个集合的数据
	echo -e "${red_color}-----------本次进行单集合数据恢复-----------${text_end}"
	docker exec mongodb /bin/bash -c "mongorestore -u $username -p$password --archive  --db $database_name --collection  $collection_name" < $backup_file
	echo -e "${green_color}-----------恢复完毕！-----------${text_end}"
}

restore_the_entire_library_data() {
	# 还原单个数据库的数据
	echo -e "${red_color}-----------本次进行单库据恢复-----------${text_end}"
	docker exec mongodb /bin/bash -c "mongorestore -u $username -p$password --archive  --db $database_name" < $backup_file
	echo -e "${green_color}-----------恢复完毕！-----------${text_end}"
}


Restore_a_database_in_full() {
	# 从全量数据中，还原一个数据库
	echo -e "${red_color}----------本次进行全量中单库据恢复-----------${text_end}"
	docker exec MySQL8 /bin/bash -c "mongorestore -u $username -p$password  --archive  --db $database_name" < $backup_file
	echo -e "${green_color}----------恢复完毕！-----------${text_end}"
}

parameter_passing;
# 功能函数调用,从下行开始
restore_the_entire_library_data;