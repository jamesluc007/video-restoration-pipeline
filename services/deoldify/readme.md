# DeOldify - Colorizing and Restoring Old Images and Videos

DeOldify is an AI model designed to colorize and restore old black and white images and videos. This README provides instructions to run DeOldify locally and create a Docker image for use in the Video Restoration Pipeline.

## Instructions to Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/jantic/DeOldify
   cd DeOldify
   ```

2. **Create a Conda Environment**:
   ```bash
   conda create --name deoldify python=3.8
   conda activate deoldify
   ```

3. **Install PyTorch and CUDA**:
   ```bash
   conda install pytorch torchvision cudatoolkit=10.1 -c pytorch
   ```

4. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Add Custom Script**:
   - Add the script `colorize_video.py` included in this repository to the DeOldify directory.

6. **Run Inference**:
   - Place your input video `input.mp4` in the `./video/source` folder.
   ```bash
   python colorize_video.py --file_name input.mp4 --render_factor 21
   ```

## Instructions to Create a Docker Image

**Special Mention**: This was VERY difficult and took many hours to achieve.

1. **Add the Dockerfile**:
   - Use the Dockerfile included in this repository.

2. **Add the Requirements File**:
   - Use the `requirements-colab` file included in this repository.

3. **Build the Docker Image**:
   ```bash
   docker build -t deoldify .
   ```

4. **Run the Docker Container**:
   ```bash
   docker run -it --rm --gpus=all -v %cd%:/deoldify deoldify python colorize_video.py --file_name input.mp4 --render_factor 21
   ```

## Notes

- Ensure that you have NVIDIA Docker installed and configured to use GPU support.
- The `--render_factor` flag in the `colorize_video.py` command adjusts the rendering quality. Higher values generally produce better results but may require more memory and processing power.

For any issues or support, please refer to the main repository or create an issue in this repository.