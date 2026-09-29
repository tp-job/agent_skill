# Google Sans Flex — วิวัฒนาการของ Typeface

> **อ่านไฟล์นี้เมื่อ:** เลือก Typeface, ตั้งค่า Variable Font Axes, ออกแบบ Type Scale สำหรับ Android/Web/AI Products หรือออกแบบ Multi-script / Global UI

---

### 📖 7 ปัญหา → 7 วิวัฒนาการ

Google Sans ไม่ได้เกิดจาก "แรงบันดาลใจ" แต่เกิดจากการแก้ปัญหาต่อเนื่อง:

|ปัญหา|วิธีแก้|ปี|
|---|---|---|
|Logo Redesign 2015 → Product Lockup นับร้อยต้องอัปเดต|**Product Sans** — Geometric, ตัวอักษรชิด เหมาะ Product Name ขนาดใหญ่|2015|
|Product Sans ทำงานไม่ดีใน Ad/UI|**Google Sans** — ออปติไมซ์ Counter, X-height, Stroke Contrast|2018|
|Google Sans อ่านยากที่ขนาดเล็ก|**Google Sans Text** — สูงกว่า, แคบกว่า, Tracking มากกว่า (เปิดตัวบน Pixel 3)|2020|
|รองรับแค่ Latin|**Google Sans International** — ขยายสู่ 20+ Writing Systems (Arabic, Chinese, Thai, Japanese, Korean, Hebrew ฯลฯ)|~2021|
|Google Sans Mono แยกแยะตัวอักษรไม่ออกใน Code|**Google Sans Code** — เฉพาะ 20 ภาษา Programming (Q มีหาง, a/g traditional, curly brackets) เป็น Open-Source ใน Gemini|2025|
|Dynamic/Expressive UI ต้องการ Typography ปรับได้|**Google Sans Flex** — 6 Variable Axes ได้รับ Red Dot Winner 2024|2024|
|Google Sans ใช้ได้เฉพาะใน Google Products|**Open-Source** — Google Sans + Flex เปิดที่ Google Fonts|2025|

---

### 🎚️ Google Sans Flex — 6 Variable Axes

|Axis|บทบาท|ตัวอย่าง|
|---|---|---|
|**Weight**|น้ำหนักตัวอักษร|Thin → Black|
|**Width**|ความกว้างตัวอักษร|Condensed → Extended|
|**Optical Size**|ปรับสำหรับขนาดที่ใช้จริง|Caption ↔ Display|
|**Slant**|เอียงแบบ Variable Italic|0° → −10°|
|**Grade**|เพิ่ม/ลด น้ำหนักโดยไม่เปลี่ยน Spacing|ตอบสนองต่อ Dark Mode|
|**Roundedness**|ความโค้งมนที่ปลายตัวอักษร|Geometric → Friendly|

**ตัวอย่างการใช้งาน:**

- ปรับ `Roundedness` สูงขึ้น → ดูเป็นมิตร เหมาะ Consumer App
- ปรับ `Weight` สูง + `Width` แคบ → ดูมั่นคง เหมาะ Enterprise
- ปรับ `Grade` ลดลงบน Dark Mode → ลด Blooming ของตัวอักษรสีขาวบนพื้นมืด

---

### 📐 Type Scale (Material 3)

|Role|ขนาดแนะนำ|ใช้เมื่อ|
|---|---|---|
|Display Large|57sp|Hero Heading, First Screen|
|Display Medium|45sp|Section Hero|
|Display Small|36sp|Sub-hero|
|Headline Large|32sp|Screen Title|
|Headline Medium|28sp|Card Title|
|Headline Small|24sp|Section Header|
|Title Large|22sp|List Header|
|Title Medium|16sp / Medium weight|Emphasized Body|
|Title Small|14sp / Medium weight|Component Label|
|Body Large|16sp|Primary Reading Content|
|Body Medium|14sp|Secondary Content|
|Body Small|12sp|Caption|
|Label Large|14sp|Button, Tab|
|Label Medium|12sp|Badge, Chip|
|Label Small|11sp|Overline|

**กฎสำคัญ:**

- Body text ขั้นต่ำ: **16sp บนมือถือ / 14sp บน Desktop**
- Line height: **1.4–1.6× font-size** สำหรับ Body
- ให้ Text Scale ได้เมื่อ System Font Size เปลี่ยน (Accessibility)

---

### 🌍 Multi-Script Considerations

- Google Sans International ครอบคลุม **Arabic, Chinese (Simplified/Traditional), Thai, Japanese, Korean, Hebrew, Devanagari** และอีกมาก
- เมื่อออกแบบ Global UI: ทดสอบ Layout กับ RTL (Arabic, Hebrew) และ Tall Scripts (Thai, Devanagari)
- Thai: ตัวอักษรไทยมีวรรณยุกต์บน/ล่าง ต้องการ Line Height สูงกว่า Latin (~1.7–2.0×)

---

### 🎓 บทเรียนสำคัญ

> _"Google Sans คือตำราแห่ง Need-Based Design — ไม่ใช่ Flash of Inspiration แต่เป็นวิวัฒนาการที่ขับเคลื่อนด้วยมนุษย์"_

### ✅ Checklist Typography Review

- [ ] ใช้ Google Sans Flex หรือ Typeface ที่เลือกบน Google Fonts
- [ ] Type Scale ตรงกับ Material 3 Role ที่กำหนด
- [ ] Body text ≥ 16sp (mobile) / 14sp (desktop)
- [ ] Line height อยู่ในช่วง 1.4–1.6× สำหรับ Body
- [ ] ทดสอบ Scale Up ด้วย System Large Font Size
- [ ] ถ้ามี Multi-script: ทดสอบ RTL + Tall Script layouts