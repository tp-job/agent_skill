# Academic mode — NFRs in a thesis or project report

## Contents

- Where each part goes
- Justifying a number
- Common examiner questions
- Results table for the results chapter
- Thai academic wording

---

## Where each part goes

Thai undergraduate theses (ปริญญานิพนธ์) usually follow a five-chapter structure. NFR material is spread across chapters 2 to 4:

| Chapter | Put here |
| --- | --- |
| 2 Literature and theory (ทฤษฎีและงานวิจัยที่เกี่ยวข้อง) | the quality model (ISO/IEC 25010:2023 and why it was chosen); the response-time thresholds and their sources; the WCAG contrast formula; the SUS scoring method; any statistics used (mean, SD, p95) |
| 3 Method and design (วิธีดำเนินงาน) | the applicability table (14 categories, IN or N/A with reasons); the NFR table with Scale, Meter, Condition and Must; the verification plan (method and tool per NFR); measurement conditions; the user-test protocol |
| 4 Results (ผลการดำเนินงาน) | the results table (measured value against threshold); evidence in an appendix; failures with their decision (fix, relax, or accept the risk) |
| Appendix | color-pair contrast table, SUS raw answers, k6 summary, accuracy oracle cases, access-control matrix |

A table that says *how the system meets* an NFR ("uses TypeScript strict mode") is design, and belongs in chapter 3. It is not verification. Add the columns **Verification method** and **Pass criterion**, and report the measured result in chapter 4.

## Justifying a number

Every threshold must fall into one of two kinds, and the text has to say which.

| Kind | Wording pattern |
| --- | --- |
| **From a standard or study** | "ไม่เกิน 2 วินาที เพื่อรักษาความต่อเนื่องของความคิดผู้ใช้ (Miller, 1968; Nielsen, 1993)" |
| **Project target** | "ผู้ใช้พร้อมกัน 30 คน ซึ่งคณะผู้จัดทำกำหนดจากจำนวนอาจารย์ในภาควิชา (28 คน) เผื่อร้อยละ 10" |

BAD: "ระบบต้องรองรับผู้ใช้จำนวนมาก" (no number, no source)
BAD: "ร้อยละ 80 ตามมาตรฐาน" (no standard actually says 80%)
BETTER: "อัตราการทำภารกิจสำเร็จไม่ต่ำกว่าร้อยละ 80 (เกณฑ์ของโครงงาน อ้างอิงค่าเฉลี่ยประมาณร้อยละ 78 จาก Sauro และ Lewis, 2016)"

## Common examiner questions

Prepare one sentence of evidence for each of these:

| Question | Answer with |
| --- | --- |
| "2 วินาทีนี้วัดยังไง วัดกี่ครั้ง" | the Meter and Condition: tool, dataset, n = 30, p95 |
| "ทำไมเลือกเกณฑ์นี้" | the source, or the project-target rationale |
| "ความคมชัดของสีผ่านไหม เท่าไหร่" | the contrast table with ratios, plus SC 1.4.3 and 1.4.11 |
| "ใช้งานง่ายวัดจากอะไร นอกจากความเห็นผู้เชี่ยวชาญ" | task success, time on task, SUS from real users |
| "ถ้าเซิร์ฟเวอร์หลับ (cold start) ผลจะเป็นยังไง" | the cold-start figure reported separately |
| "ข้อที่ไม่ผ่านทำยังไง" | the fix, relax or accept-the-risk decision |
| "คำนวณถูกต้องเทียบกับอะไร" | the oracle cases: hand calculation and number of cases |

## Results table for the results chapter

```markdown
| รหัส | ข้อกำหนด | วิธีตรวจสอบ | เกณฑ์ | ผลที่วัดได้ | ผล |
| --- | --- | --- | --- | --- | --- |
| PF-01 | เวลาแสดงหน้าตารางคะแนน | Performance API, n = 30 | p95 ≤ 2.0 วินาที | median 0.84, p95 1.31 วินาที | ผ่าน |
| AX-01 | ความต่างของสีข้อความเนื้อหา | contrast_check.py ทุกคู่สี | ≥ 4.5:1 | ต่ำสุด 5.12:1 | ผ่าน |
| UX-04 | คะแนน SUS | แบบสอบถาม SUS, n = 5 | ≥ 68 | 74.5 (SD 6.2) | ผ่าน |
```

Under the table, state the environment: machine, browser and version, hosting, dataset, and date.

## Thai academic wording

| English | Thai term commonly used |
| --- | --- |
| non-functional requirement | ข้อกำหนดที่ไม่ใช่เชิงหน้าที่ |
| verification / validation | การทวนสอบ / การตรวจสอบความถูกต้อง |
| pass criterion / threshold | เกณฑ์การผ่าน / ค่าเกณฑ์ |
| response time | เวลาในการตอบสนอง |
| contrast ratio | อัตราส่วนความต่างของสี |
| task success rate | อัตราการทำภารกิจสำเร็จ |
| percentile 95 | เปอร์เซ็นไทล์ที่ 95 |
| measurement condition | เงื่อนไขการวัด |
| project target | เกณฑ์ที่คณะผู้จัดทำกำหนด |

Format citations with [sources](sources.md), and follow the faculty's thesis manual where it differs from that format.
