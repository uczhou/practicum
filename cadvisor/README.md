## run_cadvisor script
This script will pull docker image from docker hub and create a service for cadvisor so it will run as a deamon.
```
./run_cadvisor dbhost_ip dbname_for_this_monitor
```


## run_graphite_statsd script
This script will pull docker image from docker hub and run the statsd/graphite stack in container.