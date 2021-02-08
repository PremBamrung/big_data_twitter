import os

os.system("pkill -f kibana -9 &")
os.system("pkill -f elasticsearch -9 &")
os.system("pkill -f kafka -9 &")
os.system("pkill -f zookeeper -9")
