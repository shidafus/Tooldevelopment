#!/bin/bash
##################################################################################################################
##   Create_time     : 2023/6/30                                                                                ##
##   Author          : Ops-DaBao                                                                                ##
##   Mail            : zjh13320020268@163.com                                                                   ##
##   Feature         : restore mongodb Data                                                                     ##
##   Usage           : When executing the script, you can pass parameters.                                      ##
##                     If you do not pass parameters, the default is used                                       ##
##################################################################################################################
# shellcheck disable=SC2034
red_color="\033[31m"
green_color="\033[32m"
text_end="\033[0m"
start_time=$(date +%s)
backup_file=""
username=""
password=""
database_name=""
collection_name=""
tip=""


usage() {
  echo "脚本使用方法:    bash $0 <选项> <参数>"
  echo "选项说明:"
  echo " -f <文件路径>:  数据保存路径,绝对路径 （默认为空）"
  echo " -u <用户名>:   指定用户名 (默认为空)"
  echo " -p <密码>:     指定密码 (默认为空)"
  echo " -d <数据库名>:  指定数据库名 (默认为空)"
  echo " -c <数据集合>:  指定数据库集合名 (默认为空)"
  echo " -t <恢复种类>:  指定恢复 数据 assemble(集合) 或 singlelibrary(数据库)  或 fulllibrary(全库) (默认为空)"
  exit 1
}

restore_single_table_data() {
	# 还原单个集合的数据
	echo -e "${red_color}-----------本次进行单集合数据恢复-----------${text_end}"
	docker exec mongodb /bin/bash -c "mongorestore -u $username -p$password --authenticationDatabase admin --archive  --db $database_name --collection  $collection_name" < $backup_file
	echo -e "${green_color}-----------恢复完毕！-----------${text_end}"
	echo -e "${green_color}-----本次是使用${backup_file}进行数据恢复-----------${text_end}"
}

restore_the_entire_library_data() {
	# 还原单个数据库的数据
	echo -e "${red_color}-----------本次进行单库据恢复-----------${text_end}"
	docker exec mongodb /bin/bash -c "mongorestore -u $username -p$password --authenticationDatabase admin --archive  --db $database_name" < $backup_file
	echo -e "${green_color}-----------恢复完毕！-----------${text_end}"
	echo -e "${green_color}-----本次是使用${backup_file}进行数据恢复-----------${text_end}"
}


Restore_a_database_in_full() {
	# 从全量数据中，还原一个数据库
	echo -e "${red_color}----------本次进行全量中单库据恢复-----------${text_end}"
	docker exec MySQL8 /bin/bash -c "mongorestore -u $username -p$password  --authenticationDatabase admin --archive  --db $database_name" < $backup_file
	echo -e "${green_color}----------恢复完毕！-----------${text_end}"
	echo -e "${green_color}-----本次是使用${backup_file}进行数据恢复-----------${text_end}"
}


# 检查是否有参数传递，如果有则覆盖默认值
while getopts ":f:u:p:d:c:t:*:" opt; do
  case $opt in
    f) backup_file="$OPTARG";;
    u) username="$OPTARG";;
    p) password="$OPTARG";;
    d) database_name="$OPTARG";;
    c) collection_name="$OPTARG";;
    t) tip="$OPTARG";;
    *) echo "参数传入有误: -$OPTARG"; usage;;
  esac
done

# 检查备份文件是否存在
if [ ! -f "$backup_file" ]; then
  echo "Backup file not found: $backup_file"
  exit 1
fi


case $tip in
    assemble)
      echo -e "${green_color}Mongo database_name: ${database_name}${text_end}"
      echo -e "${green_color}Mongo database_name: ${collection_name}${text_end}"
      restore_single_table_data;
      ;;
    singlelibrary)
      echo -e "${green_color}Mongo database_name: ${database_name}${text_end}"
      Restore_a_database_in_full;
      ;;
    fulllibrary)
      echo -e "${green_color}Mongo database_name: ${database_name}${text_end}"
      Restore_a_database_in_full;
      ;;
    *)
      echo -e "${red_color}暂时无法确认你要恢复那些数据${text_end}"
esac


end_time=$(date +%s)
execution_time=$((end_time - start_time))

echo -e "${green_color}本次执行脚本耗时为：$execution_time 秒${text_end}"