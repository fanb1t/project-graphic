# อธิบายการทำงานของโค้ด

## ภาพรวมการทำงาน

โปรเจกต์นี้ใช้ Pygame ในการสร้างเกม 2 มิติ โครงสร้างปัจจุบันถูกจัดใหม่เป็น OOP โดยแยก application, scene, entity, system และข้อมูลด่านออกจากกัน

flow หลักของเกมคือ:

```text
main.py
-> GameApp
-> StateManager
-> StartMenuScene
-> CharacterSelectScene
-> LevelSelectScene
-> LevelScene
```

## `main.py`

เป็นจุดเริ่มต้นของโปรแกรม มีหน้าที่สร้าง `GameApp` และเรียก `app.run()` เท่านั้น ทำให้ entry point เรียบง่ายและไม่ผูกกับ logic ของแต่ละหน้าจอโดยตรง

## `src/core/app.py`

ไฟล์นี้มี class `GameApp` ซึ่งเป็น application root ของเกม

หน้าที่หลัก:

- initialize Pygame
- สร้าง window
- สร้าง clock
- สร้าง `AssetLoader`
- สร้าง `StateManager`
- ตั้ง scene เริ่มต้นเป็น `StartMenuScene`
- รัน game loop หลัก

## `src/core/state_manager.py`

ไฟล์นี้มี class `StateManager` ใช้จัดการ scene ปัจจุบันของเกม

หน้าที่หลัก:

- เก็บ scene ที่กำลังทำงานอยู่
- เปลี่ยน scene เมื่อผู้เล่นกดปุ่มหรือผ่านด่าน
- ส่ง event, update และ draw ไปยัง scene ปัจจุบัน
- สั่งหยุดเกมเมื่อผู้เล่นปิดหน้าต่าง

## `src/core/asset_loader.py`

ไฟล์นี้มี class `AssetLoader` ใช้โหลดรูปภาพจาก path และ cache ภาพที่โหลดแล้ว

ข้อดี:

- ลดการ `pygame.image.load()` ซ้ำ
- รวม logic การโหลดรูปไว้ที่เดียว
- รองรับการ scale รูปตอนโหลด

## `src/core/settings.py`

เก็บค่าคงที่ของเกม เช่น:

- `WIDTH`
- `HEIGHT`
- `FPS`
- `TITLE`
- สีของปุ่มและข้อความ

## `src/scenes/`

โฟลเดอร์นี้เก็บ scene หรือหน้าจอของเกม

### `base_scene.py`

มี class `BaseScene` เป็น interface กลางของทุก scene โดยกำหนดเมธอดพื้นฐาน:

- `handle_events()`
- `update()`
- `draw()`

### `start_menu.py`

มี class `StartMenuScene` สำหรับหน้าเมนูเริ่มเกม มีปุ่ม `Play Game` และ `Instruction`

### `instruction.py`

มี class `InstructionScene` สำหรับแสดงคำแนะนำการเล่น

### `character_select.py`

มี class `CharacterSelectScene` สำหรับเลือกตัวละครของผู้เล่น 1 และผู้เล่น 2 แสดงปุ่มควบคุม และไปหน้าเลือกด่านหลังผู้เล่นกด `Confirm`

### `level_select.py`

มี class `LevelSelectScene` สำหรับเลือกด่าน ปัจจุบันเชื่อมด่าน 1 และด่าน 2 แล้ว ส่วนด่าน 3 ยังเป็นงานต่อยอด

### `level_scene.py`

มี class `LevelScene` สำหรับเล่นด่าน ใช้ข้อมูลจาก `level_data.py` และสร้าง object ผ่าน `LevelFactory`

ลำดับการทำงานของ `LevelScene`:

1. โหลดข้อมูลด่าน
2. สร้าง object ในด่าน
3. รับ event
4. update ผู้เล่น กุญแจ ปุ่ม และลิฟต์
5. ตรวจชน hazard
6. ตรวจเข้าประตู
7. draw object ทั้งหมด

## `src/entities/`

โฟลเดอร์นี้เก็บ object ที่อยู่ในเกม

### `Player`

ดูแลการเดิน กระโดด gravity collision และการเก็บกุญแจ

### `Key`

เป็นกุญแจของด่าน เมื่อผู้เล่นเก็บแล้วกุญแจจะตามผู้เล่นคนนั้น

### `Door`

ตรวจว่าผู้เล่นที่ถือกุญแจชนประตูหรือไม่

### `Platform`

ใช้แทนพื้น กล่อง หรือ hazard ที่เป็น sprite สี่เหลี่ยม

### `Elevator`

เป็น platform ที่เคลื่อนที่ขึ้นลงตามสถานะของปุ่ม

### `ElevatorButton`

ตรวจว่าผู้เล่นคนใดยืนทับปุ่มอยู่หรือไม่

## `src/systems/`

### `level_factory.py`

มี class `LevelFactory` ใช้สร้าง object ของด่านจากข้อมูลใน `level_data.py`

หน้าที่หลัก:

- สร้าง player 1 และ player 2
- สร้าง key และ door
- สร้าง platform และ hazard
- สร้าง elevator และ elevator button

### `ui.py`

มี class `TextButton` ใช้สร้างปุ่มข้อความใน menu scene

## `src/data/level_data.py`

เก็บข้อมูลด่านในรูปแบบ dictionary เช่น:

- ชื่อด่าน
- background image
- ตำแหน่งผู้เล่น
- ตำแหน่งกุญแจ
- ตำแหน่งประตู
- platform
- hazard
- elevator
- button

ถ้าจะเพิ่มด่านใหม่ ควรเพิ่มข้อมูลด่านในไฟล์นี้ก่อน แล้วให้ `LevelScene` และ `LevelFactory` ใช้ข้อมูลนั้นสร้าง object

## Game Loop

Game loop หลักอยู่ใน `GameApp.run()` โดยทำงานซ้ำตามลำดับนี้:

1. อ่าน event จาก Pygame
2. ส่ง event ให้ scene ปัจจุบัน
3. update scene ปัจจุบัน
4. draw scene ปัจจุบัน
5. flip หน้าจอ
6. จำกัด FPS

## Collision

ระบบ collision หลักอยู่ใน `Player` และ `LevelScene`

ตัวอย่าง collision:

- ผู้เล่นชน platform
- ผู้เล่นชน elevator
- ผู้เล่นชน key
- ผู้เล่นชน hazard
- ผู้เล่นชน door
- ผู้เล่นชน elevator button

## สิ่งที่ควรพัฒนาต่อ

- เชื่อมด่าน 3 เข้ากับระบบ scene ใหม่
- แยก Game Over เป็น scene เฉพาะ
- เพิ่ม Pause Scene
- เพิ่มเสียงและเอฟเฟกต์
- ย้าย `image/` เป็น `assets/` เมื่อพร้อมแก้ path ทั้งหมด
