#! /bin/bash

#ref: https://github.com/google/cadvisor/blob/master/docs/runtime_options.md
systemctl daemon reload

systemctl restart docker

docker pull google/cadvisor:latest

#docker service create  --mode global --name cadvisor \
#  --mount type=bind,source=/,target=/rootfs,readonly=true \
#  --mount type=bind,source=/var/run,target=/var/run,readonly=false \
#  --mount type=bind,source=/sys,target=/sys,readonly=true \
#  --mount type=bind,source=/var/lib/docker/,target=/var/lib/docker,readonly=true \
#  --publish=8080:8080 \    // enable publish to check live stats in browser
#  --detach=true \
#  google/cadvisor:latest \
#  -housekeeping_interval=30s \
#  -storage_driver=statsd \
#  -storage_driver_host=host_ip:8125 \   // graphite vm ip address
#  -storage_driver_db=db_name

docker service create  --mode global --name cadvisor \
  --mount type=bind,source=/,target=/rootfs,readonly=true \
  --mount type=bind,source=/var/run,target=/var/run,readonly=false \
  --mount type=bind,source=/sys,target=/sys,readonly=true \
  --mount type=bind,source=/var/lib/docker/,target=/var/lib/docker,readonly=true \
  --detach=true \
  google/cadvisor:latest \
  -housekeeping_interval=30s \
  -storage_driver=statsd \
  -storage_driver_host=$1:8125 \
  -storage_driver_db=$2


