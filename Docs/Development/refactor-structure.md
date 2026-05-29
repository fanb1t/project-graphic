# Refactor Structure

เอกสารนี้สรุปโครงสร้างโปรเจกต์ปัจจุบันหลังปรับเป็น OOP และเริ่มใช้ Design Pattern

## โครงสร้างปัจจุบัน

```text
project-graphic/
├── main.py
├── README.md
├── requirements.txt
├── src/
│   ├── core/
│   │   ├── app.py
│   │   ├── asset_loader.py
│   │   ├── settings.py
│   │   └── state_manager.py
│   ├── data/
│   │   └── level_data.py
│   ├── entities/
│   │   ├── door.py
│   │   ├── elevator.py
│   │   ├── elevator_button.py
│   │   ├── key.py
│   │   ├── platform.py
│   │   └── player.py
│   ├── scenes/
│   │   ├── base_scene.py
│   │   ├── character_select.py
│   │   ├── instruction.py
│   │   ├── level_scene.py
│   │   ├── level_select.py
│   │   └── start_menu.py
│   └── systems/
│       ├── level_factory.py
│       └── ui.py
├── image/
└── Docs/
```

## สิ่งที่เปลี่ยนจากโครงสร้างเดิม

- ลบไฟล์ legacy และไฟล์ทดลองออกจาก root แล้ว
- `main.py` เหลือหน้าที่เป็น entry point เท่านั้น
- logic หลักย้ายเข้า `src/`
- object ของเกมแยกอยู่ใน `src/entities/`
- หน้าจอของเกมแยกอยู่ใน `src/scenes/`
- ข้อมูลด่านย้ายไปอยู่ใน `src/data/level_data.py`
- รูปภาพยังอยู่ใน `image/` และยังไม่ย้ายเพื่อเลี่ยงปัญหา path asset

## Design Pattern ที่ใช้

### State Pattern

ใช้ผ่าน `StateManager` ใน `src/core/state_manager.py`

แต่ละหน้าจอของเกมเป็น scene แยกกัน เช่น:

- `StartMenuScene`
- `InstructionScene`
- `CharacterSelectScene`
- `LevelSelectScene`
- `LevelScene`

ข้อดีคือ flow เกมไม่ต้องเรียกไฟล์ข้ามกันโดยตรงแบบเดิม

### Template Method

ใช้ใน `LevelScene`

ทุกด่านมีลำดับการทำงานคล้ายกัน:

1. โหลดข้อมูลด่าน
2. สร้าง object
3. รับ event
4. update object
5. ตรวจแพ้หรือชนะ
6. draw object

ถ้าจะเพิ่มด่านใหม่ สามารถใช้ `LevelScene` เดิมร่วมกับข้อมูลด่านใหม่ได้

### Factory Pattern

ใช้ใน `LevelFactory`

หน้าที่คือสร้าง `Player`, `Key`, `Door`, `Platform`, `Elevator` และ `ElevatorButton` จากข้อมูลใน `level_data.py`

### Asset Loader

ใช้ใน `AssetLoader`

หน้าที่คือโหลดและ cache รูปภาพจาก path เดียวกัน ลดการโหลดรูปซ้ำหลายจุด

## หน้าที่ของคลาสสำคัญ

### `GameApp`

เป็น application root ของเกม ดูแล Pygame window, clock, asset loader และ state manager

### `StateManager`

ดูแล scene ปัจจุบันและเปลี่ยน scene เช่น จาก menu ไป character select หรือจาก level select ไป level

### `BaseScene`

เป็น interface กลางของทุก scene มีเมธอด `handle_events()`, `update()` และ `draw()`

### `LevelScene`

เป็น scene สำหรับเล่นด่าน ใช้ข้อมูลด่านจาก `level_data.py` และสร้าง object ผ่าน `LevelFactory`

### `LevelFactory`

สร้าง object ของด่านจากข้อมูล config

### `Player`

ดูแลการเดิน กระโดด gravity collision และการเก็บกุญแจ

### `Key`

เป็นกุญแจของด่าน เมื่อถูกเก็บจะตามผู้เล่น

### `Door`

ตรวจว่าผู้เล่นที่ถือกุญแจชนประตูหรือไม่

### `Platform`

ใช้แทนพื้น กล่อง หรือ hazard ที่มีรูปและ hitbox เป็นสี่เหลี่ยม

### `Elevator`

เป็น platform ที่เคลื่อนที่ได้ตามสถานะของปุ่ม

### `ElevatorButton`

ตรวจว่าผู้เล่นคนใดยืนทับปุ่มอยู่หรือไม่

## งานต่อยอดที่แนะนำ

- เชื่อมด่าน 3 เข้ากับ scene ใหม่
- เพิ่ม Pause Scene
- เพิ่ม Game Over Scene แทนการแสดงข้อความใน `LevelScene`
- เพิ่มระบบเสียงและเอฟเฟกต์
- เพิ่ม tests หรือ smoke test script
- ย้าย `image/` เป็น `assets/` หลังแก้ path ครบ
