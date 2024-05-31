FROM python:3.8-slim

# install deps
RUN apt-get update && apt-get -y install \
    bash ffmpeg

# setup real-esrgan
WORKDIR /real-esrgan
COPY . /real-esrgan
RUN pip3 install -r requirements.txt

# ADD docker/inference_img /usr/local/bin/inference_img
# RUN chmod +x /usr/local/bin/inference_img
# ADD docker/inference_video /usr/local/bin/inference_video
# RUN chmod +x /usr/local/bin/inference_video

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# add pre-trained models
# COPY train_log /rife/train_log
# COPY train_log /train_log
# COPY train_log /usr/local/bin/train_log

# WORKDIR /host
# ENTRYPOINT ["/bin/bash"]

ENV NVIDIA_DRIVER_CAPABILITIES all

RUN sed -i 's/from torchvision.transforms.functional_tensor import rgb_to_grayscale/from torchvision.transforms.functional import rgb_to_grayscale/' /usr/local/lib/python3.8/site-packages/basicsr/data/degradations.py

# Run app.py when the container launches
CMD ["python", "inference_realsrgan_video.py"]