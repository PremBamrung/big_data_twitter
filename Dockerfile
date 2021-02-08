FROM ubuntu:18.04
# FROM python:3.7

RUN useradd -ms /bin/bash appuser
WORKDIR /home/appuser/app
COPY . /home/appuser/app
RUN chown -R appuser:appuser /home/appuser/app
RUN chmod 755 /home/appuser/app
# RUN groupadd -g 999 appuser && \
#     useradd -r -u 999 -g appuser appuser


RUN apt-get update\
    && apt-get install python3.7 -y\
    && apt-get install python3-pip -y\
    && apt-get install wget -y\
    && apt-get install curl -y

RUN ln -s /usr/bin/python3 /usr/bin/python


USER appuser
RUN pip3 install -r requirements.txt
RUN bash install.sh

# RUN echo "PYTHONPATH=/usr/lib/python3.7" >> ~/.bashrc
# RUN /bin/bash -c "source ~/.bashrc"
# RUN apt-get install python3
# RUN pip install -r requirements.txt
# RUN bash install.sh
CMD ["python","run.py"]