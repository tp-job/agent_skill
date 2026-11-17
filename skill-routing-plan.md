# แผน: จัดระเบียบ skill และให้เรียกใช้อัตโนมัติ

สถานะ: **ระยะ 0–1 กำลังทำ** (2026-11-16)

## ความคืบหน้า

| ระยะ | ทำแล้ว | ค้าง |
| --- | --- | --- |
| 0 | เพิ่ม eval จาก prompt จริง 27 ข้อใน `evals/trigger/real-*` และ `not-real-*` (tag `real`) | รัน baseline ไม่ได้: `claude` CLI ยังไม่ได้ login ต้องรัน `claude /login` ใน terminal ก่อน แล้วรัน `claude plugin eval . --tag real --runs 2 --ablation none --no-publish --model claude-sonnet-5-5 -j 4` |
| 1 | ตั้ง `skillListingBudgetFraction: 0.03` ใน `~/.claude/settings.json` ให้คำอธิบาย skill ทุกตัวอยู่ในงบ เก็บ plugin ทุกตัวไว้ตามที่คุณเลือก | คุณปิด plugin `agent-skill` ใน claude.ai (Customize → Plugins) เพื่อเหลือแค่ตัวที่ติดตั้งจาก GitHub |

### ผล baseline (2026-11-16, 27 ข้อ × 2 รอบ, ค่าใช้จ่าย $3.57)

| วัด | ผล |
| --- | --- |
| ผ่านทั้งข้อ | 10 / 27 (ข้อที่ห้ามเรียก skill ผิด 3 จาก 3 ผ่าน; ข้อที่ต้องเรียก skill ถูก 7 จาก 24) |
| คะแนนเฉลี่ย | 0.43 |
| ล้มเพราะ Claude ตอบเองโดยไม่เปิด skill เลย | ส่วนใหญ่ (`Skill called 0x`) |

ผ่าน: `supabase-*`, `drawio-diagrams`, `cs-course-designer`, แผน endpoint
ล้ม: bug/error (`debug-master`), ฐานข้อมูลช้า, SQL injection/auth (`owasp`), UI ขอบไม่ตรง (`ui-checker`), thesis/NFR, SRS/sprint, Flutter รัน/ทดสอบ, user flow/design system, ถามสถาปัตยกรรมแบบแบ่งชั้น (`knowledge-base`), สรุปโน้ต Obsidian

ข้อควรระวังในการอ่านผล: eval รันแบบ headless 4 turn มี plugin เดียว ไม่มี CLAUDE.md ของคุณ จึงแข็งกว่า session จริง และผลนี้เป็นค่าฐานก่อนระยะ 2–3 ไม่ใช่ผลของงบ 3% โดยตรง (งบนี้มีผลใน session ใหม่)

### ผลหลังเพิ่มคำ trigger ไทย (2026-11-16, ทั้งชุด 46 ข้อ × 2 รอบ, $7.79)

| ชุด | ก่อน | หลัง |
| --- | --- | --- |
| prompt จริง 27 ข้อ | ผ่าน 10, เฉลี่ย 0.43 | ผ่าน 17, เฉลี่ย 0.67 |
| ชุดเดิม 19 ข้อ | ไม่มีค่าฐาน | ผ่าน 14, เฉลี่ย 0.83 |

ยังไม่ผ่าน (prompt จริง): `google-button-error` (debug-master), `slow-insert-thai`, `sql-injection-thai` (owasp), `ui-border-thai` (ui-checker), `thesis-examiner` (NFR), `next-issue-plan`, `setup-react`, `skill-flowchart-pages`
ชุดเดิมที่ไม่เต็ม: `im-stuck` 0, `lessons-learned` 0, `one-slow-query` 0.5, `ci-trustworthy` 0.5 (ไม่มีค่าฐานก่อนแก้ จึงยังบอกไม่ได้ว่าถอยหลังหรือไม่)

### ผลหลังแก้ 8 เคสที่ไม่ผ่าน (2026-11-17, prompt จริงและเคสไม่ควรเรียก 27 ข้อ × 2 รอบ)

