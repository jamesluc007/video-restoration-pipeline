#!/bin/bash

# Set default volumes (All models are used scenario)
RIFE_INPUT_VOLUME='./video/source:/video/source'
RIFE_OUTPUT_VOLUME='./video/intermediate_1:/video/result'
DEOLDIFY_INPUT_VOLUME='./video/intermediate_1:/video/source'
DEOLDIFY_OUTPUT_VOLUME='./video/intermediate_2:/video/result'
NEURAL_STYLE_INPUT_VOLUME='./video/intermediate_2:/video/source'
NEURAL_STYLE_OUTPUT_VOLUME='./video/intermediate_3:/video/result'
ESRGAN_INPUT_VOLUME='./video/intermediate_3:/video/source'
ESRGAN_OUTPUT_VOLUME='./video/result:/results'

# Adjust volumes based on environment variables
if [ "$RUN_RIFE" = "false" ]; then
  DEOLDIFY_INPUT_VOLUME='./video/source:/video/source'
fi

if [ "$RUN_DEOLDIFY" = "false" ] && [ "$RUN_RIFE" = "false" ]; then
  NEURAL_STYLE_INPUT_VOLUME='./video/source:/video/source'
elif [ "$RUN_DEOLDIFY" = "false" ]; then
  NEURAL_STYLE_INPUT_VOLUME='./video/intermediate_1:/video/source'
fi

if [ "$RUN_NEURAL_STYLE" = "false" ] && [ "$RUN_DEOLDIFY" = "false" ] && [ "$RUN_RIFE" = "false" ]; then
  ESRGAN_INPUT_VOLUME='./video/source:/video/source'
elif [ "$RUN_NEURAL_STYLE" = "false" ] && [ "$RUN_DEOLDIFY" = "false" ]; then
  ESRGAN_INPUT_VOLUME='./video/intermediate_1:/video/source'
elif [ "$RUN_NEURAL_STYLE" = "false" ]; then
  ESRGAN_INPUT_VOLUME='./video/intermediate_2:/video/source'
fi

# Export variables for use in the template
export RIFE_INPUT_VOLUME
export RIFE_OUTPUT_VOLUME
export DEOLDIFY_INPUT_VOLUME
export DEOLDIFY_OUTPUT_VOLUME
export NEURAL_STYLE_INPUT_VOLUME
export NEURAL_STYLE_OUTPUT_VOLUME
export ESRGAN_INPUT_VOLUME
export ESRGAN_OUTPUT_VOLUME

# Generate docker-compose.yml from the template
envsubst < docker-compose-template.yaml > docker-compose.yml
