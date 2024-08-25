#!/bin/bash
set -e  # หยุดทันทีถ้ามีคำสั่งใดผิดพลาด

log_message() {
    echo "$(date): $1"
}

cd setup/

log_message "เริ่มการติดตั้งสภาพแวดล้อม..."
chmod +x setup_environment.sh
./setup_environment.sh
log_message "ติดตั้งสภาพแวดล้อมเสร็จสิ้น"

log_message "เริ่มการติดตั้ง Comitup..."
chmod +x setup_comitup.sh
./setup_comitup.sh
log_message "ติดตั้ง Comitup เสร็จสิ้น"

log_message "เริ่มการติดตั้ง Inference Server..."
chmod +x setup_Inferance-Server.sh
./setup_Inferance-Server.sh
log_message "ติดตั้ง Inference Server เสร็จสิ้น"

log_message "การติดตั้งทั้งหมดเสร็จสิ้น"