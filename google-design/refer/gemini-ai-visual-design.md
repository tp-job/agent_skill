# Gemini AI Visual Design — ภาษาภาพสำหรับ AI

> **อ่านไฟล์นี้เมื่อ:** ออกแบบ Interface สำหรับ AI Products (Gemini, Assistant, Copilot-style), ออกแบบ Loading/Thinking States, Illustration สำหรับ AI, หรือสร้าง Trust ในระบบที่ "ยังไม่นิ่ง"

---

### 🌊 ความท้าทาย: ออกแบบสิ่งที่ไม่เคยมีมาก่อน

Gemini เป็น AI ที่ **"เปลี่ยนแปลงอยู่เสมอ"** ซึ่งหมายความว่า:

- ไม่สามารถใช้วิธีออกแบบแบบ Linear หรือ Predictable ได้
- ต้องสร้างภาษาภาพที่ทำให้ผู้ใช้ **ไว้วางใจ** สิ่งที่ยังไม่นิ่ง

> _เปรียบเหมือน Susan Kare ผู้บุกเบิก Macintosh Interface ที่ใช้ถังขยะ, แปรงพู่กัน, และหน้าคอมยิ้ม เพื่อทำให้โลก Digital Abstract กลายเป็นสิ่งที่จับต้องได้_

---

### 🎨 องค์ประกอบภาพหลัก 4 ส่วน

**1. Gradients — ภาษาหลักของ Gemini**

- Gradient คือ "Vibe" ไม่ใช่ Object (ต่างจาก Icon ที่เป็น "Thing")
- ออกแบบให้ **ขอบด้านหน้าเข้มเกือบทึบ** และ **ค่อยๆ จางออก** → สื่อถึง "ทิศทาง" และ "พลังงาน"

|ชนิด Gradient|ใช้ตอนไหน|
|---|---|
|**Concentrated Gradient**|ขณะ Transcribing Voice|
|**Diffused Gradient**|ขณะ Listening|
|**Directional Gradient**|นำสายตาไปที่ Feature Icons|

**2. Foundational Shapes — รากฐานจาก Google DNA**

- เลือก **วงกลม** เป็นรูปทรงหลัก → สื่อถึง Simplicity, Harmony, Comfort
- Logo Gemini สร้างจาก **Negative Space ของ 4 วงกลมที่มาชิดกัน**
- ปุ่มและ Container มีมุมโค้ง (Rounded Corners) → สร้าง Continuity กับ Google Apps อื่น

**3. Intentional Motion — เคลื่อนไหวอย่างมีเหตุผล**

- ทุก Animation มี Start และ End ที่ชัดเจน → ผู้ใช้รู้ว่าระบบ "กำลังทำอะไร"
- Inner Activity ใน Motion = Gemini "กำลังคิด, วิเคราะห์, รู้สึก" → ทำให้ AI Relatable

|Motion Type|ความหมาย|
|---|---|
|Curve Speed|สร้าง Anticipation แล้ว Release|
|Radial Gradient Ripple|แทน Voice Waves|
|Pulsing Icons|แนะนำ Feature ใหม่|

**4. Softness by Design**

- Illustration ต้องให้ความรู้สึก **"อบอุ่น, Spatial, โค้งมน"**
- คำที่ต้องรู้สึกได้: "Optimistic, Delightful, Playful yet Sophisticated"
- Ethereal Quality → สะท้อน "กระบวนการ Ideation ที่ไม่เป็นเส้นตรง" ของ AI

---

### 🗺️ นักออกแบบในฐานะนักทำแผนที่

> _"ออกแบบ Gemini เหมือนการวาดแผนที่บนพื้นที่ที่ยังคงเปลี่ยนแปลง — ผู้ใช้ไม่ต้องการระบบที่สมบูรณ์แบบ พวกเขาต้องการระบบที่ 'ไม่สมบูรณ์แบบอย่างรอบคอบ'"_

---

### 🤝 Trust & Transparency ใน AI UI

- แสดงให้ผู้ใช้รู้ว่ากำลังโต้ตอบกับ AI (ไม่ใช่มนุษย์)
- ระบุ Confidence Level ของ AI output อย่างชัดเจน
- ออกแบบ Error State เมื่อ Model ผิดพลาด → บอกผู้ใช้ว่า "ทำไม" และ "ทำอะไรต่อได้"
- ห้ามแสดง AI เป็น "ทุกรู้" → สร้าง False Confidence ใน User

---

### ✅ Checklist AI UI Design Review

- [ ] ผู้ใช้รู้ชัดว่ากำลังคุยกับ AI (ไม่ใช่มนุษย์)
- [ ] Thinking/Loading State สื่อสารว่า "ระบบยังทำงานอยู่" อย่างมีความหมาย
- [ ] มี Error State ที่ Actionable ("เกิดอะไรขึ้น + ทำอะไรต่อได้")
- [ ] Gradient/Motion เลือกชนิดให้ตรงกับ State ที่ถูกต้อง
- [ ] Illustration มีความรู้สึก Soft/Optimistic ไม่แข็งกระด้าง
- [ ] ไม่แสดงให้ AI ดู "ทุกรู้" หรือ "ไม่เคยผิดพลาด"