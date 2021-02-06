import os
import time

os.system("python3 launch_serveur.py &")
time.sleep(30)
os.system("python3 producer.py &")
time.sleep(5)
os.system("python3 spark_streaming.py &")
time.sleep(3)