แก้ที่คำอธิบายของ `promethean-parthenon` (v3.11.0: เพิ่ม "ปุ่มไม่ทำงาน", "insert ช้า", "ขอบไม่ตรง", "thesis defence", "setup project", "เริ่มทำ issue ต่อ" และคำไทย "ช้ามาก") กับ `drawio-diagrams` (v1.4.1: "สร้าง page ใน drawio") ผ่าน 47 จาก 54 รอบ (ก่อนแก้ 17 จาก 27 ข้อ)

| ยังไม่ผ่านแน่นอน | เหตุผล |
| --- | --- |
| `sql-injection-thai` 0/2 | prompt ถามให้อธิบายตารางในโปรเจกต์ มีคำว่า sql injection แค่ท้ายประโยค โมเดลตอบเองโดยไม่เปิด skill |

ไม่เสถียร (ผ่าน 1 จาก 2): `design-system-html`, `layered-arch-thai`, `skill-flowchart-pages`, `srs-sprint`, `supabase-mcp` เคสไม่ควรเรียก skill (`not-real-*`) ผ่านครบ

ช่องว่างที่พบระหว่างทำ eval: ไม่มี skill ดูแล **Render deploy** (มีแต่ Vercel), **Excel/VBA** และ **การเขียน thesis/รายงาน** ทั้งที่เป็นงานที่ทำบ่อย ใช้เป็นข้อมูลของระยะ 2

## Contents

- สิ่งที่พบ
- เป้าหมาย
- แผนงาน 5 ระยะ
- เรื่องที่คุณต้องตัดสินใจ
- สิ่งที่แผนนี้ไม่ครอบคลุม

---

## สิ่งที่พบ

ข้อมูลจาก transcript ของ Claude Code ทุกโปรเจกต์ในเครื่อง (266 session, ประมาณ 2,800 prompt)

### 1. skill แทบไม่เคยถูกเรียกเอง

| วัด | จำนวน |
| --- | --- |
| prompt ที่คุณพิมพ์ | ~2,800 |
| ครั้งที่ Claude โหลด skill เอง (Skill tool) | 57 |
| ครั้งที่คุณพิมพ์ `/promethean-parthenon` เอง | 138 |
| ครั้งที่คุณพิมพ์ `/senior-leadership-advisor` เอง | 43 |

skill ทำงานเมื่อคุณพิมพ์ชื่อ แต่แทบไม่ทำงานเอง

### 2. สาเหตุหลัก: คำอธิบาย skill ถูกตัดทิ้ง

Claude Code มีงบรายการ skill ร่วมกันทุก plugin (1% ของ context) เมื่อเกิน ระบบเก็บไว้แค่ชื่อ และ skill ที่เหลือแค่ชื่อจะ **ไม่ถูกเลือกเอง** ทำงานเฉพาะตอนพิมพ์ชื่อ

ใน session นี้ จาก skill ของ `agent-skill` ที่แสดง มีแค่ 2 hub ที่ยังมีคำอธิบาย (`promethean-parthenon`, `athena-erechtheion`) อีก 16 ตัวเหลือแค่ชื่อ เช่น `chronos-artemis`, `hermes-olympus`, `obsidian-vault`, `lighthouse`, `flutter`, `supabase-senior`, `data-analyze`

สาเหตุที่งบเต็ม: มี plugin ติดตั้งอยู่ประมาณ 17 ตัว รวมราว 200 skill แข่งกัน

| กลุ่ม | ตัวอย่าง | ใช้จริง |
| --- | --- | --- |
| ไม่เคยใช้ | `bio-research` (10+ skill), `product-tracking-skills` (7), `operations` (9), `enterprise-search` (5), `cowork-plugin-management` | 0 ครั้ง |
| ซ้ำกับของคุณเอง | `anthropic-skills:obsidian-vault`, `:project-file-structure`, `:skill-creator`, `:lighthouse-score-optimizer` | ซ้ำกับ skill ใน repo นี้ |
| ซ้ำหน้าที่กับ hub | `engineering:debug`, `:code-review`, `:testing-strategy`, `design:*` | แย่งงานกับ promethean / athena |
| สำเนาซ้ำของ library นี้ | `agent-skill` ติดตั้ง 2 ทาง: แบบ user (`agent-skill@tp-job-skills`) และแบบ sync จาก claude.ai | คำอธิบายเดียวกันถูกนับ 2 รอบ |

### 3. งานที่คุณทำจริง

