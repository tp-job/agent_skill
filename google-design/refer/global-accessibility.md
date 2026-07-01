# Global Accessibility — การออกแบบที่ครอบคลุมโลก

> **อ่านไฟล์นี้เมื่อ:** ตรวจสอบ Accessibility, ออกแบบสำหรับ Global Users หรือ Next Billion Users, กำหนด Touch Target, Contrast, หรือสนับสนุน RTL / Low Bandwidth Environments

---

### 🌍 3 มิติ: ตรวจสอบสมมติฐาน, โครงสร้างพื้นฐาน, การตัดสินใจ UX

#### Part 1 — Check Your Assumptions

นักวิจัย Nithya Sambasivan และ Astrid Weber พบว่า **ผู้ออกแบบมักมีสมมติฐานผิด** เกี่ยวกับผู้ใช้จริง

ปัจจัยที่มักถูกมองข้าม:

- แสงแดดจ้า → อ่านหน้าจอไม่ออก
- มือเปียก / ถุงมือ → แตะหน้าจอไม่ได้
- ความบกพร่องทางสายตา / มือ / การได้ยิน
- บริบทแวดล้อม: เดินไปด้วย, อยู่บนรถ, เสียงดัง

**หลักการ Curb Cut Effect:**

> _"Dropped Curb บนทางเท้า ช่วยคนนั่งวีลแชร์ แต่ยังช่วยคนเข็นรถเข็นเด็กและลากกระเป๋าด้วย — Accessibility ช่วยทุกคน"_

#### Part 2 — Infrastructure & Devices

**ความท้าทายด้านเครือข่าย:**

- ค่าใช้จ่าย Data ในประเทศกำลังพัฒนาสูงกว่าเทียบกับรายได้มาก
- ออกแบบให้ทำงานได้บน **Low Bandwidth** หรือ Offline

**ความหลากหลายของ Device:**

- สมาร์ทโฟนราคาถูก: Screen Resolution ต่ำ, RAM น้อย
- Touchscreen คุณภาพต่ำ → Touch Target เล็กเกินไป = ใช้งานไม่ได้
- ออกแบบสำหรับ Screen **4" ถึง 7"+**
- ทดสอบบน Low-end Device จริง ไม่ใช่แค่ Emulator

#### Part 3 — Tactical UX Decisions

**Touch Target:**

- ขนาดต่ำสุดที่แนะนำ: **48×48 dp** (Android) / **44×44 pt** (iOS)
- ช่วยผู้ใช้ที่มืออ่อนแรง, Tremor, สายตาไม่ดี
- M3 Expressive แนะนำให้ **เกินมาตรฐาน** เพื่อ Usability ที่ดีกว่า

---

### 🎨 Contrast Standards (WCAG 2.1)

|ประเภท|Contrast Ratio ขั้นต่ำ|
|---|---|
|Body Text (< 18pt)|**4.5:1**|
|Large Text (≥ 18pt หรือ 14pt Bold)|**3:1**|
|UI Components & Graphics|**3:1**|
|Decorative / Disabled elements|ไม่มีข้อกำหนด|

**กฎสำคัญ:**

- ห้ามใช้สีเพียงอย่างเดียวเป็นสื่อข้อมูล (Color-blind Users)
- เสมอมี Text Label คู่กับ Icon (อย่างน้อย tooltip)

---

### 🔤 Typography Accessibility

- ทำข้อความและ Typography ให้ใหญ่โดย Default
- ต้อง Scale ได้เมื่อ System Font Size เปลี่ยน
- ห้าม Lock Font Size ด้วย `px` บน Web → ใช้ `rem` แทน
- Line Height Body: 1.5× ขึ้นไป

---

### 🌐 RTL Support

- Support Right-to-Left (Arabic, Hebrew) layout ตั้งแต่เริ่มต้น ไม่ใช่ Retrofit
- Icons ที่มีทิศทาง (เช่น Back Arrow, Play) ต้อง Mirror ใน RTL
- Padding/Margin: ใช้ `start/end` ไม่ใช่ `left/right`

---

### 🔊 Screen Reader & Keyboard

- ทดสอบด้วย TalkBack (Android) และ VoiceOver (iOS/macOS)
- ทุก Non-text Content ต้องมี Alt Text หรือ `contentDescription`
- Navigation Flow ด้วย Keyboard ต้องสมเหตุสมผล
- Focus Indicator ต้องมองเห็นได้ชัด (ไม่ใช่แค่ Browser Default)

---

### ✅ Accessibility Checklist (ใช้ทุก Design Review)

- [ ] Color Contrast ผ่านมาตรฐาน WCAG 2.1 AA
- [ ] ไม่ใช้สีเพียงอย่างเดียวสื่อข้อมูล
- [ ] Touch Target ≥ 48×48 dp
- [ ] Font Scale ได้เมื่อ System Size เปลี่ยน
- [ ] มี Alt Text / contentDescription ทุก Image & Icon
- [ ] ทดสอบ TalkBack / VoiceOver Navigation Order
- [ ] Support RTL Layout (ถ้า Product ไป Global)
- [ ] ทดสอบบน Low-end Device จริง
- [ ] มี `prefers-reduced-motion` สำหรับ Animation