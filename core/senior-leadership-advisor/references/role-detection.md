# Role detection — signal tables

Match the request's signals to a role. Pick one or two best fits; for roles not listed or org-wide questions, see [roles](roles.md).

## Contents

- สาย Software & Logic
- สาย IoT (Internet of Things)
- สาย UX/UI & Design
- สาย Writing & Content
- สายบริหารจัดการและประสานงาน
- สาย R&D — Silicon Research & Development
- สาย TEST — Silicon Verification & QA
- สาย SELL — Silicon Sales, Marketing & Business
- สาย Client Service — Silicon Support & Technical Services
- Senior Leadership (cross-functional blends)

### สาย Software & Logic

| Signal in the request | Role |
|---|---|
| API/server code, DB schema, auth, microservices, backend perf | Backend Developer |
| React/Vue/CSS, component state, web perf, accessibility bugs | Frontend Developer |
| Algorithm design, formula optimization, sorting/search logic, complex calculation | Logic / Algorithm Engineer |
| Firmware, microcontroller, RTOS, chip-level code, embedded C/C++ | Embedded / Firmware Engineer |
| Test scripts, automation framework, bug triage, QA logic verification | QA / Automation Tester |

### สาย IoT (Internet of Things)

| Signal in the request | Role |
|---|---|
| IoT system design, device topology, protocol choice (MQTT/CoAP/AMQP) | IoT Architect |
| Sensor data pipeline, device-to-cloud flow, edge processing | IoT Developer |
| Network config, cloud infra for IoT, bandwidth/latency/connectivity | Cloud / Network Engineer |

### สาย UX/UI & Design

| Signal in the request | Role |
|---|---|
| User research, interviews, usability test, insight synthesis | UX Researcher |
| Screen layouts, color, typography, visual components | UI Designer |
| Micro-interactions, HMI, human-machine interface, gesture/animation | Interaction Designer |
| End-to-end product look+feel, design system, business-user balance | Product Designer |

### สาย Writing & Content

| Signal in the request | Role |
|---|---|
| In-app copy, button labels, error messages, onboarding text, microcopy | UX Writer |
| API docs, user manuals, system documentation, developer guides | Technical Writer |
| Explaining tech to non-technical audiences, content plan, explainer articles | Tech Content Strategist |

### สายบริหารจัดการและประสานงาน

| Signal in the request | Role |
|---|---|
| Product roadmap, feature prioritization, sprint planning, "should we build X" | Product Manager / Owner |
| Tech stack selection for client, Software+IoT integration proposal | Solutions Architect |

### สาย R&D — Silicon Research & Development

| Signal in the request | Role |
|---|---|
| Chip architecture, microarchitecture, ISA, cache/memory hierarchy, PPA tradeoff | Silicon Architect / Microarchitect |
| Verilog/SystemVerilog/VHDL, RTL, timing closure, CDC, synthesis, DFT insertion | ASIC / RTL Design Engineer |
| Model architecture research, training at scale, quantization, benchmark methodology | AI / Deep Learning Research Scientist |
| LLVM/MLIR, kernels, drivers/runtime, CUDA/ROCm, achieved-vs-peak FLOPS | Software / Compiler Engineer |

### สาย TEST — Silicon Verification & QA

| Signal in the request | Role |
|---|---|
| UVM testbench, constrained-random, coverage closure, formal, pre-silicon signoff | Design Verification (DV) Engineer |
| Lab bring-up, shmoo, thermal/VT characterization, silicon debug on real parts | Silicon Validation Engineer |
| ATE test program, wafer sort, binning/speed grades, yield analysis, DPPM | Post-Silicon Test Engineer |
| Qualification, AEC-Q100/ISO 9001, failure analysis, RCCA, RMA trends, release gate | Quality Assurance (QA) Engineer |

### สาย SELL — Silicon Sales, Marketing & Business

| Signal in the request | Role |
|---|---|
| Competitive benchmarking, performance claims, reviewer guides, launch content | Technical Marketing Engineer |
| SKU/bin strategy, silicon pricing and margin, tapeout-gated roadmap, EOL/supply | Silicon Product Manager |
| Design-win pursuit, enterprise/hyperscaler deal, supply agreement, allocation | Strategic Account Manager / Enterprise Sales |
| Partnerships, ecosystem/ODM/ISV enablement, new market entry, licensing | Business Development Manager |

### สาย Client Service — Silicon Support & Technical Services

| Signal in the request | Role |
|---|---|
| Customer design-in, schematic/layout review, on-site bring-up and debug | Field Application Engineer (FAE) |
| Rack/cluster sizing, reference architecture, TCO model, deployment tuning | Solutions Architect / Systems Engineer |
| Support case triage, reproduction, escalation packaging, RMA intake, KB | Customer Support Engineer |
| Long-term account technical health, escalation ownership, NDA roadmap briefing | Technical Account Manager (TAM) |

**Disambiguation:** "Product Manager" and "Solutions Architect" exist in both the software tracks and the silicon tracks. Route to the silicon versions when the constraint is hardware — tapeout schedules, bin yields, foundry capacity, rack power. Route to [05-Management](../roles/05-Management.md) when the constraint is sprint velocity and a software release train.

### Senior Leadership (cross-functional blends)

| Signal in the request | Role blend |
|---|---|
| "How should we architect/scale this," tech stack choice, system design | Software Architecture |
| Org strategy, build-vs-buy, multi-quarter direction, headcount/budget | Executive Leadership |
| Spans 2+ tracks with no single clear owner | Blend the relevant roles (see Step 3) |
| Prompts, system prompts, agent design, context/LLM workflow | Prompt Engineering |
| Test strategy, release sign-off, quality process | QA Leadership |
