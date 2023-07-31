#!/bin/bash
#!/bin/bash
##################################################################################################################
##   Create_time     : 2023/7/28                                                                                ##
##   Author          : Ops-DaBao                                                                                ##
##   Feature         : Delete expired files and directories                                                     ##                                     ##
##################################################################################################################

#basefile=( "/data/executor/tmp" "/data/executor/tmp2" )
#tmpbase="/data/executor/tmp"
#
#masterfile="/data/executor/tmp/master"
#tmpfile="/data/executor/tmp/tmp"
#
#mergefile="/data/executor/tmp/merge"
#npgMergefile="/data/executor/tmp/npgMerge"
#sharefile="/data/executor/tmp/share"
#
#tmp2base="/data/executor/tmp2"
#
#downloadfile="/data/executor/tmp2/download"
#coverfile="/data/executor/tmp2/cover"
#vlogfile="/data/executor/tmp2/vlog"

pwd="/data/executor"
dd=`date +%Y-%m-%d-%H-%M-%S`
logfile="/tmp/deleted-${dd}.txt"
# 保留7天
tmp1data=( "${pwd}/tmp/master"
            "${pwd}/tmp/tmp"
            )

# 保留三天
tmpdata=( "${pwd}/tmp/merge"
          "${pwd}/tmp/npgMerge"
          "${pwd}/tmp/share"
          "${pwd}/tmp2/download"
          "${pwd}/tmp2/cover"
          "${pwd}/tmp2/vlog"
          )

# 删除文件
delfile() {
    for file in $tmp1data; do
      find $file  -maxdepth 3 -type f -ctime +7 -exec rm {} \; -printf "Deleting: %p\t%TY-%Tm-%Td %TH:%TM:%.2TS\n" >> $logfile
    done
    for file in $tmpdata; do
      find $file  -maxdepth 3 -type f -ctime +3 -exec rm {} \; -printf "Deleting: %p\t%TY-%Tm-%Td %TH:%TM:%.2TS\n" >> $logfile
    done
}

# 删除目录
deldirectories() {
    for file in $tmp1data; do
      find $file/*  -maxdepth 3 -type d -empty -ctime +7 -exec rm -rf {} \; -printf "Deleting: %p\t%TY-%Tm-%Td %TH:%TM:%.2TS\n" >> $logfile
    done
    for file in $tmpdata; do
      find $file/*  -maxdepth 3 -type d -empty -ctime +3 -exec rm -rf {} \; -printf "Deleting: %p\t%TY-%Tm-%Td %TH:%TM:%.2TS\n" >> $logfile
    done
}

delfile;
deldirectories;
