#!/bin/bash

# MySQL连接参数
MYSQL_USER="your_mysql_username"
MYSQL_PASSWORD="your_mysql_password"
MYSQL_HOST="localhost"
MYSQL_DATABASE="your_database_name"

# 函数：创建MySQL用户
create_mysql_user() {
    local username=$1
    local password=$2
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -h "$MYSQL_HOST" -e "CREATE USER '$username'@'%' IDENTIFIED BY '$password';"
    echo "MySQL user '$username' created successfully."
}

# 函数：删除MySQL用户
delete_mysql_user() {
    local username=$1
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -h "$MYSQL_HOST" -e "DROP USER IF EXISTS '$username'@'%';"
    echo "MySQL user '$username' deleted successfully."
}

# 函数：修改MySQL用户密码
change_mysql_user_password() {
    local username=$1
    local new_password=$2
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -h "$MYSQL_HOST" -e "ALTER USER '$username'@'%' IDENTIFIED BY '$new_password';"
    echo "MySQL user '$username' password changed successfully."
}

# 函数：授予MySQL用户权限
grant_mysql_user_permissions() {
    local username=$1
    local database=$2
    local permissions=$3
    mysql -u "$MYSQL_USER" -p"$MYSQL_PASSWORD" -h "$MYSQL_HOST" -e "GRANT $permissions ON $database.* TO '$username'@'%'; FLUSH PRIVILEGES;"
    echo "MySQL user '$username' granted '$permissions' permissions on database '$database'."
}

# 主函数
main() {
    echo "MySQL User Management Script"
    echo "1. Create User"
    echo "2. Delete User"
    echo "3. Change Password"
    echo "4. Grant Permissions"
    read -p "Enter your choice (1/2/3/4): " choice

    case $choice in
        1)
            read -p "Enter username: " username
            read -p "Enter password: " password
            create_mysql_user "$username" "$password"
            ;;
        2)
            read -p "Enter username to delete: " username
            delete_mysql_user "$username"
            ;;
        3)
            read -p "Enter username to change password: " username
            read -p "Enter new password: " new_password
            change_mysql_user_password "$username" "$new_password"
            ;;
        4)
            read -p "Enter username: " username
            read -p "Enter database name: " database
            read -p "Enter permissions (e.g., SELECT, INSERT, UPDATE): " permissions
            grant_mysql_user_permissions "$username" "$database" "$permissions"
            ;;
        *)
            echo "Invalid choice. Please select a valid option."
            ;;
    esac
}

# 调用主函数
main
