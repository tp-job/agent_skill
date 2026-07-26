---
name: google-design-system
description: >
  Apply Google Design principles across 16 domains: Material 3 Expressive, Motion Design, Google Sans Flex
  typography, AI/Gemini Visual Design, Global Accessibility, Design Sprints, UX Writing, Brand Building,
  Design Culture, and XR/AI Glasses (Glimmer). Use for ANY task involving Google design standards:
  designing/reviewing UI, choosing Material components, implementing animation, selecting typography,
  designing AI interfaces, running sprints, writing microcopy, or auditing accessibility.
  Trigger on: Material Design, M3 Expressive, Google design, expressive UI, motion design, Google Sans,
  variable font, design sprint, UX writing, AI interface, Gemini design, WCAG, touch target, RTL,
  design review, design system, Android UI, brand building, typography scale, accessible design, Glimmer.
license: MIT
metadata:
  author: nevinas06 (enhanced by Claude)
  version: "2.0.0"
  source: design.google (compiled June 2026)
---

# Google Design System Skill

ระบบอ้างอิงครบวงจรสำหรับการออกแบบตาม Google Design Philosophy ครอบคลุม 16 ด้าน ตั้งแต่ Material 3 Expressive, Motion, Typography, AI Visual Design, Accessibility, Design Sprints จนถึง UX Writing และ Brand Building

มุมมองจาก Senior Leadership: **UI Design · UX Design · Product Design · UX Research · Design Systems**

---

## เมื่อไหรต้องใช้ Skill นี้

ใช้ทุกครั้งที่:
- ออกแบบหรือรีวิว UI/UX บน Android, Web, หรือ AI Products
- เลือก Material Component, Color, Shape, หรือ Motion
- ตรวจสอบ Accessibility หรือ Global Design
- เขียน UX Copy, Error Messages, หรือ Onboarding
- วางแผนหรือ Facilitate Design Sprint
- ออกแบบ AI Interface (Gemini-style, Assistant, Copilot)
- ออกแบบสำหรับ XR / AI Glasses
- สร้างหรืออัปเดต Design System

---

## Quick Reference (อ่านก่อนเสมอ)

### 10 หลักการ Google Design

| # | หลักการ | สาระสำคัญ |
|---|---|---|
| 1 | **User First** | Research ก่อน Design |
| 2 | **Research-Driven** | ทุก Decision มีข้อมูลรองรับ |
| 3 | **Expressive + Usable** | ความงามและการใช้งานไม่ขัดกัน |
| 4 | **Inclusive by Default** | Accessibility = Foundation ไม่ใช่ Add-on |
| 5 | **System Thinking** | Token → Component → Pattern → Product |
| 6 | **Motion with Purpose** | ทุก Animation มีความหมาย ไม่ใช่แค่ตกแต่ง |
| 7 | **Iterate Relentlessly** | ไม่มี Perfect มีแต่ Better |
| 8 | **Global by Design** | RTL, Multi-script, Low bandwidth ตั้งแต่ต้น |
| 9 | **Trust through Transparency** | ระบุ AI, Confidence Level, Error State |
| 10 | **Design for Feeling** | Product ต้อง "รู้สึกดี" ไม่ใช่แค่ใช้งานได้ |

### กฎ Accessibility 3 ข้อที่ต้องจำ
- Contrast ≥ **4.5:1** (body) / **3:1** (large text & UI)
- Touch Target ≥ **48×48 dp**
- ทุก Animation ต้องมี **`prefers-reduced-motion`** variant

### Motion Duration (Material)
- Micro: **100–200ms** | Standard: **200–300ms** | Emphasis: **400–500ms**
- ห้ามใช้ Linear Easing — ใช้ Physics-based (spring / emphasized curve) เสมอ

### Typography ขั้นต่ำ
- Body mobile: **16sp** | Body desktop: **14sp** | Line height: **1.4–1.6×**

---

## Domain Map — อ่านไฟล์อ้างอิงไหน?

ระบุ Domain ที่ตรงกับงานที่ทำ แล้วเปิดไฟล์ใน `references/` ที่ตรงกัน:

