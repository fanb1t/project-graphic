# Design Patterns In Poonny Moony

เอกสารนี้อธิบาย Design Pattern ที่ใช้ในโปรเจกต์ Poonny Moony หลังปรับโครงสร้างเป็น OOP

## ภาพรวม

โปรเจกต์นี้ใช้ pattern หลัก 4 แบบ:

- State Pattern
- Template Method Pattern
- Factory Pattern
- Asset Loader แบบ shared service

Pattern เหล่านี้ช่วยลดการเรียกไฟล์ข้ามกันโดยตรง ลดโค้ดซ้ำ และทำให้เพิ่มด่านหรือหน้าจอใหม่ได้ง่ายขึ้น

## 1. State Pattern

### ใช้ที่ไหน

- `src/core/state_manager.py`
- `src/scenes/`

### แนวคิด

เกมมีหลายสถานะ เช่น เมนูหลัก หน้าเลือกตัวละคร หน้าเลือกด่าน และหน้าด่าน แทนที่จะเขียน loop แยกในแต่ละไฟล์แล้วเรียกกันไปมา โปรเจกต์นี้ใช้ `StateManager` เป็นตัวควบคุมว่า scene ไหนกำลังทำงานอยู่

### Scene ที่มีตอนนี้

- `StartMenuScene`
- `InstructionScene`
- `CharacterSelectScene`
- `LevelSelectScene`
- `LevelScene`

### ประโยชน์

- flow เกมชัดเจนขึ้น
- เปลี่ยนหน้าจอได้ง่าย
- ลดปัญหา import วนกัน
- เพิ่ม scene ใหม่ เช่น Pause หรือ Game Over ได้ง่าย

### ตัวอย่างแนวคิด

```text
StateManager
└── current_scene
    ├── handle_events()
    ├── update()
    └── draw()
```

เมื่อผู้เล่นกดปุ่ม `Play Game` scene จะเปลี่ยนจาก `StartMenuScene` ไปเป็น `CharacterSelectScene`

## 2. Template Method Pattern

### ใช้ที่ไหน

- `src/scenes/level_scene.py`
- `src/scenes/base_scene.py`

### แนวคิด

ด่านแต่ละด่านมีขั้นตอนคล้ายกัน คือรับ event, update, ตรวจเงื่อนไข, แล้ว draw ภาพ ดังนั้น `LevelScene` จึงทำหน้าที่เป็น template กลางของด่าน

### ลำดับการทำงานของด่าน

```text
load level data
create objects
handle events
update players and objects
check hazard
check door
render level
```

### ประโยชน์

- ไม่ต้องเขียน game loop ใหม่ทุกด่าน
- เพิ่มด่านใหม่ด้วยการเพิ่มข้อมูลด่านได้ง่าย
- logic กลางของด่านอยู่ที่เดียว

## 3. Factory Pattern

### ใช้ที่ไหน

- `src/systems/level_factory.py`
- `src/data/level_data.py`

### แนวคิด

ข้อมูลด่านอยู่ใน `level_data.py` ส่วนการสร้าง object จริงอยู่ใน `LevelFactory` ทำให้ `LevelScene` ไม่ต้องรู้รายละเอียดว่าต้องสร้าง `Player`, `Key`, `Door`, `Platform` อย่างไร

### Object ที่ Factory สร้าง

- `Player`
- `Key`
- `Door`
- `Platform`
- `Elevator`
- `ElevatorButton`

### ประโยชน์

- ลดการสร้าง object ซ้ำในหลายไฟล์
- แยกข้อมูลด่านออกจาก logic การสร้าง object
- ทำให้เพิ่มด่านใหม่ง่ายขึ้น

## 4. Asset Loader Shared Service

### ใช้ที่ไหน

- `src/core/asset_loader.py`
- `src/core/app.py`

### แนวคิด

ทุก scene และ system ใช้ `AssetLoader` ตัวเดียวจาก `GameApp` เพื่อโหลดรูปภาพและ cache ไว้ เมื่อมีการเรียก path เดิมซ้ำ โปรแกรมไม่ต้องโหลดรูปใหม่ทุกครั้ง

### ประโยชน์

- ลดการโหลดรูปซ้ำ
- รวม path loading logic ไว้ที่เดียว
- รองรับการ scale image ตอนโหลด
- ช่วยให้เปลี่ยนโครง asset ในอนาคตง่ายขึ้น

## ความสัมพันธ์ของ Pattern

```text
GameApp
└── StateManager
    └── Scene ปัจจุบัน
        ├── StartMenuScene
        ├── CharacterSelectScene
        ├── LevelSelectScene
        └── LevelScene
            └── LevelFactory
                └── Entities
```

`GameApp` เป็นตัวเริ่มระบบทั้งหมด `StateManager` เลือก scene ที่ทำงานอยู่ `LevelScene` เป็น template สำหรับด่าน และ `LevelFactory` สร้าง object จากข้อมูลด่าน

## แนวทางเพิ่มด่านใหม่ด้วยโครงนี้

1. เพิ่มข้อมูลด่านใหม่ใน `src/data/level_data.py`
2. ใส่ path asset และตำแหน่ง object ให้ครบ
3. เชื่อมปุ่มเลือกด่านใน `LevelSelectScene`
4. ใช้ `LevelScene(app, NEW_LEVEL_DATA)` เพื่อเปิดด่าน

ถ้าด่านใหม่มี mechanic พิเศษมาก ๆ เช่น spring, coin หรือ timer อาจสร้าง subclass ของ `LevelScene` เพิ่ม หรือเพิ่ม system ใหม่แยกใน `src/systems/`

## งานต่อยอดของ Design Pattern

- เพิ่ม `GameOverScene` เพื่อแยก logic แพ้ออกจาก `LevelScene`
- เพิ่ม `PauseScene`
- แยก collision บางส่วนไปเป็น `CollisionSystem`
- เพิ่ม `LevelRepository` หรือ `LevelLoader` ถ้าข้อมูลด่านย้ายไปเป็น JSON ในอนาคต
