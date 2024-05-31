# Real-ESRGAN - Enhanced Super-Resolution Generative Adversarial Networks

Real-ESRGAN is an AI model designed for high-quality image and video super-resolution. This README provides instructions to run Real-ESRGAN locally and create a Docker image for use in the Video Restoration Pipeline.

## Instructions to Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/xinntao/Real-ESRGAN
   cd Real-ESRGAN
   ```

2. **Create a Conda Environment**:
   ```bash
   conda create -n esrgan python=3.8
   conda activate esrgan
   ```

3. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Install PyTorch and CUDA**:
   Follow the instructions to install the latest Conda Torch version [here](https://pytorch.org/get-started/locally/). As of May 2024, the command is:
   ```bash
   conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
   ```

5. **Install Additional Requirements**:
   ```bash
   pip install ffmpeg
   ```

6. **Setup the Environment**:
   ```bash
   python setup.py develop
   ```

7. **Install `chardet`**:
   ```bash
   pip install chardet
   ```

8. **Optional Fix**:
   If you encounter issues, you may need to revise line 8 of the file `degradations.py`. Refer to this [issue explanation](https://github.com/xinntao/Real-ESRGAN/issues/765) for more details.

9. **Run Inference**:
   - Place your input video `input.mp4` in the appropriate folder.
   ```bash
   python inference_realesrgan_video.py -n RealESRGAN_x4plus -i input.mp4 --outscale 4.0
   ```

## Instructions to Create a Docker Image

1. **Add the Dockerfile**:
   - Use the Dockerfile included in this repository.

2. **Build the Docker Image**:
   ```bash
   docker build -t esrgan .
   ```

3. **Run the Docker Container**:
   ```bash
   docker run -it --rm --gpus=all -v %cd%:/video/source esrgan python inference_realesrgan_video.py -i /video/source/video.mp4 -n RealESRGAN_x4plus --outscale 4.0
   ```

## Notes

- Ensure that you have NVIDIA Docker installed and configured to use GPU support.
- The `--outscale` flag in the `inference_realesrgan_video.py` command adjusts the upscaling factor. Higher values will increase the resolution proportionally.

For any issues or support, please refer to the main repository or create an issue in this repository.