# Material Design — วิวัฒนาการ 10 ปี

> **อ่านไฟล์นี้เมื่อ:** ต้องการเข้าใจ Context ของ Material Design System, เลือกว่าจะใช้ M1/M2/M3/M3E ระดับไหน, หรือสร้าง System Thinking บน Material Design

---

### 🏛️ 4 ยุคของ Material Design

**Material 1 (2014) — "Stake in the Ground"**

- Google ประกาศว่า "เราใส่ใจ UI และ UX"
- เปรียบ UI เหมือน **กระดาษและหมึก** — มี Surface, Shadow, Depth
- เริ่มโดย Matías Duarte (VP of Design)
- มีประมาณ 20 Component แต่ Implement ใน Code ได้แค่ 1-2 ตัว
- Core Metaphor: "Material is the metaphor"

**Material 2 (~2018) — "Going Deeper"**

- พัฒนาระบบให้ครอบคลุมมากขึ้น
- เพิ่ม Component สำหรับ Enterprise, Desktop, Consumer Apps
- อัปเดต Motion Guidelines ใหม่
- เริ่มมีการพูดถึง Design Tokens

**Material 3 (M3) — "Personalization at Scale"**

- **Dynamic Color System** — เปลี่ยนสีตาม Wallpaper ผู้ใช้ (Android 12+)
- Typography Updates ที่ Expressive ขึ้น
- Compose Integration ที่แข็งแกร่ง (Jetpack Compose)
- Token-based Design System
- ขยาย Component Library ครอบคลุมขึ้น

**Material 3 Expressive (2025) — "Emotion-Driven UX"**

- การอัปเดตที่ใหญ่ที่สุด ผ่านการวิจัยมากที่สุด (46 studies, 18,000+ คน)
- เพิ่ม Vibrant Colors, Intuitive Motion, Adaptive Components
- **35 Shapes ใหม่** พร้อม Shape Morph Motion
- Motion Physics System ขับเคลื่อนด้วย Tokens
- เปิดตัวพร้อม Android 16 และ Wear OS 6

---

### 🧱 หลักการ 3 ข้อหัวใจของ Material (ตลอดทุกยุค)

**1. Material is the Metaphor**

- UI มีน้ำหนัก ความลึก และแสงเหมือนวัตถุจริง
- Cards ทำงานเหมือนกระดาษ — ซ้อน, แยก, ปรากฏ
- Shadow = ระยะห่างจาก Surface ที่ต่างกัน

**2. Bold, Graphic, Intentional**

- ใช้สีตัดกันอย่างจงใจ — ไม่ใช่แค่ "ปลอดภัย"
- Typography ขนาดใหญ่ เป็นส่วนหนึ่งของ Design ไม่ใช่แค่ Placeholder
- Edge-to-edge imagery: ภาพขยายเต็ม Surface

**3. Motion Provides Meaning**

- Animation ใช้เพื่อนำทาง ยืนยัน และให้ Feedback
- ไม่ใช้ Animation เพื่อ "ตกแต่ง"
- Motion คือ "ชั้นสี่มิติ" ของ Design System

---

### 📐 Adaptive Design: Responsive Grid

|Breakpoint|Columns|Gutter|
|---|---|---|
|Compact (< 600dp)|4|16dp|
|Medium (600–904dp)|8|24dp|
|Expanded (905–1239dp)|12|24dp|
|Large (1240–1439dp)|12|24dp|
|Extra-large (≥ 1440dp)|12|24dp|

---

### 👥 เสียงจากผู้สร้าง Material

> **Matías Duarte:** "ข้อจำกัดเดียวของ Design คือจินตนาการ… และอายุแบตเตอรี่"

> **Christian Robertson (UX Lead, Material):** "M1 เป็นการวาง Stake ในดิน — Google ใส่ใจ UI/UX ไม่ใช่แค่ทฤษฎี แต่เป็น Tactical, Actionable Design Thinking"

> **Rich Fulcher:** "Material ยังคงเป็น Source of Truth ที่ Google แม้ว่าจะต้องปรับ Adapt ตามความต้องการของแต่ละ Product"

---

### 🔗 แหล่งข้อมูล Material Design ที่ใช้บ่อย

|Resource|URL|
|---|---|
|Material Design 3 Docs|m3.material.io|
|Material Figma Kit|Figma Community (M3 Design Kit)|
|Material Web Components|material-web.dev|
|Material Design Blog|material.io/blog|