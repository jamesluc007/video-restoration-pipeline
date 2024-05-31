FROM python:3.8-slim

# install deps
RUN apt-get update && apt-get -y install \
    bash ffmpeg

# setup RIFE
WORKDIR /rife
COPY . /rife
RUN pip3 install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

ENV NVIDIA_DRIVER_CAPABILITIES all

# Run app.py when the container launches
CMD ["python", "inference_video.py"]