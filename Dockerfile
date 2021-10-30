FROM ubuntu:18.04
WORKDIR /app


RUN apt update -y && apt upgrade -y
RUN apt install -y python3
RUN apt install -y python3-dev python3-pip python3-setuptools
RUN python3 -m pip install --upgrade pip setuptools
RUN python3 -m pip install scikit-build numpy
RUN python3 -m pip install opencv-python
RUN python3 -m pip install opencv-contrib-python
RUN apt-get install -y libgl1-mesa-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY app .
CMD ["python3", "main.py"]