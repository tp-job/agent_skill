---

## name: software-design-2024 description: > Comprehensive software design knowledge base extracted from "Design-2024-V1.6" course material. Use this skill whenever a user asks about UML diagrams (Use Case, Class, Activity, Sequence), software architecture patterns (Monolithic, SOA, Microservices, 3-tier), UI/UX design principles, Material Design guidelines, Nielsen's Heuristics, ERD/database design, wireframes, mockups, prototypes, color theory, or any software design concept. Trigger this skill for design reviews, architecture decisions, diagram explanations, usability evaluations, and database schema planning. author: surachai version: 1.6 source: Design-2024-V1.6.pdf (212 pages, Jan 2025) language: Thai + English

# Software Design 2024 — Agent Skill

This skill contains the full knowledge base from the Design-2024-V1.6 course. All content below is sourced directly from the PDF and is 100% accurate.

---

## Table of Contents

1. [High-Level vs Low-Level Design](https://claude.ai/chat/941e7dab-ca4d-411e-97eb-f8967273f846#1-high-level-vs-low-level-design)
2. [UML — Use Case Diagram](https://claude.ai/chat/941e7dab-ca4d-411e-97eb-f8967273f846#2-uml--use-case-diagram)
3. [UML — Class Diagram](https://claude.ai/chat/941e7dab-ca4d-411e-97eb-f8967273f846#3-uml--class-diagram)
4. [UML — Activity Diagram](https://claude.ai/chat/941e7dab-ca4d-411e-97eb-f8967273f846#4-uml--activity-diagram)
5. [UML — Sequence Diagram](https://claude.ai/chat/941e7dab-ca4d-411e-97eb-f8967273f846#5-uml--sequence-diagram)
6. [Software Architecture Patterns](https://claude.ai/chat/941e7dab-ca4d-411e-97eb-f8967273f846#6-software-architecture-patterns)
7. [UI/UX Design](https://claude.ai/chat/941e7dab-ca4d-411e-97eb-f8967273f846#7-uiux-design)
8. [Material Design](https://claude.ai/chat/941e7dab-ca4d-411e-97eb-f8967273f846#8-material-design)
9. [Color Theory](https://claude.ai/chat/941e7dab-ca4d-411e-97eb-f8967273f846#9-color-theory)
10. [Database Design — ERD](https://claude.ai/chat/941e7dab-ca4d-411e-97eb-f8967273f846#10-database-design--erd)

---

## 1. High-Level vs Low-Level Design

### High-Level Design (HLD)

- **Use Case Diagram** — ภาพรวมของระบบ
- **Activity Diagram** — ขั้นตอนการทำงาน
- **System Architecture Design** — สถาปัตยกรรมระบบ

### Low-Level Design (Detail Design)

- **Class/Component Design** — ออกแบบคลาสและคอมโพเนนต์
- **Database Design** — ออกแบบฐานข้อมูล
- **UI/UX Details Design** — ออกแบบหน้าจอละเอียด
- **API Design** — ออกแบบ API

---

## 2. UML — Use Case Diagram

**Purpose:** แสดงภาพรวมของระบบและความสัมพันธ์ระหว่าง Actor กับ Use Case

### Basic Elements (องค์ประกอบพื้นฐาน)

|Element|Description|
|---|---|
|**Actor**|ผู้ใช้หรือระบบภายนอกที่มีปฏิสัมพันธ์กับระบบ|
|**Use Case**|ฟังก์ชันที่ระบบมี|
|**System Boundary**|ขอบเขตของระบบ|
|**Relationships**|ความสัมพันธ์ระหว่างองค์ประกอบต่างๆ|

### Naming Conventions (หลักการตั้งชื่อ)

- **Use Case:** ใช้คำกริยา+คำนาม (verb+noun) เช่น "Register Account"
- **Actor:** ใช้คำนามที่สื่อถึงบทบาท เช่น "Customer", "Administrator"
- ชื่อต้องสั้น กระชับ และสื่อความหมายชัดเจน

### Types of Relationships (ประเภทของ Relationships)

|Relationship|Symbol|Description|
|---|---|---|
|**Association**|เส้นตรง|ความสัมพันธ์พื้นฐานระหว่าง Actor กับ Use Case|
|**Include**|`<<include>>`|Use Case หนึ่งต้องเรียกใช้อีก Use Case หนึ่ง|
|**Extend**|`<<extend>>`|Use Case หนึ่งอาจขยายพฤติกรรมของอีก Use Case หนึ่ง|
|**Generalization**|ลูกศรสามเหลี่ยมทึบ|ความสัมพันธ์แบบทั่วไป-เฉพาะ|

### Design Principles (หลักการออกแบบ)

- **Single Responsibility:** แต่ละ Use Case ควรมีหน้าที่เดียวที่ชัดเจน
- **Abstraction:** แสดงเฉพาะรายละเอียดที่สำคัญ
- **Modularity:** แบ่งฟังก์ชันเป็นส่วนๆ อย่างเหมาะสม
- **Cohesion:** ความสัมพันธ์ภายใน Use Case ต้องเข้ากันได้ดี

### Recommended Tools

- PlantUML
- StarUML
- Visual Paradigm
- UMLet

---

## 3. UML — Class Diagram

**Purpose:** แสดงโครงสร้างของคลาสทั้งหมดในระบบ และความสัมพันธ์ระหว่างคลาส (Object-Oriented Design)

### Class Components (องค์ประกอบของ Class)

**Class Name**

- ขึ้นต้นด้วยตัวพิมพ์ใหญ่
- ใช้คำนาม
- สื่อความหมายชัดเจน

**Attributes (คุณลักษณะ)**

- ตัวแปรที่เก็บข้อมูลของคลาส
- ระบุ Access Modifier (+, -, #, ~)
- ระบุชนิดข้อมูล

**Access Modifiers**

|Symbol|Modifier|
|---|---|
|`+`|Public|
|`-`|Private|
|`#`|Protected|
|`~`|Package/Default|

**Operations (การดำเนินการ)**

- เมธอดที่ใช้จัดการข้อมูล
- ระบุ Access Modifier
- ระบุพารามิเตอร์และค่าที่ส่งกลับ

### Class Relationships (ความสัมพันธ์ระหว่างคลาส)

#### Association (ความสัมพันธ์แบบเชื่อมโยง)

- คลาสมีความสัมพันธ์กัน
- ระบุจำนวนความสัมพันธ์ด้วย Multiplicity:

|Notation|Meaning|
|---|---|
|`1`|หนึ่งต่อหนึ่ง|
|`0..1`|มีหรือไม่มีก็ได้ (ไม่เกิน 1)|
|`*` หรือ `0..*`|มีได้หลายอัน (0 ถึงหลายอัน)|
|`1..*`|มีได้หลายอัน (อย่างน้อย 1)|
|`n..m`|มีได้ตั้งแต่ n ถึง m|
|`+`|มีการจัดเรียงลำดับ|

#### Aggregation (ความสัมพันธ์แบบรวมกลุ่ม)

- ส่วนประกอบสามารถแยกจากกันได้
- ส่วนย่อยสามารถอยู่ได้โดยอิสระ

#### Composition (ความสัมพันธ์แบบประกอบ)

- ส่วนประกอบไม่สามารถแยกจากกันได้
- ส่วนย่อยไม่สามารถอยู่ได้โดยอิสระ

#### Inheritance (การสืบทอด)

- คลาสลูกสืบทอดคุณสมบัติจากคลาสแม่
- ใช้หลักการ "is a"

---

## 4. UML — Activity Diagram

**Purpose:** แสดงลำดับขั้นตอนการทำงาน (Workflow), อธิบายรายละเอียดการทำงาน, ระบุผู้รับผิดชอบชัดเจน

### Node Types (ประเภทของ Node)

|Symbol|Name|Description|
|---|---|---|
|`●`|Initial Node|จุดเริ่มต้นของกิจกรรม — มีได้เพียงจุดเดียว|
|`⬤`|Final Node|จุดสิ้นสุดของกิจกรรม — มีได้หลายจุด|
|`🛑`|Flow Final Node|จุดสิ้นสุดของ flow บางส่วน — ไม่ใช่จุดสิ้นสุดของทั้งกิจกรรม|
|`[ ]`|Action|กิจกรรมย่อยที่ไม่สามารถแบ่งย่อยได้อีก เช่น "ตรวจสอบรหัสผ่าน"|
|`[rounded]`|Activity|กลุ่มของกิจกรรมย่อย เช่น "กระบวนการสั่งซื้อ"|
|`→`|Flow|แสดงทิศทางการไหลของกิจกรรม|
|`◇`|Decision Node|จุดตัดสินใจ Yes/No — มีทางออกอย่างน้อย 2 ทาง|
|`═`|Fork/Join|Fork: แยกการทำงานแบบขนาน / Join: รวมการทำงานแบบขนาน|
|`○`|Merge Node|รวมเส้นทางหลังการตัดสินใจ — ไม่ต้องรอให้ทุกเส้นทางเสร็จ|

### Swimlanes

- แบ่งความรับผิดชอบของแต่ละส่วน
- แนวตั้งหรือแนวนอนก็ได้
- ตัวอย่างการแบ่ง:
    - ตามแผนก (ฝ่ายขาย, ฝ่ายการเงิน)
    - ตามระบบ (Frontend, Backend)
    - ตามบทบาท (ลูกค้า, พนักงาน)

---

## 5. UML — Sequence Diagram

**Purpose:** แสดงลำดับการทำงานของระบบในแต่ละ Use Case (interaction ระหว่าง objects ตามเวลา)

> _(Sequence Diagram content is covered visually in the slides — use this section as a trigger for explaining message flows, lifelines, activation bars, and synchronous/asynchronous calls.)_

---

## 6. Software Architecture Patterns

### Service Layers

|Layer|Thai Name|Responsibility|
|---|---|---|
|**Presentation Logic**|ส่วนติดต่อผู้ใช้|การติดต่อระหว่างผู้ใช้กับ Application|
|**Application Logic (Business Logic)**|ตรรกะทางธุรกิจ|จัดการด้านโปรแกรมประยุกต์|
|**Data Access Logic**|การเข้าถึงข้อมูล|คำสั่งรองขอดูข้อมูล, จัดเก็บข้อมูลลง DB|
|**Data Storage**|จัดเก็บข้อมูล|บริการเกี่ยวกับการจัดเก็บข้อมูลลงฐานข้อมูลจริง|

### Architecture Patterns

#### Single-location System

- ระบบงานแบบรวมศูนย์ ทุกอย่างอยู่ที่เดียว

#### 2-Tier Architecture (Client/Server)

- Desktop App / Mobile App → Server
- ข้อเสีย: Client ทำงานหนักเกินไป, เมื่อเปลี่ยนแปลง App ต้องติดตั้งให้กับ Client ทุกเครื่อง

#### 3-Tier Architecture

|Tier|Description|
|---|---|
|**Presentation Tier**|หน้าเว็บแบบ Static หรือ Dynamic (front-end)|
|**Application/Logic Tier**|ประมวลผล dynamic โดย application server เช่น Java EE, PHP, ASP.net (middleware)|
|**Data Tier**|ฐานข้อมูล + DBMS (back-end)|

#### N-Tier Architecture

- Mobile App / Webpage / Desktop App → Presentation Tier → API/Caching/Security Tier → Application Tier → Data Tier

#### Monolithic Architecture

- ทุกส่วนทำงานรวมกันในแอปพลิเคชันเดียว
- ✅ ง่ายในการพัฒนาและบำรุงรักษา
- ❌ ยากในการขยายและการปรับปรุงระบบ

#### Service-Oriented Architecture (SOA)

- แยก software ออกเป็นกลุ่มของการบริการ
- แต่ละ Service ตอบสนองต่อการทำงานใดงานหนึ่ง
- เชื่อมต่อกันด้วยมาตรฐานการเชื่อมต่อ
- ✅ ง่ายต่อการขยายระบบและการแก้ไข
- ❌ ซับซ้อนในการพัฒนาและการบำรุงรักษา

#### Microservices Architecture

- พัฒนาต่อจาก SOA
- แบ่งแยกระบบออกเป็นบริการเล็กๆ เป็นอิสระต่อกัน
- ทีมพัฒนาแบ่งงานได้ง่าย เน้นความเร็วและความยืดหยุ่น
- ❌ มีความซับซ้อนในการพัฒนาและบำรุงรักษา

### Microservices vs SOA Comparison

|Aspect|SOA|Microservices|
|---|---|---|
|Scope|Enterprise-wide services|Single application decomposed|
|Communication|ESB (Enterprise Service Bus)|Lightweight APIs (REST, gRPC)|
|Deployment|Typically together|Independently deployable|
|Data|Shared database common|Each service owns its database|

### 3-Tier Architecture vs MVC Pattern

- **3-Tier:** แบ่งแยกแอปพลิเคชันเป็น 3 ชั้นอย่างชัดเจน (physical separation)
- **MVC:** แยกส่วนประกอบภายในแอปพลิเคชัน (logical separation within one tier)

---

## 7. UI/UX Design

### Key Definitions

- **UX (User Experience):** ออกแบบกระบวนการใช้งานให้ผู้ใช้พึงพอใจ — ตรงตามความต้องการ, ใช้งานง่าย, มีลำดับขั้นตอนชัดเจน
- **UI (User Interface):** เติมเต็ม UX ให้มีความสวยงาม เช่น การวางตัวอักษร, ช่องว่าง, ขนาดฟอนต์

### Wireframe, Mockup, Prototype

|Stage|Description|
|---|---|
|**Wireframe**|โครงร่างคร่าวๆ ของแอปพลิเคชัน อธิบายฟีเจอร์ของแต่ละหน้า การวางตำแหน่งข้อมูล การเชื่อมต่อการทำงาน|
|**Mockup**|ใส่รายละเอียดเพิ่มเติมความสวยงาม — ยังไม่สามารถทดลองใช้จริงได้|
|**Prototype**|ทำให้มี interaction หรือองค์ประกอบอื่นๆ ที่เหมือนงานจริง แต่ขาดลอจิกการทำงานจริง|

### Wireframe Steps (ขั้นตอน)

1. สรุปความต้องการลูกค้า
2. วางแผนโครงสร้างแอป — กำหนดจุดประสงค์ของแต่ละหน้า
3. เขียน Sitemap ระบุความสัมพันธ์ของแต่ละหน้า
4. วาง Layout ของแต่ละหน้าใน Wireframe
5. ระบุ action ที่จะต้องทำในหน้านั้น (ฟังก์ชัน, แนวการดีไซน์, การเชื่อมต่อ DB)

### Wireframe Design Tools

- **Figma** — https://www.figma.com/
- **MockFlow** — https://mockflow.com/
- **Moqups** — https://moqups.com/

### Usability

**5 Dimensions of Usability:**

1. **Ease of Use** — ความง่ายในการใช้งาน
2. **Efficiency** — ประสิทธิภาพ
3. **Learnability** — ความง่ายในการเรียนรู้
4. **Error Prevention** — ป้องกันข้อผิดพลาด
5. **User Satisfaction** — ความพึงพอใจของผู้ใช้

**How to Measure Usability:**

- **Usability Testing:** วัดค่าทางปริมาณ (เวลา, จำนวนคลิก) + ความพึงพอใจผ่านสัมภาษณ์
- **Heuristics Evaluation:** ประเมินโดยผู้เชี่ยวชาญ เช่น Nielsen's Heuristics

---

### Nielsen's 10 Heuristics

|#|Heuristic|Description|
|---|---|---|
|1|**Visibility of system status**|แสดงสถานะของระบบอย่างชัดเจน|
|2|**Match between system and real world**|ใช้ภาษาและแนวคิดที่ผู้ใช้คุ้นเคย|
|3|**User control and freedom**|ผู้ใช้ต้องสามารถยกเลิก/แก้ไขได้ง่าย|
|4|**Consistency and standards**|ความสอดคล้องและมาตรฐาน|
|5|**Error prevention**|การป้องกันข้อผิดพลาด|
|6|**Recognition rather than recall**|การรู้จำแทนการสะกดจำ|
|7|**Flexibility and efficiency of use**|ความยืดหยุ่นและประสิทธิภาพในการใช้งาน|
|8|**Aesthetic and minimalist design**|การออกแบบที่สวยงามและเรียบง่าย|
|9|**Help users recognize, diagnose, and recover from errors**|ช่วยผู้ใช้ระบุปัญหาและแก้ไขข้อผิดพลาด|
|10|**Help and documentation**|ความช่วยเหลือและเอกสารอ้างอิง|

#### Nielsen's Heuristics — Online Shopping Examples

|Heuristic|Online Shopping Application|
|---|---|
|Visibility of system status|แสดงสถานะ "กำลังดำเนินการ", "สำเร็จ", "เกิดข้อผิดพลาด"; ติดตามสถานะการจัดส่ง|
|Match with real world|ใช้คำเช่น "เพิ่มลงตะกร้า", "ชำระเงิน", "ดูรายละเอียดสินค้า"|
|User control and freedom|แก้ไขหรือยกเลิกการสั่งซื้อก่อนชำระเงิน; เลือกวิธีชำระเงินได้หลากหลาย|
|Consistency and standards|ใช้ตัวอักษรและขนาดเหมือนกันทุกหน้า; สัญลักษณ์เหมือนกันทั้งระบบ|
|Error prevention|ตรวจสอบรูปแบบอีเมล, รหัสผ่าน; ตรวจสอบความสมบูรณ์ของข้อมูล|
|Recognition not recall|แสดงรูปภาพสินค้าพร้อมชื่อ; จัดหมวดหมู่ด้วย filter|
|Flexibility|ระดับสมาชิก VIP; ปรับแต่งหน้าจอส่วนตัว; เครื่องมือค้นหาที่มีประสิทธิภาพ|
|Aesthetic design|Interface เรียบง่าย; รูปภาพสินค้าคุณภาพสูง; สีและองค์ประกอบสอดคล้องกัน|
|Recover from errors|ข้อความแจ้งเตือนชัดเจน; ตัวช่วยและคำแนะนำ; เก็บข้อมูลให้เรียกคืนได้|
|Help and documentation|คู่มือการใช้งาน; FAQ; ปุ่มช่วยเหลือในหน้าจอ; ช่องทางติดต่อ Support|

---

### Don't Make Me Think (Steve Krug)

**Core Principles:**

- ออกแบบให้ผู้ใช้เข้าถึงข้อมูลหรือฟังก์ชันได้โดยรวดเร็ว
- ลดความยุ่งยากและความสับสนในการใช้งาน
- Interface ควรใช้งานได้ง่าย เข้าใจง่าย โดยไม่ต้องคิด

**Key Areas:**

- **Navigation:** สร้างเมนูที่เข้าใจง่าย, สัญลักษณ์นำทางชัดเจน
- **Forms:** แบบฟอรม์คุ้นเคย, ลดความยุ่งยาก, มีการแสดงข้อความช่วยเหลือ
- **Credibility:** สร้างความน่าเชื่อถือด้วยข้อมูลที่ถูกต้องและอัพเดท

---

### Nick Kolenda — UX Design Guide

#### FOCUS

|Principle|Description|
|---|---|
|**Create an Entry Point**|ทุก Interface ต้องการองค์ประกอบเฉพาะที่ดึงดูดสายตา เน้นองค์ประกอบที่สำคัญที่สุด|
|**Guide Eye Flow**|นำสายตาผู้ใช้ผ่านการออกแบบ — รายละเอียดพื้นหลังที่ไม่ชัด, องค์ประกอบที่ซ้อนทับกันข้ามส่วน|
|**Group Similar Elements**|จัดกลุ่มให้ใกล้กัน, ใช้สีเดียวกัน, จัดกลุ่มไว้ภายใน container; วางหัวข้อใกล้กับเนื้อหา; แยกฟังก์ชันสำคัญออกมา|
|**Remove Unnecessary Elements**|รักษาโฟกัสไปที่องค์ประกอบที่สำคัญ; ละเว้นคำแนะนำที่อธิบายตนเอง; ซ่อนรายละเอียดเพิ่มเติมในส่วนที่ขยายได้|
|**Communicate Hidden Sections**|แจ้งให้ผู้ใช้ทราบถ้า Interface ขยายมากกว่าขอบเขตที่มองเห็น|
|**Depict Changes Without Disrupting**|ทำให้ผู้ใช้สังเกตการเปลี่ยนแปลง; ปกป้องการเปลี่ยนแปลงจากการบล็อกฟังก์ชันอื่น; เตือนเมื่อฟังก์ชัน timer จะเกิดขึ้น|

#### UNDERSTANDING

|Principle|Description|
|---|---|
|**Indicate Interactive Items**|ผู้ใช้ควรรู้ว่าสิ่งใดทำได้หรือไม่ — เปลี่ยน cursor, เปลี่ยนองค์ประกอบเมื่อ hover|
|**Provide Feedback**|ให้ข้อเสนอแนะระหว่างและหลังจากการโต้ตอบ|
|**Communicate in Relative Terms**|การจัดเฟรมสัมพันธ์ (Relative) มีความหมายมากกว่าแบบสัมบูรณ์ (Absolute); สื่อสารเวลาสัมพันธ์กับปัจจุบัน|
|**Design for Scannability**|แทรกประเด็นหลักลงในหัวข้อ; วางข้อมูลสำคัญไว้ที่จุดเริ่มต้น|
|**Communicate Expected Outcome**|ผู้ใช้ควรรู้ว่าจะเกิดอะไรขึ้นก่อนที่มันจะเกิดขึ้น; แสดงจำนวนรายการในกลุ่ม; อธิบายปลายทางของลิงก์|
|**Match User Expectations**|เมื่อสื่อสารความคาดหวังที่ถูกต้องแล้ว ตรวจสอบให้เป็นไปตามนั้น|

#### EFFORT

|Principle|Description|
|---|---|
|**Help Users Choose Options**|ลดความซับซ้อนของตัวเลือก; นำเสนอตัวเลือกในจุดเริ่มต้น; เปรียบเทียบคุณลักษณะ; แนะนำทางเลือก|
|**Minimize Waiting**|ลดสีเร้าอารมณ์ด้วยสีโทนเย็น; ให้ผู้ใช้มีส่วนร่วมขณะรอ; ใช้ Skeleton/Placeholder ขณะโหลด|
|**Minimize Reliance on Calculations/Memory**|คำนวณจำนวนรายการคงเหลือ; เก็บข้อมูลที่เกี่ยวข้องไว้ให้เห็น; ระบุรายการที่ผู้ใช้ดูไปแล้ว|
|**Minimize Redundant Tasks**|อนุญาตให้ทำซ้ำ input ที่ผ่านมา; กรอกช่อง input ล่วงหน้าด้วยคำตอบทั่วไป; วางคำตอบทั่วไปไว้ที่ด้านบน|
|**Guide Users Toward Their Goal**|เริ่มต้นความก้าวหน้ามากกว่าศูนย์; กระตุ้นผู้ใช้ไปสู่จุดที่มีคุณค่า|

#### ERRORS

|Principle|Description|
|---|---|
|**Prevent Errors**|ปิดการใช้งานปุ่มเมื่อผู้ใช้คลิกไปแล้ว; เปิดใช้ฟังก์ชันเมื่อจำเป็นเท่านั้น; เพิ่มข้อจำกัดให้กับการเปลี่ยนแปลงที่ไม่สามารถย้อนกลับได้|
|**Communicate Requirements**|อธิบายสิ่งที่จำเป็นในการป้อน input; ระบุองค์ประกอบที่จำเป็น; จับคู่ขนาดแบบฟอร์มกับขนาด input|
|**Monitor Error Signals**|ตรวจสอบว่ามีการใช้งานอยู่หรือไม่; ตรวจสอบการส่งที่ว่างเปล่า; ยืนยันเจตนาสำหรับการดำเนินการซ้ำๆ|
|**Provide Easy Revert/Escape**|ช่วยให้ผู้ใช้ย้อนกลับถ้าผิดพลาดแบบไม่ตั้งใจ; ให้ผู้ใช้ Undo/Redo ได้หลายระดับ|

#### COMPATIBILITY

|Principle|Description|
|---|---|
|**Accommodate Skill/Knowledge**|ช่วยเหลือผู้ใช้มือใหม่โดยไม่เป็นอุปสรรคผู้ใช้ที่เชี่ยวชาญ; ช่วยให้เข้าใจภาษาที่ไม่คุ้นเคย|
|**Accommodate Goal/Workflow**|ให้ผู้ใช้ควบคุมลักษณะและลำดับขององค์ประกอบ; ให้ผู้ใช้ไปที่ตำแหน่งโดยตรง|
|**Maximize Accessibility**|สื่อสารข้อมูลในรูปแบบต่างๆ; จัดหมวดหมู่องค์ประกอบที่มีความหมาย|
|**Maximize Input Compatibility**|ยอมรับรูปแบบ input ต่างๆ; จัดการ input ที่การจัดรูปแบบไม่เหมาะสม|

---

### UI Design Principles

#### Simplicity and Clarity (ความเรียบง่ายและความชัดเจน)

**Reducing Complexity:**

- หลักการ: ลดองค์ประกอบที่ไม่จำเป็น แต่คงประสิทธิภาพการใช้งาน
- ✅ ตัวอย่างที่ดี: Google Search (โลโก้ + ช่องค้นหา), Apple App Store, Spotify
- ❌ ควรหลีกเลี่ยง: เมนูซ้อนหลายชั้น, ปุ่มกดซ้ำซ้อน, แสดงข้อมูลมากเกินความจำเป็น

**Organized Layout:**

- ใช้ Grid system และ Visual hierarchy
- ใช้ระยะห่างที่สม่ำเสมอ (8dp grid system)
- จัดกลุ่มข้อมูลที่เกี่ยวข้องไว้ด้วยกัน
- ✅ ตัวอย่าง: Gmail (list layout), Instagram (grid layout), Medium (typography hierarchy)

#### Consistency (ความสอดคล้องและสม่ำเสมอ)

**Visual Consistency — องค์ประกอบที่ต้องรักษาความสอดคล้อง:**

- **สี:** ใช้ color palette ที่กำหนด
- **Typography:** ใช้ font family และขนาดที่กำหนด
- **Icons:** ใช้ชุดไอคอนที่มีสไตล์เดียวกัน
- **Spacing:** ใช้ระยะห่างที่สม่ำเสมอ

**Platform Examples:**

- Google Workspace: Material Icons, สีประจำแบรนด์, Roboto font
- Apple iOS: San Francisco font, SF Symbols, Dynamic Type system

**Behavioral Consistency — การตอบสนองที่สอดคล้อง:**

- การ Navigate ระหว่างหน้า
- การแสดง Feedback
- การจัดการ Error states

#### Responsiveness (การตอบสนองต่อการใช้งาน)

**Visual Feedback — รูปแบบการตอบสนอง:**

- Hover states
- Active states
- Loading states
- Success/Error states

**Button States:**

- Default: สีปกติ
- Hover: เปลี่ยนความเข้มของสี
- Active: เพิ่ม ripple effect
- Disabled: ลดความเข้มของสี

**Animation Guidelines:**

- ใช้ animation ที่มีความหมาย
- ระยะเวลาที่เหมาะสม: **200–300 ms**
- smooth transitions

---

## 8. Material Design

**Reference:** https://m3.material.io

### What is Material Design?

- ระบบการออกแบบที่พัฒนาโดย Google ในปี 2014
- แนวคิดการจำลองวัสดุในโลกดิจิทัล
- สร้างภาษาการออกแบบที่เป็นมาตรฐานเดียวกัน
- รองรับการใช้งานบนทุกอุปกรณ์และขนาดหน้าจอ

### Core Metaphor — Material as a Metaphor

|Property|Description|
|---|---|
|Surface|วัสดุมีพื้นผิวที่สามารถรับแสงและทอดเงาได้|
|Thickness|วัสดุมีความหนา ทำให้เกิดระยะลึกและความสูง|
|Impenetrability|วัสดุไม่สามารถทะลุผ่านกันได้ เหมือนกระดาษจริง|
|Transform|วัสดุสามารถเปลี่ยนรูปร่างได้ผ่านการ transform|
|Merge/Separate|วัสดุสามารถรวมกันหรือแยกออกจากกันได้|

### Material Design Structure

- **Foundations:** Accessibility, Content design, Design tokens, Interaction, Layout
- **Styles:** Color, Icons, Motion, Shape, Typography
- **Components:** App bars, Buttons, Cards, Dialogs, Navigation, Menus, etc.

---

### Foundations: Accessibility

#### Colors and Contrast

**Contrast Ratio Formula:**

```
Contrast Ratio = (L1 + 0.05) / (L2 + 0.05)
L1 = ค่าความสว่างของสีที่สว่างกว่า
L2 = ค่าความสว่างของสีที่มืดกว่า
```

**Luminance Calculation:**

```
ความสว่าง = (R × 0.2126) + (G × 0.7152) + (B × 0.0722)
```

**Examples:**

- สีดำ (#000000) บนพื้นขาว (#FFFFFF): อัตราส่วน = **21:1**
- สีเทา (#767676) บนพื้นขาว (#FFFFFF): อัตราส่วน = **4.54:1**

**Required Contrast Ratios:**

|Text Type|Minimum Contrast|
|---|---|
|Large text (14pt bold / 18pt regular and up) & graphics|3:1 against background|
|Small text|4.5:1 against background|

_Note: Standalone components (e.g., FABs) don't require 3:1 contrast ratio between container and background due to their prominence._

#### Structure — Landmark Roles (W3C ARIA)

|#|Role|Description|
|---|---|---|
|1|**Navigation**|Navigation area|
|2|**Search**|A search field|
|3|**Main**|The main content area (only one per page)|
|4|**Banner**|Site header/banner|
|5|**Complementary**|Sidebar/aside that can stand alone|
|6|**Contentinfo**|Typically the footer|
|7|**Region**|Important content blocks|
|8|**Form**|Takes and stores user info|

#### Structure — Headings

- Identify headings based on content hierarchy
- Headings should NOT skip a level
- Map content to headings (H1–H6) in sequential order
- A single H1 for the page title is recommended

#### Structure — Touch Target Sizes

- **Icons:** 24dp
- **Star icon:** 40dp
- **Touch target on both:** 48dp (~9mm)
- Note: iOS recommends 44×44dp

#### Accessibility — Flow (Focus Order & Key Traversal)

- **Tab:** Moves focus between interactive elements (Tab + Shift reverses direction)
- **Arrow:** Navigate within components
- **Enter:** Activates a link, button, or sends a form

---

### Foundations: Content Design — Alt Text

**Best Practices:**

1. Write alt text for images to provide context to screen reader users
2. Avoid auto-generated file numbers as alt text (e.g., `jpg-0223939-330`)
3. Keep alt text under **140 characters**
4. Describe the image — do NOT write "image of" (screen reader announces it already)
5. Decorative images (no information value) use `alt=""`
6. Don't repeat caption as alt text
7. For video/motion: describe what happens step by step

---

### Foundations: Content Design — Style Guide (UX Writing)

|Guideline|Rule|
|---|---|
|**Explain consequences**|Tell users what will happen before they act|
|**Use sentence case**|Not title case for UI text|
|**Use abbreviations sparingly**|Only when well-known|
|**Use second person**|Use "you" not "I/my" in interface text|
|**Don't mix first and second person**|Avoid mixing "me"/"my" with "you"/"your"|

---

### Foundations: Interaction — Gestures

|Gesture|Use Case Example|
|---|---|
|**Tap**|Tapping a card in newsfeed opens the full article|
|**Double Tap**|Double tapping a photo opens it to full screen|
|**Long press**|Long pressing a list item selects it|
|**Scroll and pan**|Scrolling through a feed vertically|
|**Swipe**|Swiping a list item reveals additional actions|
|**Drag**|Reordering a list by dragging|
|**Pick up and move**|Moving a calendar event to a new time|
|**Pinch**|Pinching outward a photo to full screen|

---

### Foundations: Interaction — Selection

**Selection Components:**

1. Segmented buttons
2. Chips
3. List items
4. Checkboxes
5. Radio buttons
6. Switch
7. Slider

**Components with Active Indicators:**

- Tab
- Navigation drawer

**Selection by Touch:**

- Long press touch or two-finger touch

---

### Styles: Color Roles

|Role|Description|
|---|---|
|**Surface**|Backgrounds and large, low-emphasis areas|
|**Primary**|High-emphasis fills, texts, icons against surface|
|**On Primary**|Text and icons against primary|
|**Primary Container**|Standout fill color for key components like FAB|
|**On Primary Container**|Text and icons against primary container|
|**Secondary**|Less prominent fills, text, icons against surface|
|**On Secondary**|Text and icons against secondary|
|**Secondary Container**|Less prominent fill for recessive components (e.g., tonal buttons)|
|**On Secondary Container**|Text and icons against secondary container|
|**Container**|Fill color for foreground elements like buttons (not for text/icons)|
|**On**|Color for text/icons on top of paired parent color|
|**Variant**|Lower emphasis alternative to non-variant pair|

---

## 9. Color Theory

**Reference video:** https://youtu.be/GyVMoejbGFg?si=jcHpxaYq-ittvp7_ **Color palette tool:** https://paletton.com

### Color Temperature

#### Cool Colors (สีโทน Cool — เย็น)

- **สี:** น้ำเงิน, ม่วง, เขียว และโทนสีที่ผสมกับสีน้ำเงิน
- **ความรู้สึก:** สงบ, ผ่อนคลาย, เป็นมืออาชีพ, น่าเชื่อถือ
- **เหมาะกับ:** เว็บไซต์องค์กร, แอปพลิเคชันทางการแพทย์, ระบบที่ต้องการความน่าเชื่อถือ

#### Warm Colors (สีโทน Warm — อุ่น)

- **สี:** แดง, ส้ม, เหลือง และโทนสีที่ผสมกับสีแดง
- **ความรู้สึก:** อบอุ่น, มีชีวิตชีวา, เป็นมิตร, สนุกสนาน
- **เหมาะกับ:** เว็บไซต์ร้านอาหาร, แอปพลิเคชันสำหรับเด็ก, ระบบที่ต้องการความเป็นมิตร

### Color Models

- RGB (Red, Green, Blue) — for screens
- CMYK (Cyan, Magenta, Yellow, Black) — for print
- HSB/HSL (Hue, Saturation, Brightness/Lightness)

### Color Categories (from Color Theory)

- Primary colors
- Secondary colors
- Tertiary colors
- Complementary colors
- Analogous colors
- Triadic colors

---

## 10. Database Design — ERD

### Entity Relationship Diagram (ERD) Basics

|Element|Description|
|---|---|
|**Entity**|สิ่งที่ต้องการจัดเก็บข้อมูล|
|**Properties/Attributes**|คุณลักษณะที่ต้องการจัดเก็บ|
|**Relationship**|ความสัมพันธ์ระหว่าง Entity: 1:1, 1:M (M:1), M:N|

---

### Relationship Types

#### 1:M Relationship

- นำ Primary key ฝั่ง 1 ไปใส่ไว้ฝั่ง M
- ทำหน้าที่เป็น **Foreign key**

**Example:**

```
Emp (EmpID, EName, Salary, Email, Education, DeptID)
     ^PK                                       ^FK

Dept (DeptID, DName, Location)
      ^PK
```

#### 1:1 Relationship

- นำ Primary key ฝั่ง 1 ไปใส่ไว้อีกฝั่ง
- ทำหน้าที่เป็น **Foreign key**
- พิจารณาว่าจะใส่ฝั่งใด ขึ้นอยู่กับความถี่การใช้งาน

#### M:N Relationship

- Relationship จะถูกสร้างเป็น Entity ใหม่ (**Composite Entity**)
- เชื่อมโยงความสัมพันธ์จาก 2 Entity เดิม มายัง Entity ใหม่แบบ 1:M
- นำ Primary key ของทั้ง 2 Entity เดิม มารวมกันที่ Entity ใหม่เพื่อกำหนดเป็น Primary key

**Example M:N Decomposition:**

```
Student ←——M:N——→ Course
becomes:
Student ←1:M→ Enrollment ←M:1→ Course
```

---

### ERD Design Example — Invoice System

```
Customer  1——M  Invoice  1——M  Inv_Detail  M——1  Product
```

---

### Workshop — Room Activity Fund System

**Requirements:**

- จัดการข้อมูลสมาชิก (CRUD)
- จัดการข้อมูลกิจกรรม (ชื่อ, สถานที่, วันที่, ไฟล์เอกสาร, ค่าใช้จ่าย)
- สมาชิกจ่ายเงินผ่านการโอน พร้อมส่งหลักฐาน
- เก็บข้อมูลรายจ่าย (ประเภทรายจ่าย, จำนวนเงิน, วันที่, ผู้รับผิดชอบ)
- Admin: เพิ่ม ลบ แก้ไขข้อมูลการเก็บเงินและจ่ายเงิน
- Member: ดูยอดการจ่ายเงินของตนเองและยอดรวมแต่ละกิจกรรม
- ระบบ Login + ตรวจสอบประเภทผู้ใช้งาน
- จัดเก็บ Log ของการแก้ไขและลบข้อมูล

---

## Design System References

|Resource|URL|
|---|---|
|Material Design 3|https://m3.material.io|
|Atlassian Design System|https://atlassian.design|
|Apple Human Interface Guidelines|https://developer.apple.com|
|Figma|https://www.figma.com|
|MockFlow|https://mockflow.com|
|Moqups|https://moqups.com|
|Paletton (Color Palette)|https://paletton.com|

### Figma Free Resources

- Figma Finder — https://www.figmafinder.com/
- Figma Elements — https://figmaelements.com/
- Figma Crush — https://www.figmacrush.com/
- Figma Resources — https://www.figmaresources.com/
- Figmafreebies — https://www.figmafreebies.com/
- Freebiesui — https://freebiesui.com/figma-freebies/

---

## Quick Reference Card

|Topic|Key Points|
|---|---|
|**Use Case Diagram**|Actor + Use Case + System Boundary; Relationships: Association, Include, Extend, Generalization|
|**Class Diagram**|Attributes (+/-/#/~) + Operations; Relationships: Association, Aggregation, Composition, Inheritance|
|**Activity Diagram**|Initial Node●, Final Node⬤, Decision◇, Fork/Join═, Swimlanes|
|**Architecture**|Monolithic < SOA < Microservices; 2-tier < 3-tier < N-tier|
|**Nielsen's Heuristics**|10 rules: Visibility, Real world match, Control, Consistency, Error prevention, Recognition, Flexibility, Aesthetics, Error recovery, Documentation|
|**Material Design**|Material metaphor; Contrast: large text 3:1, small text 4.5:1; Touch target 48dp|
|**ERD**|1:1 (FK on either), 1:M (FK on M side), M:N (create composite entity)|
|**Color**|Cool = professional/calm; Warm = friendly/energetic; Contrast ratio = (L1+0.05)/(L2+0.05)|