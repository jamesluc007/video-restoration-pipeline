# Neural Style Transfer - Fast Neural Style Transfer with PyTorch

Neural Style Transfer is an AI model designed to apply artistic styles to images and videos. This README provides instructions to run the Fast Neural Style Transfer locally and create a Docker image for use in the Video Restoration Pipeline.

## Instructions to Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/pytorch/examples
   cd examples/fast_neural_style
   ```

2. **Create a Conda Environment**:
   ```bash
   conda create --name fast_neural_style python=3.8
   conda activate fast_neural_style
   ```

3. **Install PyTorch and CUDA**:
   Follow the instructions to install the latest Conda Torch version with PIP [here](https://pytorch.org/get-started/locally/). As of May 2024, the command is:
   ```bash
   pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
   ```

4. **Create Folders**:
   ```bash
   mkdir -p video/source
   ```

5. **Install Additional Requirements**:
   ```bash
   pip install opencv-python tqdm ffmpeg-python
   ```

6. **Add Custom Script**:
   - Add the script `inference_video.py` included in this repository to the `fast_neural_style` directory.

7. **Run Inference**:
   - Place your input video `input.mp4` in the `video/source` folder.
   - Download the pre-trained model `mosaic.pth` from the original neural style repository as per their instructions.
   ```bash
   python inference_video.py --file_name input.mp4 --model_name mosaic.pth
   ```

## Instructions to Create a Docker Image

1. **Add the Dockerfile**:
   - Use the Dockerfile included in this repository.

2. **Build the Docker Image**:
   ```bash
   docker build -t video-style-transfer .
   ```

3. **Run the Docker Container**:
   ```bash
   docker run -it --rm --gpus=all -v %cd%:/neural_style video-style-transfer python inference_video.py --file_name input.mp4 --model_name mosaic.pth
   ```

## Notes

- Ensure that you have NVIDIA Docker installed and configured to use GPU support.
- The `--model_name` flag in the `inference_video.py` command specifies the pre-trained model to use. Ensure the model file is downloaded and placed in the appropriate directory.

For any issues or support, please refer to the main repository or create an issue in this repository.