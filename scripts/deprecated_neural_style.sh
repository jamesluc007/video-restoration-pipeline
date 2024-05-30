#!/bin/bash
if [ "$RUN_NEURAL_STYLE" = "true" ]; then
  python inference_video.py --file_name video.mp4 --model_name "$NEURAL_MODEL"
else
  echo 'Skipping Neural Style'
fi