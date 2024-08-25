#!/bin/bash
set -e

log_message() {
    echo "$(date): $1"
}

log_message "กำลังอัปเดตระบบ..."
sudo apt-get update
sudo apt-get upgrade -y

log_message "กำลังติดตั้ง Docker..."
if ! curl -fsSL https://get.docker.com -o get-docker.sh; then
    log_message "ไม่สามารถดาวน์โหลดสคริปต์ติดตั้ง Docker ได้"
    exit 1
fi

if ! sudo sh get-docker.sh; then
    log_message "เกิดข้อผิดพลาดในการติดตั้ง Docker"
    exit 1
fi

sudo usermod -aG docker $USER
newgrp docker

rm get-docker.sh

log_message "กำลังรัน inference-server container..."
if ! sudo docker run -d --rm -p 9001:9001 --name inference_server roboflow/roboflow-inference-server-arm-cpu; then
    log_message "ไม่สามารถรัน inference-server container ได้"
    exit 1
fi

log_message "Inference server กำลังทำงานบนพอร์ต 9001"