# Usa la imagen base de NVIDIA CUDA
#FROM python:3.8-slim
# FROM python:3.8-slim
# FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu20.04
# FROM nvidia/cuda:12.4.1-cudnn-runtime-ubuntu20.04
FROM nvidia/cuda:12.1.0-runtime-ubuntu18.04
# FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

# Instala dependencias necesarias
# RUN apt-get update && apt-get install -y git
#RUN apt-get update && apt-get -y install \
#    ffmpeg
# RUN apt-get update && apt-get install bash ffmpeg libsm6 libxext6  -y
# install deps
RUN apt-get update && apt-get -y install \
    bash ffmpeg

# bash

# Copia el repositorio de DeOldify al contenedor
# RUN git clone https://github.com/jantic/DeOldify.git /DeOldify
WORKDIR /deoldify
COPY . /deoldify

# install anaconda
RUN apt-get update
RUN apt-get install -y wget bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git mercurial subversion && \
        apt-get clean
RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh -O ~/anaconda.sh && \
        /bin/bash ~/anaconda.sh -b -p /opt/conda && \
        rm ~/anaconda.sh && \
        ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
        echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
        find /opt/conda/ -follow -type f -name '*.a' -delete && \
        find /opt/conda/ -follow -type f -name '*.js.map' -delete && \
        /opt/conda/bin/conda clean -afy

# set path to conda
ENV PATH /opt/conda/bin:$PATH

# RUN conda update conda \
#     && conda create --name deoldify python=3.8
    
# -f environment.yml


RUN echo "conda activate deoldify" >> ~/.bashrc
ENV PATH /opt/conda/envs/deoldify/bin:$PATH
ENV CONDA_DEFAULT_ENV $deoldify

RUN conda init bash \
    && . ~/.bashrc \
    && conda env create -f environment.yml \
    # && conda create --name deoldify python=3.8 \
    && conda activate deoldify \
    # && conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cudatoolkit=10.1 -c pytorch \
    && conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia \
    && pip install -r requirements-colab.txt

# Could also use this one
# https://stackoverflow.com/questions/65686462/use-gpu-on-python-docker-image
# Make port 80 available to the world outside this container
EXPOSE 90

# Define environment variable
ENV NAME World2

# Crea los directorios para videos de entrada y salida
# RUN mkdir -p /video/source /video/result

ENV NVIDIA_DRIVER_CAPABILITIES all

# Comando para ejecutar el script de colorización
CMD ["python", "colorize_video.py"]