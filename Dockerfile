FROM python:3.8-slim
COPY . .
RUN apt-get update \
    && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip \
    && pip install -r req.txt
CMD python run.py
