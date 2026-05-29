# เอกสารโปรเจกต์ Poonny Moony

โฟลเดอร์นี้ใช้เก็บเอกสารประกอบโปรเจกต์เกม Poonny Moony เพื่อให้เข้าใจแนวคิดของเกม วิธีรันโปรแกรม โครงสร้างโค้ด และแนวทางพัฒนาต่อ

## ไฟล์เอกสารหลัก

- [รายละเอียดโปรเจกต์](project-details.md) แนวคิด ประเภทเกม โครงสร้างไฟล์ปัจจุบัน และเครดิตรูปภาพ
- [วิธีการเล่น](gameplay.md) ปุ่มควบคุม เป้าหมาย และเงื่อนไขผ่านด่าน

## เอกสารด้านการพัฒนา

- [สารบัญการพัฒนา](Development/README.md)
- [อธิบายการทำงานของโค้ด](Development/code-explanation.md)
- [โครงสร้างหลัง refactor](Development/refactor-structure.md)
- [Design Pattern ที่ใช้ในโปรเจกต์](Development/design-patterns.md)
- [ภาพรวมระบบและ Use Cases](Development/system-overview-use-cases.md)

## โครงสร้างโค้ดที่เอกสารอ้างอิง

```text
project-graphic/
├── main.py
├── src/
│   ├── core/
│   ├── data/
│   ├── entities/
│   ├── scenes/
│   └── systems/
├── image/
└── Docs/
```

## เอกสารที่ควรเพิ่มในอนาคต

- `level-design.md` รายละเอียดการออกแบบด่านแต่ละด่าน
- `known-issues.md` ปัญหาที่พบและสิ่งที่ต้องแก้
- `roadmap.md` แผนพัฒนาต่อ
- `assets-credit.md` รายละเอียด license และที่มาของ asset แบบเต็ม
