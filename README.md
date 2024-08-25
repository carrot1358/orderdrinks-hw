# ส่วนประกอบของโครงการ

### Git สำหรับเว็บแอพพลิเคชัน : [คลิก](https://gitlab.eng.rmuti.ac.th/orapan.ya/orderdrink.git)

### Git สำหรับ Hardware(Raspberry Pi) : [คลิก](https://gitlab.eng.rmuti.ac.th/nattapad.sa/orderdrinks-hw.git) (คุณอยู่ที่นี่)

## จัดเตรียมฝั่ง Raspberry pi
### - เตรียมสภาพแวดล้อมบน Raspberry pi.
1. เปิดใช้งาน Serial Comunication
    ```
    sudo raspi-config
    ```
    เลือก Interface Option > Serial Port
    - Would you like a login sheel to be accessible over serial  `<NO>`
    - Would you like the serial port hardware to be enabled `<Yes>`
    
    reboot


### - เตรียม Code สำหรับ Raspbery pi

1. โคลนโปรเจค
    ```bash
   git clone
   cd BootleDetect 
   ```
2. setup โปรเจค
    ```
    chmod +x setup_all.sh
    ./setup_all.sh
    ```

## การใช้งาน
1. แก้ไข config `orderdrinks-hw/config.yaml`

2. รันโปรแกรม
   ```bash
   chmod +x run.sh
   ./run.sh
   ```
