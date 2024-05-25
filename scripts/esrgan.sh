#!/bin/bash
if [ "$RUN_RIFE" = "true" ]; then
  python inference_realesrgan_video.py -i /video/source/video.mp4 -n RealESRGAN_x4plus --outscale "$ESRGAN_OUTSCALE"
else
  echo 'Skipping ESRGAN'
fi