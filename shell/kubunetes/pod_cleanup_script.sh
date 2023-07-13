#!/bin/bash

source /etc/profile
printf "\n本次操作是用来清理集群内部状态为 Evicted 和 Failed 的Pod !\n"

printf "\nA.  Aliyun-product      B.   Aliyun-test     C.    k8s-Intranet\n\n"

read -p "你需要清理的集群是:" mess

if [ $mess == A ];then
  cluster=Aliyun-product
elif [ $mess == B ];then
  cluster=Aliyun-test
elif [ $mess == C ];then
  cluster=k8s-Intranet
fi

printf "\n以切换至您需要操作的集群!\n"

kubecm switch $cluster > /dev/null

read -p  "您是否需要选择清理  (yes/no): " judge

if [ $judge == yes  ];then
   echo "正在清理中，请勿 ctrl+c 中断操作!"
   /usr/bin/kubectl get pods --all-namespaces -o go-template='{{range .items}} {{if (or (eq .status.phase "Evicted") (eq .status.phase "Failed" ))}} {{.metadata.name}}{{" "}} {{.metadata.namespace}} {{"\n"}}{{end}} {{end}}' | while read epod namespace; do kubectl -n $namespace delete pod $epod; done; >> /root/shell/pod/log/$mess-$(date +%Y-%m-%d-%H-%M-%S).txt
   logfile=$mess-$(date +%Y-%m-%d-%H-%M-%S).txt
else
   echo "正在停止并退出!"
   exit

fi

if [ $? != 0  ];then
   printf "\n在${cluster}集群未能清理成功\n"
elif [ ! -s ${logfile} ];then
   printf "\n在${cluster}集群中没有可清理的POD\n"
   /usr/bin/rm -rf  /root/shell/pod/log/${logfile}
else
   printf "\n在${cluster}集群以清理完毕!\n"
   printf "\n清理的POD保存在/root/shell/pod/log/${logfile}中\n"
fi
kubecm switch k8s-Intranet > /dev/null