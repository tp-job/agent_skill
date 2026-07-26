---
tags: [index, MOC, senior-leadership]
aliases: [Home, Index, Role Map]
---

# 🗺️ Senior Leadership Advisor — Knowledge Graph Index

This is the **Map of Content (MOC)** for the Senior Leadership Advisor skill vault.
Open in Obsidian → Graph View to see all role relationships as a network.

---

## 📚 Skill Files

- [SKILL](./SKILL.md) — Main agent instructions (role detection, thinking process, answer style)
- [roles](references/roles.md) — Full role catalog (~35 roles)
- [thinking-framework](references/thinking-framework.md) — 7-point thinking discipline detail

---

## 🗂️ Role Tracks (สาย)

### 1. สาย Software & Logic
→ [01-Software-Logic](roles/01-Software-Logic.md)
- [Backend Developer](roles/01-Software-Logic.md#backend-developer)
- [Frontend Developer](roles/01-Software-Logic.md#frontend-developer)
- [Logic / Algorithm Engineer](roles/01-Software-Logic.md#logic-algorithm-engineer)
- [Embedded / Firmware Engineer](roles/01-Software-Logic.md#embedded-firmware-engineer)
- [QA / Automation Tester](roles/01-Software-Logic.md#qa-automation-tester)

### 2. สาย IoT (Internet of Things)
→ [02-IoT](roles/02-IoT.md)
- [IoT Architect](roles/02-IoT.md#iot-architect)
- [IoT Developer](roles/02-IoT.md#iot-developer)
- [Cloud / Network Engineer](roles/02-IoT.md#cloud-network-engineer)

### 3. สาย UX/UI & Design
→ [03-UX-UI-Design](roles/03-UX-UI-Design.md)
- [UX Researcher](roles/03-UX-UI-Design.md#ux-researcher)
- [UI Designer](roles/03-UX-UI-Design.md#ui-designer)
- [Interaction Designer](roles/03-UX-UI-Design.md#interaction-designer)
- [Product Designer](roles/03-UX-UI-Design.md#product-designer)

### 4. สาย Writing & Content
→ [04-Writing-Content](roles/04-Writing-Content.md)
- [UX Writer](roles/04-Writing-Content.md#ux-writer)
- [Technical Writer](roles/04-Writing-Content.md#technical-writer)
- [Tech Content Strategist](roles/04-Writing-Content.md#tech-content-strategist)

### 5. สายบริหารจัดการและประสานงาน (Management)
→ [05-Management](roles/05-Management.md)
- [Product Manager / Owner](roles/05-Management.md#product-manager-owner)
- [Solutions Architect](roles/05-Management.md#solutions-architect)

### 6. Engineering & Leadership (Original Roles)
→ [06-Engineering-Leadership](roles/06-Engineering-Leadership.md)
- Software Architecture, Frontend/Backend Engineering, QA, Security, DevOps, SRE, Cloud, Data, AI/ML, Prompt Engineering, Executive Leadership, Product Management

---

## 🔗 Cross-Track Relationships (Graph Edges)

| From | To | Relationship |
|---|---|---|
| [02-IoT](roles/02-IoT.md) | [01-Software-Logic](roles/01-Software-Logic.md) | IoT dev needs Backend + Embedded |
| [02-IoT](roles/02-IoT.md) | [06-Engineering-Leadership](roles/06-Engineering-Leadership.md) | IoT Architect ↔ Cloud/SRE |
| [03-UX-UI-Design](roles/03-UX-UI-Design.md) | [04-Writing-Content](roles/04-Writing-Content.md) | Design + copy always paired |
| [03-UX-UI-Design](roles/03-UX-UI-Design.md) | [01-Software-Logic](roles/01-Software-Logic.md) | UI Designer ↔ Frontend Dev |
| [05-Management](roles/05-Management.md) | [06-Engineering-Leadership](roles/06-Engineering-Leadership.md) | PM ↔ Engineering leadership |
| [05-Management](roles/05-Management.md) | [02-IoT](roles/02-IoT.md) | Solutions Architect spans IoT+Software |
| [04-Writing-Content](roles/04-Writing-Content.md) | [03-UX-UI-Design](roles/03-UX-UI-Design.md) | UX Writer ↔ UX Researcher |

---

## 🧠 Thinking Framework
→ [thinking-framework](references/thinking-framework.md)

| Concept | Apply When |
|---|---|
| Think Thoroughly | Always, before any answer |
| Pre-Mortem | Architecture, irreversible decisions |
| Edge-Case Analysis | API design, firmware, agent prompts |
| First-Principles | Build-vs-buy, tech stack choices |
| Holistic View | Cross-track integration requests |