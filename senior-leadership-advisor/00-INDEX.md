---
tags: [index, MOC, senior-leadership]
aliases: [Home, Index, Role Map]
---

# 🗺️ Senior Leadership Advisor — Knowledge Graph Index

This is the **Map of Content (MOC)** for the Senior Leadership Advisor skill vault.  
Open in Obsidian → Graph View to see all role relationships as a network.

---

## 📚 Skill Files

- [[agent-skill/senior-leadership-advisor/SKILL]] — Main agent instructions (role detection, thinking process, answer style)
- [[references/roles]] — Full role catalog (~35 roles)
- [[references/thinking-framework]] — 7-point thinking discipline detail

---

## 🗂️ Role Tracks (สาย)

### 1. สาย Software & Logic
→ [[roles/01-Software-Logic]]
- [[roles/01-Software-Logic#Backend Developer|Backend Developer]]
- [[roles/01-Software-Logic#Frontend Developer|Frontend Developer]]
- [[roles/01-Software-Logic#Logic Algorithm Engineer|Logic / Algorithm Engineer]]
- [[roles/01-Software-Logic#Embedded Firmware Engineer|Embedded / Firmware Engineer]]
- [[roles/01-Software-Logic#QA Automation Tester|QA / Automation Tester]]

### 2. สาย IoT (Internet of Things)
→ [[roles/02-IoT]]
- [[roles/02-IoT#IoT Architect|IoT Architect]]
- [[roles/02-IoT#IoT Developer|IoT Developer]]
- [[roles/02-IoT#Cloud Network Engineer|Cloud / Network Engineer]]

### 3. สาย UX/UI & Design
→ [[roles/03-UX-UI-Design]]
- [[roles/03-UX-UI-Design#UX Researcher|UX Researcher]]
- [[roles/03-UX-UI-Design#UI Designer|UI Designer]]
- [[roles/03-UX-UI-Design#Interaction Designer|Interaction Designer]]
- [[roles/03-UX-UI-Design#Product Designer|Product Designer]]

### 4. สาย Writing & Content
→ [[roles/04-Writing-Content]]
- [[roles/04-Writing-Content#UX Writer|UX Writer]]
- [[roles/04-Writing-Content#Technical Writer|Technical Writer]]
- [[roles/04-Writing-Content#Tech Content Strategist|Tech Content Strategist]]

### 5. สายบริหารจัดการและประสานงาน (Management)
→ [[roles/05-Management]]
- [[roles/05-Management#Product Manager Owner|Product Manager / Owner]]
- [[roles/05-Management#Solutions Architect|Solutions Architect]]

### 6. Engineering & Leadership (Original Roles)
→ [[roles/06-Engineering-Leadership]]
- Software Architecture, Frontend/Backend Engineering, QA, Security, DevOps, SRE, Cloud, Data, AI/ML, Prompt Engineering, Executive Leadership, Product Management

---

## 🔗 Cross-Track Relationships (Graph Edges)

| From | To | Relationship |
|---|---|---|
| [[roles/02-IoT]] | [[roles/01-Software-Logic]] | IoT dev needs Backend + Embedded |
| [[roles/02-IoT]] | [[roles/06-Engineering-Leadership]] | IoT Architect ↔ Cloud/SRE |
| [[roles/03-UX-UI-Design]] | [[roles/04-Writing-Content]] | Design + copy always paired |
| [[roles/03-UX-UI-Design]] | [[roles/01-Software-Logic]] | UI Designer ↔ Frontend Dev |
| [[roles/05-Management]] | [[roles/06-Engineering-Leadership]] | PM ↔ Engineering leadership |
| [[roles/05-Management]] | [[roles/02-IoT]] | Solutions Architect spans IoT+Software |
| [[roles/04-Writing-Content]] | [[roles/03-UX-UI-Design]] | UX Writer ↔ UX Researcher |

---

## 🧠 Thinking Framework
→ [[references/thinking-framework]]

| Concept | Apply When |
|---|---|
| Think Thoroughly | Always, before any answer |
| Pre-Mortem | Architecture, irreversible decisions |
| Edge-Case Analysis | API design, firmware, agent prompts |
| First-Principles | Build-vs-buy, tech stack choices |
| Holistic View | Cross-track integration requests |