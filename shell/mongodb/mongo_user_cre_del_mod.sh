#!/bin/bash
#MongoDB 数据库用户名、密码、主机地址、端口
DB_USER="root"
DB_PASS="wpUvlYgpcweFQ2B8"
DB_HOST="dds-bp1ae778e813f0541409-pub.mongodb.rds.aliyuncs.com"
DB_PORT="3717"


#添加新用户
add_user() {
read -p "请输入要添加的用户名: " username
read -p "请输入该用户的密码: " password
read -p "请输入该用户在哪个数据库中具有权限: " db_name
mongo admin -u $DB_USER -p $DB_PASS --host $DB_HOST --port $DB_PORT --eval "db = db.getSiblingDB('$db_name');db.runCommand({createUser: '$username',pwd:'$password',roles: [{ role: 'read', db: '$db_name' }]});"
echo "用户添加成功"
}


#删除用户
delete_user() {
read -p "请输入要删除的用户名: " username
read -p "请输入要删除的用户名所在的数据库: " db_name
mongo admin -u $DB_USER -p $DB_PASS --host $DB_HOST --port $DB_PORT --eval " db = db.getSiblingDB('$db_name') ; db.dropUser( '$username') "
echo "用户删除成功"
}

#修改用户权限
modify_user_role() {
read -p "请输入要修改权限的用户名: " username
# 展示该用户已拥有的角色
#echo "用户已拥有的角色："
#mongo admin -u $DB_USER -p $DB_PASS --host $DB_HOST --port $DB_PORT --eval "db.getUser('$username').roles"
# 展示可用的角色
echo "可供选择的角色："
echo "================"
echo "1. read"
echo "2. readWrite"
echo "3. dbAdmin"
echo "4. dbOwner"
echo "5. userAdmin"
echo "6. backup"
echo "7. restore"
echo "8. root"
echo "=========================="
read -p "请选择新的角色: " role
case $role in
    1)
        new_role="read"
        ;;
    2)
        new_role="readWrite"
        ;;
    3)
        new_role="dbAdmin"
        ;;
    4)
        new_role="dbOwner"
        ;;
    5)
        new_role="userAdmin"
        ;;
    6)
        new_role="backup"
        ;;
    7)
        new_role="restore"
        ;;
    8)
        new_role="root"
        ;;
    *)
        echo "无效的选择，权限修改失败！"
        return 1
        ;;
esac
read -p "请输入要修改权限的数据库名：" db_name
mongo admin -u $DB_USER -p $DB_PASS --host $DB_HOST --port $DB_PORT --eval " db = db.getSiblingDB('$db_name') ; db.grantRolesToUser('$username', [{role: '$new_role', db: '$db_name'}])"
echo "用户权限修改成功"
}


#显示帮助信息
print_help() {
echo "使用方法:"
echo "./mongodb_user_mgmt.sh [add|delete|modify]"
echo ""
echo "选项:"
echo "add     添加一个新用户"
echo "delete  删除一个用户"
echo "modify  修改一个用户的权限"
}


#检查参数是否正确
if [ $# -eq 0 ]; then
print_help
exit 0
fi
#根据参数调用对应的函数
case $1 in
"add")
add_user
;;
"delete")
delete_user
;;
"modify")
modify_user_role
;;
*)
echo "无效的参数: $1"
print_help
exit 1
;;
esac