| โปรเจกต์ | session | prompt | งานหลัก |
| --- | --- | --- | --- |
| CMAS | 131 | 1,622 | thesis/รายงาน, Excel/VBA/ข้อมูล, diagram, backend, deploy, แก้ bug |
| agent-skill | 32 | 225 | เขียนและจัด skill |
| PERN apexops-i | 29 | 236 | UI, ปฏิทิน/งาน, requirement |
| Flutter VAYA-App | 16 | 334 | Flutter, test, git |
| React/MERN อื่น ๆ | ~35 | ~300 | เว็บ, UI |

- **ภาษา:** prompt ราว 54% เป็นภาษาไทย คำสั่งที่ trigger skill จึงต้องมีคำไทยด้วย
- **เครื่องมือ:** ใช้ browser ตรวจหน้าเว็บหนักมาก (7,000+ ครั้ง) และ Bash
- **งานเอกสาร:** thesis, รายงาน, diagram และ Excel เป็นงานก้อนใหญ่ที่สุด แต่ไม่มี hub ดูแล skill ที่เกี่ยวข้อง (`drawio-diagrams`, `data-analyze`, `knowledge-base`, `obsidian-vault`) กระจายอยู่และเหลือแค่ชื่อ

---

## เป้าหมาย

1. งานทั่วไปของคุณเลือก skill ที่ถูกเองโดยไม่ต้องพิมพ์ชื่อ วัดด้วยชุด eval จาก prompt จริงของคุณ
2. skill ที่ active น้อยลงและไม่ซ้ำกัน ให้คำอธิบายทุกตัวอยู่ในงบ
3. hub ส่งงานต่อกันได้เป็นสายเดียว (requirement → แผน → ลงมือ → ทดสอบ → รายงาน)
4. แหล่งเดียว: repo นี้คือต้นฉบับ ทั้ง Claude Code และ claude.ai ใช้ชุดเดียวกัน

---

## แผนงาน 5 ระยะ

### ระยะ 0 — วัดค่าฐาน (ไม่แก้อะไร)

- ทำชุด eval ใหม่ `evals/trigger/real-*` จาก prompt จริงของคุณ ~40 ข้อ (ไทยและอังกฤษ) แต่ละข้อระบุ skill ที่ควรทำงาน
- รัน `claude plugin eval` เก็บอัตราการเลือก skill ถูกก่อนเริ่มแก้

### ระยะ 1 — ลดการแข่งขันในรายการ skill (ได้ผลมากที่สุด, แก้ settings ไม่ใช่ repo)

| ทำ | ผล |
| --- | --- |
| ปิด plugin ที่ไม่เคยใช้ (รายการให้คุณเลือก) | คืนงบหลายพันตัวอักษร |
| ลบ skill ที่ซ้ำกับของคุณออกจาก claude.ai (`obsidian-vault`, `project-file-structure`, `skill-creator`, `lighthouse-score-optimizer`) | ไม่มีสองตัวแย่งงานเดียวกัน |
| เลือกทางติดตั้ง `agent-skill` ทางเดียว | ไม่นับซ้ำ 2 รอบ |
| ถ้ายังไม่พอ: เพิ่ม `skillListingBudgetFraction` | งบใหญ่ขึ้น แลกกับ context |

ทุกข้อเป็นการตั้งค่าของคุณ ผมจะเสนอรายการ แล้วคุณกดยืนยันเอง

### ระยะ 2 — จัด library ใหม่ตามงานจริง

ลด active set จาก 19 รายการ เหลือราว 8 รายการ โดยให้ hub รับงานเป็นกลุ่ม

| รายการ active | ดูแล | spoke |
| --- | --- | --- |
| `promethean-parthenon` (เดิม) | วิศวกรรม, bug, security, test, requirement | 13 ตัวเดิม |
| `athena-erechtheion` (เดิม) | ดีไซน์ | 5 ตัวเดิม |
| `hermes-olympus` (เดิม) | AI agent, MCP | — |
| `chronos-artemis` (เดิม) | ปฏิทิน, ClickUp | — |
| **hub ใหม่: เอกสารและความรู้** (ชื่อเสนอ `mnemosyne-museion`) | thesis, รายงาน, diagram, Excel/ข้อมูล, Obsidian, การสอน | `drawio-diagrams`, `data-analyze`, `knowledge-base`, `obsidian-vault`, `cs-course-designer` |
| **hub ใหม่: ส่งมอบเว็บ** (ชื่อเสนอ `hephaestus-forge`) | deploy, Vercel, Lighthouse, React performance, JS clean code | `deploy-to-vercel`, `vercel-cli-with-tokens`, `lighthouse`, `vercel-react-best-practices`, `clean-code-javascript`, `ai-web-product-craft` |
| standalone | ระบุ stack ชัด จึงสั้นและไม่ชนใคร | `flutter`, `supabase-senior`, `java-api-performance`, `archery` |

