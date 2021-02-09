workdir=$(pwd)
rm -rf ~/logiciels/
cd
cp .bashrc .bashrc_bak
rm .bashrc
head -n -12 .bashrc_bak >> .bashrc
cd $workdir
rm -rf  spark-streaming-kafka-0-8-assembly_2.11-2.4.7.jar elasticsearch-7.10.1/ kibana-7.10.1-linux-x86_64/
