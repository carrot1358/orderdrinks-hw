#!/bin/bash
set -e

log_message() {
    echo "$(date): $1"
}

log_message "เริ่มการสร้าง virtual environment..."

# Create a virtual environment with system site packages
python3 -m venv --system-site-packages ~/orderdrinks-hw/venv

# Wait until the virtual environment is created
while [ ! -f ~/orderdrinks-hw/venv/bin/activate ]; do
    sleep 1
done

# Activate the virtual environment
source ~/orderdrinks-hw/venv/bin/activate

log_message "กำลังติดตั้งแพ็คเกจที่จำเป็น..."

pip install gps==3.22 pyyaml==6.0.2 roboflow websocket-client==1.8.0 opencv-python pynmea2

if ! sudo apt-get install -y gpsd gpsd-clients; then
    log_message "เกิดข้อผิดพลาดในการติดตั้ง gpsd และ gpsd-clients"
    exit 1
fi

log_message "สร้างและเปิดใช้งาน virtual environment เรียบร้อยแล้ว"