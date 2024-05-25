#!/bin/bash
if [ "$RUN_DEOLDIFY" = "true" ]; then
  python colorize_video.py --file_name video.mp4 --render_factor 30
else
  echo 'Skipping DeOldify'
fi