# Poonny Moony

Poonny Moony เป็นเกม 2D cooperative platformer ที่พัฒนาด้วย Python และ Pygame ผู้เล่น 2 คนต้องช่วยกันผ่านด่าน เก็บกุญแจ หลบสิ่งกีดขวาง ใช้กลไกในด่าน เช่น ลิฟต์และปุ่มกด แล้วเข้าประตูเพื่อไปด่านถัดไป

## ภาพรวมเกม

เกมนี้เป็น local two-player game ที่เล่นบนเครื่องเดียวกัน ผู้เล่น 1 ใช้ปุ่ม `A`, `W`, `D` และผู้เล่น 2 ใช้ปุ่มลูกศร เป้าหมายหลักคือร่วมมือกันผ่านด่าน เก็บกุญแจ และหลีกเลี่ยง hazard เช่น ลาวา

โครงสร้างโค้ดปัจจุบันถูกปรับเป็น OOP และแบ่งเป็น `src/core`, `src/scenes`, `src/entities`, `src/systems` และ `src/data` เพื่อให้ดูแลต่อได้ง่ายขึ้น

## สารบัญเอกสารเกม

- [รายละเอียดโปรเจกต์](Docs/project-details.md) แนวคิด ประเภทเกม โครงสร้างไฟล์ และเครดิต asset
- [วิธีการเล่น](Docs/gameplay.md) ปุ่มควบคุม เป้าหมาย เงื่อนไขชนะ/แพ้ และวิธีรันเกม
- [สารบัญเอกสาร](Docs/README.md) รายการเอกสารทั้งหมดในโฟลเดอร์ `Docs`

## สารบัญเอกสารการพัฒนา

- [ภาพรวมโครงสร้างหลัง refactor](Docs/Development/refactor-structure.md)
- [Design Pattern ในโปรเจกต์](Docs/Development/design-patterns.md)
- [ภาพรวมระบบและ Use Cases](Docs/Development/system-overview-use-cases.md)
- [อธิบายการทำงานของโค้ด](Docs/Development/code-explanation.md)
- [สารบัญการพัฒนา](Docs/Development/README.md)

## โครงสร้างโปรเจกต์

```text
project-graphic/
├── main.py
├── README.md
├── requirements.txt
├── src/
│   ├── core/
│   ├── data/
│   ├── entities/
│   ├── scenes/
│   └── systems/
├── image/
└── Docs/
```

## การติดตั้งและใช้งาน

หมายเหตุ: โฟลเดอร์ `image/` เป็น asset ของเกมและไม่ได้ถูก push ขึ้น GitHub ต้องมีโฟลเดอร์นี้อยู่ในเครื่องก่อนรันเกม

### 1. เตรียม Python

แนะนำให้ใช้ Python 3.12 หรือใกล้เคียง ตรวจสอบเวอร์ชันด้วยคำสั่ง:

```powershell
python --version
```

### 2. เข้าโฟลเดอร์โปรเจกต์

```powershell
cd project-graphic
```

### 3. ติดตั้ง dependency

```powershell
pip install -r requirements.txt
```

### 4. รันเกม

```powershell
python main.py
```

ถ้าหน้าต่างเกมเปิดขึ้นมา แปลว่าโปรแกรมเริ่มทำงานแล้ว ให้ปิดหน้าต่างเกมเมื่อต้องการหยุดโปรแกรม

## Design Pattern ที่ใช้

- State Pattern สำหรับจัดการหน้าจอเกมผ่าน `StateManager`
- Template Method สำหรับ flow ของด่านผ่าน `LevelScene`
- Factory Pattern สำหรับสร้าง object ในด่านผ่าน `LevelFactory`
- Asset Loader สำหรับโหลดและ cache รูปภาพ
