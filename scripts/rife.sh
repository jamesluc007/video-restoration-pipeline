#!/bin/bash
if [ "$RUN_RIFE" = "true" ]; then
  python inference_video.py --video /video/source/video.mp4 --output /video/result/video.mp4
else
  echo 'Skipping RIFE'
fi