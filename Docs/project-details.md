# รายละเอียดโปรเจกต์ Poonny Moony

## ภาพรวมโปรเจกต์

Poonny Moony เป็นเกม 2D cooperative platformer ที่พัฒนาด้วย Python และ Pygame ผู้เล่น 2 คนควบคุมตัวละครบนเครื่องเดียวกันเพื่อช่วยกันผ่านด่าน เก็บกุญแจ หลบพื้นที่อันตราย และเข้าสู่ประตูเพื่อไปด่านถัดไป

หลังการปรับโครงสร้าง โปรเจกต์ถูกจัดให้อยู่ในรูปแบบ OOP มากขึ้น โดยแยกส่วน core, scene, entity, system และ data ออกจากกัน ทำให้โค้ดอ่านง่ายขึ้น ลดการเขียนซ้ำ และต่อยอดด่านใหม่ได้ง่ายกว่าเดิม

## แนวคิดของเกม

แนวคิดหลักคือการร่วมมือกันระหว่างตัวละครสองตัว ผู้เล่นต้องเดิน กระโดด ใช้ platform ลิฟต์ และปุ่มกด เพื่อไปถึงกุญแจและประตู ในด่านที่มี hazard เช่น ลาวา ผู้เล่นต้องหลีกเลี่ยงพื้นที่อันตราย ไม่เช่นนั้นจะเกิด Game Over

เป้าหมายของผู้เล่นคือ:

- ควบคุมตัวละครทั้งสองให้ผ่านอุปสรรค
- เก็บกุญแจของด่าน
- พากุญแจไปยังประตู
- หลีกเลี่ยง hazard เช่น ลาวา
- ผ่านไปยังด่านถัดไป

## ประเภทเกม

เกมนี้จัดอยู่ในประเภท:

- 2D platformer
- Cooperative game
- Puzzle platformer
- Local two-player game

## เทคโนโลยีที่ใช้

- Python
- Pygame
- Git
- PNG/JPG assets

## โครงสร้างไฟล์ปัจจุบัน

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

## คำอธิบายส่วนหลัก

### `main.py`

เป็น entry point ของโปรแกรม ทำหน้าที่สร้าง `GameApp` และเริ่ม game loop

### `src/core/`

เก็บระบบแกนกลางของเกม เช่น application root, settings, asset loader และ state manager

### `src/scenes/`

เก็บหน้าจอหรือสถานะของเกม เช่น start menu, instruction, character select, level select และ level scene

### `src/entities/`

เก็บ object ในเกม เช่น player, key, door, platform, elevator และ elevator button

### `src/systems/`

เก็บระบบช่วยเหลือที่ไม่ใช่ entity โดยตรง เช่น factory สำหรับสร้าง object ในด่าน และ UI button

### `src/data/`

เก็บข้อมูลด่าน เช่น ตำแหน่งผู้เล่น กุญแจ ประตู platform hazard elevator และ asset path ของแต่ละด่าน

### `image/`

เก็บรูปภาพและ asset ทั้งหมดของเกม เช่น ตัวละคร พื้นหลัง เมนู ปุ่ม tileset กุญแจ ประตู และลาวา

### `Docs/`

เก็บเอกสารประกอบโปรเจกต์

## เครดิตรูปภาพและ Asset

จากชื่อไฟล์ในโปรเจกต์ พบว่ามี asset หลายชุดที่มาจาก CraftPix และไฟล์ภาพที่เก็บไว้ในโฟลเดอร์ `image`

ตัวอย่างไฟล์ asset ต้นฉบับ:

- `craftpix-net-396765-free-simple-platformer-game-kit-pixel-art (1).zip`
- `craftpix-161519-free-lava-fields-level-map-2d-backgrounds (1).zip`
- `craftpix-891123-free-golems-chibi-2d-game-sprites.zip`
- `craftpix-785611-free-dungeon-platformer-pixel-art-tileset.zip`
- `craftpix-net-846754-free-green-zone-tileset-pixel-art.zip`
- `craftpix-net-115897-free-exclusion-zone-tileset-pixel-art (1).zip`

ควรตรวจสอบ license ของ asset แต่ละชุดจากเว็บไซต์ต้นทางก่อนเผยแพร่หรือส่งงานจริง โดยเฉพาะถ้าจะใช้เกมในเชิงสาธารณะหรือเชิงพาณิชย์
