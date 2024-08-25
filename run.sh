#!/bin/bash

# Check if the virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Virtual environment not activated. Activating now..."
    source ~/orderdrinks-hw/venv/bin/activate
else
  echo "Virtual environment is already activated."
fi

# Check if the Docker container "inference_server" is running
if ! sudo docker ps | grep -q "inference_server"; then
    echo "Starting the 'inference_server' container..."
    sudo docker run -d --rm -p 9001:9001 --name inference_server roboflow/roboflow-inference-server-arm-cpu
else
  echo "'inference_server' container is already running."
fi

# Check if "confidence_threshold" in config.yaml is set to exactly 0
if grep -q 'confidence_threshold: 0$' config.yaml; then
    echo "You need to set up confidence_threshold first."
    exit 1
fi

# Check if the 'gpsd' service is not running
if ! systemctl is-active --quiet gpsd; then
    echo "Starting the 'gpsd' service..."
    sudo systemctl start gpsd
    sudo systemctl enable gpsd
    echo "'gpsd' service started and enabled to start on boot."
else
    echo "'gpsd' service is already running."
fi

# Run the main script
python3 main.py