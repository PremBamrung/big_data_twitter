import os
import time


zookeeper = "zookeeper-server-start.sh ~/intergiciels/kafka_2.13-2.7.0/config/zookeeper.properties &"
kafka = (
    "kafka-server-start.sh ~/intergiciels/kafka_2.13-2.7.0/config/server.properties &"
)
elasticsearch = "~/server/elasticsearch-7.10.1/bin/elasticsearch &"
kibana = "~/server/kibana-7.10.1-linux-x86_64/bin/kibana"

os.system(zookeeper)
time.sleep(5)

os.system(kafka)
time.sleep(7)

os.system(elasticsearch)
time.sleep(7)

os.system(kibana)
time.sleep(7)

# zookeeper-server-stop.sh ~/intergiciels/kafka_2.13-2.7.0/config/zookeeper.properties