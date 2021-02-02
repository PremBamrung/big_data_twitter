import os
import time


zookeeper = "zookeeper-server-start ~/Downloads/kafka-2.6.0-src/config/zookeeper.properties &"
kafka = (
    "kafka-server-start ~/Downloads/kafka-2.6.0-src/config/server.properties &"
)
elasticsearch = "~/server/elasticsearch-7.10.1/bin/elasticsearch &"
kibana = "~/server/kibana-7.10.1-darwin-x86_64/bin/kibana"


os.system('rm -rf ~/tmt/kafka-logs')
os.system(zookeeper)
time.sleep(5)

os.system(kafka)
time.sleep(7)


os.system('pkill -f elasticsearch')
os.system(elasticsearch)
time.sleep(7)

os.system(kibana)
time.sleep(7)

# zookeeper-server-stop.sh ~/intergiciels/kafka_2.13-2.7.0/config/zookeeper.properties