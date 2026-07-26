# Motion Design — การเคลื่อนไหวที่มีความหมาย

> **อ่านไฟล์นี้เมื่อ:** ออกแบบ Animation, Transition, Micro-interaction, หรือกำหนด Motion Token สำหรับ Design System ใดก็ตามที่ต้องการความสอดคล้องตาม Material Motion

---

### 🎬 หลักการ 4 ข้อของ Material Motion

|หลักการ|ความหมาย|
|---|---|
|**1. Responsive**|ตอบสนองต่อ Input ทันที เหมือนวัตถุในโลกจริงที่ "รู้สึก" แรงกด|
|**2. Natural**|ไม่หยุดหรือเริ่มกะทันหัน เคลื่อนที่ตาม Arc ได้แรงบันดาลใจจาก Gravity และ Friction|
|**3. Aware**|Animation รู้ว่า Element อื่นกำลังทำอะไร Shared Elements เคลื่อนที่ประสานกัน|
|**4. Intentional**|ทุก Motion มีความหมาย สื่อสาร Hierarchy หรือ Relationship ไม่ใช่ "การตกแต่ง"|

---

### ⏱️ Duration Guidelines

|ประเภท Motion|Duration|ใช้เมื่อ|
|---|---|---|
|**Micro**|100–200ms|Icon state change, FAB press, Ripple|
|**Standard**|200–300ms|Card expand, Dialog enter, Tab switch|
|**Emphasis**|400–500ms|Full-screen transition, Hero animation|
|**XR / Glasses**|~2,000ms|Notification enter บน Transparent Display|

---

### 📈 Easing Curves

|Curve|CSS / Token|ใช้เมื่อ|
|---|---|---|
|**Emphasized**|`cubic-bezier(0.2, 0, 0, 1)`|Element เข้าสู่ Screen (Fast start → Settle)|
|**Emphasized Decelerate**|`cubic-bezier(0.05, 0.7, 0.1, 1)`|Incoming elements|
|**Emphasized Accelerate**|`cubic-bezier(0.3, 0, 0.8, 0.15)`|Outgoing elements (เร็วขึ้นก่อนออก)|
|**Standard**|`cubic-bezier(0.2, 0, 0, 1)`|ใช้ทั่วไปใน Standard transitions|
|**Standard Decelerate**|`cubic-bezier(0, 0, 0, 1)`|เข้าจากขอบ Screen|
|**Standard Accelerate**|`cubic-bezier(0.3, 0, 1, 1)`|ออกจาก Screen|
|❌ **Linear**|`linear`|**ห้ามใช้** — ดูหุ่นยนต์|

---

### 🔄 วิวัฒนาการ Motion ที่ Google

- **2016** → Material Motion Guidelines ออกมาครั้งแรก มีนักออกแบบ Motion ไม่ถึง 100 คน
- **2018 (M2)** → อัปเดตหลักการ Motion มีตัวอย่างที่ Realistic มากขึ้น
- **M3** → เพิ่ม Motion Physics System ขับเคลื่อนด้วย Tokens → ทำ Custom Transition ง่ายขึ้น
- **M3 Expressive (2025)** → Shape Morph Motion: รูปทรง 35 แบบใหม่ที่ Animate เปลี่ยนรูปได้

---

### ♿ Accessibility: Reduced Motion (สำคัญมาก)

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

- **เสมอ** ต้องมี Reduced Motion Variant
- ผู้ใช้ที่เป็น Vestibular Disorder จะป่วยจาก Parallax / Scale Animations ขนาดใหญ่
- ลด Animation แต่ไม่ต้องลบทิ้งทั้งหมด — เปลี่ยนเป็น Opacity Fade แทน Scale/Translate ได้

---

### 💡 เคล็ดลับจาก Sharon Harris (Motion Lead → UX Manager, Google Maps)

> _"Motion เต็มไปด้วยความตื่นเต้น แต่ก็มีความสงสัยจาก Product และ Engineering เสมอ — คำถามคือ 'Motion มีคุณค่าอะไร?' Material ช่วยสร้างภาษากลางให้ตอบคำถามนั้นได้"_

---

### ✅ Checklist Motion Review

- [ ] ทุก Animation มีวัตถุประสงค์ชัดเจน (ไม่ใช่แค่สวย)
- [ ] Duration อยู่ใน Range ที่ถูกต้องตามประเภท
- [ ] ใช้ Physics-based Easing (ไม่ใช่ Linear)
- [ ] Shared Element Transitions สอดคล้องกันข้าม Screen
- [ ] มี `prefers-reduced-motion` implementation
- [ ] ทดสอบบน Low-end Device ว่า Animation ยังลื่นอยู่