| Priority       | Domain                                              | ไฟล์อ้างอิง                                         | เปิดเมื่อ                                          |
| -------------- | --------------------------------------------------- | --------------------------------------------------- | -------------------------------------------------- |
| 🔴 Critical    | Material 3 Expressive                               | [material-3-expressive](references/material-3-expressive.md)                       | ออกแบบ UI Component, เลือก Color/Shape/Motion      |
| 🔴 Critical    | Global Accessibility                                | [global-accessibility](references/global-accessibility.md)                        | ตรวจสอบ Contrast, Touch Target, RTL, Screen Reader |
| 🟠 High        | Motion Design                                       | [motion-design](references/motion-design.md)                               | กำหนด Animation, Transition, Duration, Easing      |
| 🟠 High        | Typography — Google Sans Flex                       | [google-sans-flex](references/google-sans-flex.md)                 | เลือก Typeface, Type Scale, Variable Axes          |
| 🟠 High        | AI / Gemini Visual Design                           | [gemini-ai-visual-design](references/gemini-ai-visual-design.md)                     | ออกแบบ AI Interface, Loading States, Trust         |
| 🟡 Medium      | Transparent Screens / XR                            | [transparent-screens](references/transparent-screens.md)                      | AI Glasses, Android XR, Additive Display           |
| 🟡 Medium      | Design Sprints                                      | [design-sprints](references/design-sprints.md)                              | วางแผน/Facilitate 5-day Sprint                     |
| 🟡 Medium      | Material Design Evolution                           | [material-design](references/material-design.md)                   | เข้าใจ Context M1–M3E, Grid System                 |
| 🟢 Support     | UX Writing, Design Review, Brand, AI Terms, Culture | [design-culture](references/design-culture.md) | เขียน Copy, ทำ Review, สร้าง Brand                 |
| 🔵 Overview    | 10 หลักการ + URL Resources                          | [google-design-10](references/google-design-10.md)               | ภาพรวม + แหล่งข้อมูล Official                      |
| 📄 Full Source | เอกสารต้นฉบับเต็ม                                   | [google-design](references/google-design.md)                             | ค้นหาข้อมูลรายละเอียดเพิ่มเติม                     |
| 📄 Concept     | สรุปแนวคิดย่อ                                       | [google-concept](references/google-concept.md)                                 | ภาพรวมเร็ว 5 นาที                                  |

---

## วิธีใช้ Skill นี้ (Step-by-Step)

1. **รับ Task** → ระบุว่า Task นี้อยู่ใน Domain ไหน (ดู Domain Map)
2. **เปิดไฟล์อ้างอิง** ที่ตรงกับ Domain นั้น (อาจมีมากกว่า 1 ไฟล์)
3. **ใช้หลักการ + Checklist** ใน Reference File ประกอบการตอบหรือรีวิว
4. **ถ้าไม่แน่ใจ** → เปิด [google-design](references/google-design.md) ค้นหาข้อมูลเพิ่มเติม
5. **ทุก Output** ต้องผ่าน Accessibility Checklist ([global-accessibility](references/global-accessibility.md)) เสมอ ไม่ว่า Domain จะเป็นอะไร

---

## Output Format แนะนำ

เมื่อทำการรีวิวหรือให้คำแนะนำ ใช้โครงสร้างนี้:

```
## Senior Design Leadership Review

### 🎯 Context & Goal
[สรุปว่ากำลังออกแบบอะไร สำหรับใคร]

### ✅ จุดแข็ง (ตาม Google Design Principles)
- ...

### ⚠️ จุดที่ต้องปรับปรุง
- [ปัญหา]: [อ้างอิงหลักการ / ตัวเลขมาตรฐาน] → [แนวทางแก้ไข]

### 🔧 คำแนะนำเชิงปฏิบัติ
1. ...

### 📋 Accessibility Checklist
- [ ] Contrast ≥ 4.5:1
- [ ] Touch Target ≥ 48×48 dp
- [ ] Motion มี prefers-reduced-motion
- [ ] ...

### 🔗 แหล่งข้อมูลเพิ่มเติม
- [URL ที่เกี่ยวข้อง]
```

---

## แหล่งข้อมูล Official (URL พร้อมใช้)

| Resource                 | URL                                          | Refer                            |
| ------------------------ | --------------------------------------------- | --------------------------------- |
| Google Design            | design.google                                 | [google-design](references/google-design.md), [google-concept](references/google-concept.md) |
| Material Design 3        | m3.material.io                                | [material-3-expressive](references/material-3-expressive.md), [material-design](references/material-design.md) |
| Google Fonts             | fonts.google.com                              | [google-sans-flex](references/google-sans-flex.md)              |
| PAIR (Human-AI)          | pair.withgoogle.com                           | [gemini-ai-visual-design](references/gemini-ai-visual-design.md)       |
| Android XR Design        | developer.android.com/design/ui/ai-glasses    | [transparent-screens](references/transparent-screens.md)           |
| Material Web Components  | material-web.dev                              | [material-3-expressive](references/material-3-expressive.md)         |
