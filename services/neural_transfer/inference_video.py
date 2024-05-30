import argparse
import os
import sys
import cv2
import re
import torch
import numpy as np
from torchvision import transforms
from neural_style.transformer_net import TransformerNet
import neural_style.utils
from tqdm import tqdm
import ffmpeg
from PIL import Image

def extract_frames(video_path, frames_dir):
    if not os.path.exists(frames_dir):
        os.makedirs(frames_dir)
    
    (
        ffmpeg
        .input(video_path)
        .output(os.path.join(frames_dir, 'frame_%04d.png'), start_number=0)
        .run()
    )

def create_video(frames_dir, output_video_path, fps):
    (
        ffmpeg
        .input(os.path.join(frames_dir, 'frame_%04d.png'), framerate=fps, start_number=0)
        .output(output_video_path, vcodec='libx264', crf=18, pix_fmt='yuv420p')
        .run()
    )

def stylize_frames(frames_dir, output_frames_dir, model_path, device):
    if not os.path.exists(output_frames_dir):
        os.makedirs(output_frames_dir)

    # Load the model
    style_model = TransformerNet()
    state_dict = torch.load(model_path, map_location=device)
    for k in list(state_dict.keys()):
        if re.search(r'in\d+\.running_(mean|var)$', k):
            del state_dict[k]
    style_model.load_state_dict(state_dict)
    style_model.to(device)
    style_model.eval()

    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])

    frame_files = sorted([f for f in os.listdir(frames_dir) if f.startswith('frame_') and f.endswith('.png')])
    for frame_file in tqdm(frame_files, desc="Processing frames"):
        frame_path = os.path.join(frames_dir, frame_file)
        frame = Image.open(frame_path).convert('RGB')
        frame = transform(frame).unsqueeze(0).to(device)

        with torch.no_grad():
            output = style_model(frame).cpu().squeeze(0)
        
        output = transforms.ToPILImage()(output.div(255.0).clamp(0, 1))
        output.save(os.path.join(output_frames_dir, frame_file))

def stylize_video(args):
    device = torch.device("cuda" if args.cuda else "cpu")
    
    input_video_path = os.path.join('./video/source', args.file_name)
    frames_dir = './video/frames'
    output_frames_dir = './video/output_frames'
    output_video_path = os.path.join('./video/result', f'stylized_{args.file_name}')
    
    # Extract frames from the video
    extract_frames(input_video_path, frames_dir)
    
    # Get FPS of the input video
    probe = ffmpeg.probe(input_video_path)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    fps = eval(video_stream['r_frame_rate'])

    # Stylize each frame
    stylize_frames(frames_dir, output_frames_dir, os.path.join('./saved_models', args.model_name), device)
    
    # Create a video from the stylized frames
    create_video(output_frames_dir, output_video_path, fps)
    
    print(f'Stylized video saved to {output_video_path}')

def main():
    parser = argparse.ArgumentParser(description="Video Style Transfer")
    parser.add_argument('--file_name', type=str, required=True, help='Name of the video file in ./video/source/')
    parser.add_argument('--model_name', type=str, required=True, help='Name of the model file in ./models/')
    parser.add_argument('--cuda', type=int, default=1, help='Set it to 1 for running on GPU, 0 for CPU')
    args = parser.parse_args()

    if args.cuda and not torch.cuda.is_available():
        print("ERROR: cuda is not available, try running on CPU")
        sys.exit(1)

    stylize_video(args)

if __name__ == "__main__":
    main()