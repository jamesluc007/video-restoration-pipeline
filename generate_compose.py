import os

# Define the default volumes
volumes = {
    "rife_input": "./video/source:/video/source",
    "rife_output": "./video/intermediate_1:/video/result",
    "deoldify_input": "./video/intermediate_1:/video/source",
    "deoldify_output": "./video/intermediate_2:/video/result",
    "neural_style_input": "./video/intermediate_2:/video/source",
    "neural_style_output": "./video/intermediate_3:/video/result",
    "esrgan_input": "./video/intermediate_3:/video/source",
    "esrgan_output": "./video/result:/video/results"
}

# Adjust volumes based on environment variables
if os.getenv("RUN_RIFE") == "false":
    volumes["deoldify_input"] = "./video/source:/video/source"

if os.getenv("RUN_DEOLDIFY") == "false" and os.getenv("RUN_RIFE") == "false":
    volumes["neural_style_input"] = "./video/source:/video/source"
elif os.getenv("RUN_DEOLDIFY") == "false":
    volumes["neural_style_input"] = "./video/intermediate_1:/video/source"

if os.getenv("RUN_NEURAL_STYLE") == "false" and os.getenv("RUN_DEOLDIFY") == "false" and os.getenv("RUN_RIFE") == "false":
    volumes["esrgan_input"] = "./video/source:/video/source"
elif os.getenv("RUN_NEURAL_STYLE") == "false" and os.getenv("RUN_DEOLDIFY") == "false":
    volumes["esrgan_input"] = "./video/intermediate_1:/video/source"
elif os.getenv("RUN_NEURAL_STYLE") == "false":
    volumes["esrgan_input"] = "./video/intermediate_2:/video/source"

# Generate the docker-compose.yml content
docker_compose_content = f"""
version: '3.8'
services:
  rife-ai:
    image: rife-container
    container_name: rife_ai
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - RUN_RIFE={os.getenv("RUN_RIFE", "true")}
    volumes:
      - {volumes["rife_input"]}
      - {volumes["rife_output"]}
      - ./scripts:/scripts
    command: bash /scripts/rife.sh
    tty: true
    stdin_open: true
    restart: no

  deoldify:
    image: deoldify
    container_name: deoldify
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - RUN_DEOLDIFY={os.getenv("RUN_DEOLDIFY", "true")}
    volumes:
      - {volumes["deoldify_input"]}
      - {volumes["deoldify_output"]}
      - ./scripts:/scripts
    command: bash /scripts/deoldify.sh
    tty: true
    stdin_open: true
    restart: no

  neural_style:
    image: video-style-transfer
    container_name: neural_style
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - RUN_NEURAL_STYLE={os.getenv("RUN_NEURAL_STYLE", "true")}
    volumes:
      - {volumes["neural_style_input"]}
      - {volumes["neural_style_output"]}
      - ./scripts:/scripts
    command: bash /scripts/neural_style.sh
    tty: true
    stdin_open: true
    restart: no

  esrgan:
    image: esrgan
    container_name: esrgan
    environment:
      - NVIDIA_VISIBLE_DEVICES=all
      - RUN_ESRGAN={os.getenv("RUN_ESRGAN", "true")}
    volumes:
      - {volumes["esrgan_input"]}
      - {volumes["esrgan_output"]}
      - ./scripts:/scripts
    command: bash /scripts/esrgan.sh
    tty: true
    stdin_open: true
    restart: no
"""

# Write the content to docker-compose.yml
with open("docker-compose.yml", "w") as f:
    f.write(docker_compose_content)

print("docker-compose.yml has been generated.")
