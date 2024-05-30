import argparse
from deoldify import device
from deoldify.device_id import DeviceId

import os

# Configurar dispositivo    
device.set(device=DeviceId.GPU0)

import torch

import fastai
from deoldify.visualize import *
from pathlib import Path
torch.backends.cudnn.benchmark=True

def check_cuda():
    print("Is CUDA available in PyTorch:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("Number of CUDA devices:", torch.cuda.device_count())
        for i in range(torch.cuda.device_count()):
            print("CUDA Device #{}: {}".format(i, torch.cuda.get_device_name(i)))

def colorize_video(file_name, render_factor, output_name):
    check_cuda()
    colorizer = get_video_colorizer()

    # Colorea el video
    colorizer.colorize_from_file_name(
        file_name=file_name,
        render_factor=render_factor,
        watermarked=False,
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Colorize black and white videos using DeOldify.")
    parser.add_argument('--file_name', type=str, required=True, help="Path to the black and white video file.")
    parser.add_argument('--render_factor', type=int, default=21, help="Render factor for colorization (1-44). Higher values result in more vibrant colors.")
    parser.add_argument('--output_name', type=str, default="output.mp4", help="Name of the output colored video file.")
    
    args = parser.parse_args()
    
    colorize_video(args.file_name, args.render_factor, args.output_name)