#!/bin/bash
set -e

log_message() {
    echo "$(date): $1"
}

log_message "กำลังดาวน์โหลด Comitup apt source package..."
if ! wget https://davesteele.github.io/comitup/deb/davesteele-comitup-apt-source_1.2_all.deb; then
    log_message "เกิดข้อผิดพลาดในการดาวน์โหลด Comitup package"
    exit 1
fi

log_message "กำลังติดตั้ง Comitup package..."
if ! sudo dpkg -i davesteele-comitup-apt-source_1.2_all.deb; then
    log_message "เกิดข้อผิดพลาดในการติดตั้ง Comitup package"
    exit 1
fi

log_message "กำลังอัปเดตรายการแพ็คเกจ..."
sudo apt-get update

log_message "กำลังติดตั้ง Comitup..."
if ! sudo apt-get install -y comitup; then
    log_message "เกิดข้อผิดพลาดในการติดตั้ง Comitup"
    exit 1
fi

log_message "กำลังลบไฟล์ network interfaces..."
sudo rm -f /etc/network/interfaces

log_message "กำลังลบ Comitup api source package..."
sudo rm -f davesteele-comitup-apt-source_1.2_all.deb

log_message "กำลังปิดการใช้งานบริการเครือข่ายต่างๆ..."
services=("dnsmasq.service" "systemd-resolved.service" "dhcpd.service" "dhcpcd.service" "wpa-supplicant.service")
for service in "${services[@]}"; do
    if ! sudo systemctl mask $service; then
        log_message "ไม่สามารถปิดการใช้งาน $service ได้"
    fi
done

log_message "กำลังเปิดใช้งาน NetworkManager..."
if ! sudo systemctl enable NetworkManager.service; then
    log_message "ไม่สามารถเปิดใช้งาน NetworkManager ได้"
    exit 1
fi

log_message "กำลังสร้างไฟล์ SSH ว่างเปล่าใน boot directory..."
sudo touch /boot/ssh

log_message "การติดตั้ง Comitup เสร็จสมบูรณ์"