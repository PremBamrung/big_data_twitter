import os
import time

zookeeper = "zookeeper-server-start.sh ~/logiciels/kafka_2.13-2.7.0/config/zookeeper.properties &"
kafka = "kafka-server-start.sh ~/logiciels/kafka_2.13-2.7.0/config/server.properties &"
elasticsearch = "elasticsearch-7.10.1/bin/elasticsearch &"
kibana = "kibana-7.10.1-linux-x86_64/bin/kibana"


def main():
    # print("Exporting environment variable")
    # os.system("export JAVA_HOME=$HOME/logiciels/jdk1.8.0_221")
    # os.system("export PATH=$JAVA_HOME/bin:$PATH")
    # os.system("export SPARK_HOME=$HOME/logiciels/spark-2.4.7-bin-hadoop2.7")
    # os.system("export PATH=$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH")
    # os.system("export SCALA_HOME=$HOME/logiciels/scala-2.13.4")
    # os.system("export PATH=$SCALA_HOME/bin:$SCALA_HOME/sbin:$PATH")
    # os.system("export SBT_HOME=$HOME/logiciels/sbt")
    # os.system("export PATH=$SBT_HOME/bin:$SBT_HOME/sbin:$PATH")
    # os.system("export KAFKA_HOME=$HOME/logiciels/kafka_2.13-2.7.0")
    # os.system("export PATH=$KAFKA_HOME/bin:$KAFKA_HOME/sbin:$PATH")
    # os.system("export ZOOKEEPER_HOME=$HOME/logiciels/apache-zookeeper-3.6.2-bin")
    # os.system("export PATH=$ZOOKEEPER_HOME/bin:$ZOOKEEPER_HOME/sbin:$PATH")

    # os.environ["JAVA_HOME"] = "$HOME/logiciels/jdk1.8.0_221"
    # os.environ["PATH"] = "$JAVA_HOME/bin:$PATH"
    # os.environ["SPARK_HOME"] = "$HOME/logiciels/spark-2.4.7-bin-hadoop2.7"
    # os.environ["PATH"] = "$SPARK_HOME/bin:$SPARK_HOME/sbin:$PATH"
    # os.environ["SCALA_HOME"] = "$HOME/logiciels/scala-2.13.4"
    # os.environ["PATH"] = "$SCALA_HOME/bin:$SCALA_HOME/sbin:$PATH"
    # os.environ["SBT_HOME"] = "$HOME/logiciels/sbt"
    # os.environ["PATH"] = "$SBT_HOME/bin:$SBT_HOME/sbin:$PATH"
    # os.environ["KAFKA_HOME"] = "$HOME/logiciels/kafka_2.13-2.7.0"
    # os.environ["PATH"] = "$KAFKA_HOME/bin:$KAFKA_HOME/sbin:$PATH"
    # os.environ["ZOOKEEPER_HOME"] = "$HOME/logiciels/apache-zookeeper-3.6.2-bin"
    # os.environ["PATH"] = "$ZOOKEEPER_HOME/bin:$ZOOKEEPER_HOME/sbin:$PATH"
    time.sleep(2)
    os.system(zookeeper)
    time.sleep(5)

    os.system(kafka)
    time.sleep(7)

    os.system(elasticsearch)
    time.sleep(7)

    os.system(kibana)
    time.sleep(7)


# zookeeper-server-stop.sh ~/intergiciels/kafka_2.13-2.7.0/config/zookeeper.properties
if __name__ == "__main__":
    main()