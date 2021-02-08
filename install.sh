workdir=$(pwd)
cd
mkdir logiciels
cd logiciels/
wget https://apache.mirrors.benatherton.com/spark/spark-2.4.7/spark-2.4.7-bin-hadoop2.7.tgz
tar xzf spark-2.4.7-bin-hadoop2.7.tgz
rm spark-2.4.7-bin-hadoop2.7.tgz
wget https://downloads.lightbend.com/scala/2.13.4/scala-2.13.4.tgz
tar xzf scala-2.13.4.tgz
rm scala-2.13.4.tgz
wget https://github.com/sbt/sbt/releases/download/v1.4.5/sbt-1.4.5.tgz
tar xzf sbt-1.4.5.tgz
rm sbt-1.4.5.tgz
wget https://downloads.apache.org/kafka/2.7.0/kafka_2.13-2.7.0.tgz
tar xzf kafka_2.13-2.7.0.tgz
rm kafka_2.13-2.7.0.tgz
wget https://downloads.apache.org/zookeeper/zookeeper-3.6.2/apache-zookeeper-3.6.2-bin.tar.gz
tar xzf apache-zookeeper-3.6.2-bin.tar.gz
rm apache-zookeeper-3.6.2-bin.tar.gz
wget http://sd-127206.dedibox.fr/hagimont/software/jdk-8u221-linux-x64.tar.gz
tar xzf jdk-8u221-linux-x64.tar.gz
rm jdk-8u221-linux-x64.tar.gz
echo "export JAVA_HOME=\$HOME/logiciels/jdk1.8.0_221" >>~/.bashrc
echo "export PATH=\$JAVA_HOME/bin:\$PATH" >>~/.bashrc

echo "export SPARK_HOME=\$HOME/logiciels/spark-2.4.7-bin-hadoop2.7" >>~/.bashrc
echo "export PATH=\$SPARK_HOME/bin:\$SPARK_HOME/sbin:\$PATH" >>~/.bashrc

echo "export SCALA_HOME=\$HOME/logiciels/scala-2.13.4" >>~/.bashrc
echo "export PATH=\$SCALA_HOME/bin:\$SCALA_HOME/sbin:\$PATH" >>~/.bashrc

echo "export SBT_HOME=\$HOME/logiciels/sbt" >>~/.bashrc
echo "export PATH=\$SBT_HOME/bin:\$SBT_HOME/sbin:\$PATH" >>~/.bashrc


echo "export KAFKA_HOME=\$HOME/logiciels/kafka_2.13-2.7.0" >>~/.bashrc
echo "export PATH=\$KAFKA_HOME/bin:\$KAFKA_HOME/sbin:\$PATH" >>~/.bashrc

echo "export ZOOKEEPER_HOME=\$HOME/logiciels/apache-zookeeper-3.6.2-bin" >>~/.bashrc
echo "export PATH=\$ZOOKEEPER_HOME/bin:\$ZOOKEEPER_HOME/sbin:\$PATH" >>~/.bashrc

source ~/.bashrc

cd $workdir

wget https://repo1.maven.org/maven2/org/apache/spark/spark-streaming-kafka-0-8-assembly_2.11/2.4.7/spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar

curl -L -O https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.10.1-linux-x86_64.tar.gz
tar -xzvf elasticsearch-7.10.1-linux-x86_64.tar.gz
rm elasticsearch-7.10.1-linux-x86_64.tar.gz

curl -L -O https://artifacts.elastic.co/downloads/kibana/kibana-7.10.1-linux-x86_64.tar.gz
tar xzvf kibana-7.10.1-linux-x86_64.tar.gz
rm kibana-7.10.1-linux-x86_64.tar.gz