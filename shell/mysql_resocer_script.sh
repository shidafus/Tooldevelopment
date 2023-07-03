#!/bin/bash

##################################################################################################################
##   Create_time     : 2023/6/30                                                                                ##
##   Author          : Ops-DaBao                                                                                ##
##   Feature         : restore mysql Data                                                                       ##
##   Usage           : When executing the script, you can pass parameters.                                      ##
##                     If you do not pass parameters, the default is used                                       ##
##################################################################################################################



# 定义默认值
backup_file="/mysqlbackup/2023-07-03-15-00-33/2023-07-03-15-00-33-mydatabase.sql"
username="root"
password="root"
database_name="mydatabase"
table_name="student"

parameter_passing() {
	# 检查是否有参数传递，如果有则覆盖默认值
	while getopts ":f:u:p:d:t:" opt; do
	  case $opt in
	    f) backup_file=$OPTARG;;
	    u) username=$OPTARG;;
	    p) password=$OPTARG;;
	    d) database_name=$OPTARG;;
	    t) table_name=$OPTARG;;
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
	# 还原单表数据
	sed  -n  "/CREATE TABLE \`$table_name\` /,/\;/p" $backup_file  > $table_name.sql
	sed -n "/INSERT INTO \`$table_name\`/p" $backup_file >> $table_name.sql
	docker cp $table_name.sql MySQL8:/$table_name.sql
	docker exec MySQL8 /bin/bash -c "mysql -u $username -p$password -e 'use $database_name;' -e 'source /$table_name.sql;'"

}

restore_the_entire_library_data() {
	# 如果数据库不存在则先创建出来，在继续回复数据
	docker exec MySQL8 /bin/bash -c "mysql -u $username -p$password -e 'CREATE DATABASE IF NOT EXISTS $database_name'"
	# 还原单库数据
	docker cp $backup_file MySQL8:/backup_file.sql
	docker exec MySQL8 /bin/bash -c "mysql -u $username -p$password -e 'use $database_name;' -e 'source /backup_file.sql;'"
}


Restore_a_database_in_full() {
	# 从全量数据中，还原一个数据库
	docker exec MySQL8 /bin/bash -c "mysql -u $username -p$password  --one-database $database_name" < $backup_file
}

parameter_passing;
# 功能函数调用,从下行开始
restore_the_entire_library_data;
