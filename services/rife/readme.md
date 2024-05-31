# RIFE - Real-Time Intermediate Flow Estimation

RIFE is a video interpolation model designed to increase the frame rate of videos by estimating intermediate frames. This README provides instructions to run RIFE locally and create a Docker image for use in the Video Restoration Pipeline.

## Instructions to Run Locally

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hzwer/ECCV2022
   cd ECCV2022
   ```

2. **Install PyTorch**:
   Follow the instructions to install the latest stable PyTorch version [here](https://pytorch.org/get-started/locally/).

3. **Create a Conda Environment**:
   ```bash
   conda create -n rife python=3.9
   conda activate rife
   ```

4. **Install Requirements**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Download Weights**:
   Manually download the weights and place them in the `./train_log` directory. Follow the instructions in the RIFE repository's README.

6. **Run Inference**:
   ```bash
   python inference_video.py --exp=2 --video=video.mp4
   ```

## Instructions to Create a Docker Image

1. **Add the Dockerfile**:
   Use the Dockerfile included in this repository (not the one from the RIFE repo as it is intended for Linux).

2. **Build the Docker Image**:
   ```bash
   docker build -t rife .
   ```

3. **Run the Docker Container**:
   ```bash
   docker run -it --rm --gpus=all -v %cd%:/rife rife-container python3 inference_video.py --video /rife/input_videos/input.mp4 --output /rife/output_videos/output.mp4
   ```

## Notes

- Ensure that you have NVIDIA Docker installed and configured to use GPU support.
- The `--exp` flag in the `inference_video.py` command specifies the interpolation factor. Adjust it according to your needs.

For any issues or support, please refer to the main repository or create an issue in this repository.
