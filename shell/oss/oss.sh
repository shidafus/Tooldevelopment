#!/bin/bash
#message=(ads-ldpage data-center decal employee evaluation finance human inventory oa-signture old-oa oms pda-traceability product supply test traceability)
message=`mc ls minio-prod | awk '{print $5 }' | sed 's#\/##'`
echo $message

for i in ${message[*]};do
    rclone sync oldminio:$i  newminio:$i
done