การเพิ่ม hub ตาม CLAUDE.md ต้องมี bundle, คำอธิบายรวม trigger ทุก spoke ไม่เกิน 1,024 ตัวอักษร และผ่าน trigger eval

### ระยะ 3 — ให้ทำงานอัตโนมัติแม้คำอธิบายถูกตัด

| กลไก | ทำงานยังไง |
| --- | --- |
| **ตารางนำทางใน `~/.claude/CLAUDE.md`** | ไฟล์นี้โหลดทุก session เสมอ ไม่โดนตัดงบ ใส่ตารางสั้น ๆ "งานแบบนี้ → เปิด skill นี้" ทั้งคำไทยและอังกฤษ |
| **คำ trigger ภาษาไทยในทุกคำอธิบาย** | เพราะ prompt ครึ่งหนึ่งเป็นไทย |
| **CLAUDE.md รายโปรเจกต์** (CMAS, VAYA, apexops) | บอก hub หลักของโปรเจกต์นั้น เช่น CMAS → เอกสารและข้อมูลก่อน |
| ทางเลือก: hook `prompt.submit` | ฉีดคำแนะนำ skill จากคำในข้อความ ใช้เมื่อสองข้อบนยังไม่พอ |

### ระยะ 4 — ให้ hub ทำงานร่วมกัน

- **สัญญาส่งต่องาน:** แต่ละ hub จบงานด้วยรูปแบบผลลัพธ์ที่ hub ถัดไปอ่านได้ เช่น requirement-gathering ส่งรายการ requirement ที่ test-strategy และ hub เอกสารนำไปใช้ต่อ
- **อ้างถึงกันเป็นข้อความ ไม่ใช่ลิงก์:** ตามกฎ hub-and-spoke ของ repo ("ถ้าต้องทำ diagram ให้ใช้ hub เอกสาร")
- **claude.ai กับ Claude Code ใช้ชุดเดียวกัน:** สร้าง zip จาก repo ด้วย script เดียว อัปโหลดแทนชุดเก่า แทนการแก้สองที่
- **วัดผลซ้ำ:** รันชุด eval จากระยะ 0 อีกครั้ง เทียบอัตราการเลือกถูก

---

## เรื่องที่คุณต้องตัดสินใจ

1. **plugin ที่จะปิด:** `bio-research`, `product-tracking-skills`, `operations`, `enterprise-search`, `cowork-plugin-management` ไม่เคยใช้เลย ส่วน `data`, `figma`, `design`, `engineering`, `product-management` ใช้บ้างหรือซ้ำกับของคุณ
2. **hub ใหม่ 2 ตัว:** เอาทั้งคู่, เอาแค่ hub เอกสาร หรือไม่เพิ่ม และชื่อที่ชอบ
3. **ทางติดตั้ง agent-skill:** ใช้แบบ marketplace ใน Claude Code อย่างเดียว หรือคงแบบ sync จาก claude.ai ไว้ด้วย
4. **hook อัตโนมัติ:** เริ่มจาก CLAUDE.md ก่อน แล้วค่อยเพิ่ม hook ถ้าไม่พอ (แนะนำ) หรือทำ hook เลย

## สิ่งที่แผนนี้ไม่ครอบคลุม

- **แชทใน claude.ai:** ผมเห็นแค่ transcript ของ Claude Code ในเครื่องนี้ ไม่เห็นประวัติแชทบนเว็บ ถ้าอยากรวมด้วย ส่งออกประวัติจาก claude.ai มาให้ได้
- **ตัวเลขหมวดงานเป็นค่าประมาณ:** จัดหมวดด้วยคำค้น หนึ่ง prompt อาจนับได้หลายหมวด
