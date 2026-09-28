# Transparent Screens — AI Glasses & XR Design (Jetpack Compose Glimmer)

> **อ่านไฟล์นี้เมื่อ:** ออกแบบสำหรับ AI Glasses, Android XR, Spatial Computing, หรือ Interface บน Additive Display ที่ไม่มี Background สีขาวทึบ

---

### 🔭 หลักการใหม่: ออกแบบบนความเป็นจริง

การออกแบบด้วย **Jetpack Compose Glimmer** (Design System สำหรับ Android XR) ท้าทายหลักการออกแบบเดิมทั้งหมด เพราะ **ไม่มี Screen สี่เหลี่ยมขาวเป็น Canvas** แต่เป็น "โลกแห่งความเป็นจริง" ที่ผันผวนตลอดเวลา

> _"ออกแบบ Traditional เริ่มจาก Container — แต่ Glasses ไม่มี Container มีแต่โลกทั้งใบ"_

---

### 🔦 Physics ของจอโปร่งแสง

Display บน AI Glasses ทำงานด้วย **Additive Display Technology** ซึ่งหมายความว่า:

- จอเพิ่มแสงได้อย่างเดียว → **ไม่สามารถสร้างสีดำทึบได้**
- "สีดำ" = ความโปร่งแสง 100% (Transparent ไม่ใช่ Black)
- Material Design เดิม → ใช้พื้นผิวสว่างและ Shadow เบาๆ → **ไม่ได้ผล** บน Additive Display
- **ปัญหา Halation:** แสงสว่างจาก Surface "ซึมซาบ" เข้าไปในพื้นที่โปร่งแสงข้างเคียง ทำให้ข้อความอ่านไม่ออก

---

### 💡 หลักการ Glimmer (4 ข้อ)

**หลักการ 1: Redefine Black**

- สีดำ ไม่ใช่ "สี" — แต่เป็น **"Container"**
- ใช้ Surface สีเข้มเพื่อสร้างพื้นฐาน "Clean Plate" ที่ Content อ่านออก
- ✅ DO: Dark Surface + Bright Content
- ❌ DON'T: Light Surface + Dark Content (เกิด Halation)

**หลักการ 2: Typography ตามวิทยาศาสตร์**

- ระยะโฟกัสของ Interface อยู่ที่ ~1 เมตร (ระยะแขน) ไม่ใช่ในมือ
- วัดตัวอักษรด้วย **Visual Angle (Degrees)** ไม่ใช่ Pixels หรือ Points
- ขนาดต่ำสุดที่อ่านออก: **0.6 องศา**
- ใช้ **Google Sans Flex** พร้อม Optical Size Axis → เพิ่มช่องไฟตัวอักษร (Counter) ให้อ่านง่ายขึ้น
- ✅ DO: Bold, ตัวอักษรห่าง, Optical Sizing
- ❌ DON'T: ฟอนต์บางและเล็ก

**หลักการ 3: Color ที่มองเห็นได้ใน Real World**

- สีสดของมือถือ "หายไป" เมื่อมองผ่านท้องฟ้าสีฟ้า
- Glimmer ใช้ Palette เป็นกลางโดย Default → สอดคล้องกับสีโลกความเป็นจริง
- ใช้สีที่ **ใกล้ขาว** เพื่อรักษา Contrast

**หลักการ 4: Motion ที่นำทาง ไม่รบกวน**

- Notification ที่ปรากฏ 500ms → "กระพริบ" เร็วเกินไป ผู้ใช้ไม่รู้ว่ามีอะไรขึ้น
- Glimmer ใช้ Transition เกือบ **2 วินาที** สำหรับ Notification เข้า
- Motion ควร "เชิญ" ความสนใจ ไม่ "บังคับ" ความสนใจ
- แต่ Response ต่อ Input ของผู้ใช้ต้องรวดเร็วทันที (Focus Ring, Highlight)

---

### 🎯 ปรัชญา: Human Factors First

> _"Interface ที่ดีที่สุดบน AI Glasses คือ Interface ที่ปรากฏเมื่อคุณต้องการมัน และหายไปเมื่อคุณไม่ต้องการ"_

### ✅ Checklist สำหรับ XR Design Review

- [ ] ทดสอบกับ Background ที่หลากหลาย (ท้องฟ้า / ห้องมืด / พื้นที่สว่างจ้า)
- [ ] Typography ≥ 0.6 องศา Visual Angle ที่ระยะ 1 เมตร
- [ ] ใช้ Dark Surface เป็น Default ไม่ใช่ Light Surface
- [ ] Animation Transition ≥ 2 วินาทีสำหรับ Non-interactive Notifications
- [ ] Interactive Feedback เร็วทันที (< 100ms)