FROM ubuntu:18.04
# FROM python:3.7
WORKDIR /app
COPY . /app

# RUN groupadd -g 999 appuser && \
#     useradd -r -u 999 -g appuser appuser
RUN useradd -ms /bin/bash appuser

RUN apt-get update\
    && apt-get install python3.7 -y\
    && apt-get install python3-pip -y\
    && apt-get install wget -y\
    && apt-get install curl -y
RUN ln -s /usr/bin/python3 /usr/bin/python
# RUN python get-pip.py
# && pip install -r requirements.txt \
# && bash install.sh
RUN chown -R appuser:appuser /app
RUN chmod 755 /app
USER appuser
RUN pip3 install -r requirements.txt
RUN bash install.sh

# RUN echo "PYTHONPATH=/usr/lib/python3.7" >> ~/.bashrc
# RUN /bin/bash -c "source ~/.bashrc"
# RUN apt-get install python3
# RUN pip install -r requirements.txt
# RUN bash install.sh
CMD ["python3","run.py"]