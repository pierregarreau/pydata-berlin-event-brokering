FROM python:3.6

# install build dependencies
RUN apt-get update -y

# install app dependencies
RUN pip install numpy
RUN pip install scipy

# Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# add app code
ADD . /rasberry
WORKDIR /rasberry
