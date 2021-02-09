sudo docker run -it   --name stream_tweet_cnt --user appuser --net=host stream_tweet_im python run_app.py


#create and enter inside the docker as appuser
#sudo docker run -it   --name stream_tweet_cnt --user appuser --net=host stream_tweet_im /bin/bash

# enter inside docker already running
#sudo docker exec -it stream_tweet_cnt   /bin/bash
# sudo docker exec -it stream_tweet_cnt  -u root /bin/bash
