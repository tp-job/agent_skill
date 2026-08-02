# Agent Skills

A library of 30 Claude Code skills. Each lives in its own folder, named for the `name:` in its `SKILL.md`, with deep-dive material under `references/` and any executable helpers under `scripts/`.

Conventions and the authoring checklist are in [CLAUDE.md](CLAUDE.md). The machine-readable index is [skill.json](skill.json) — regenerate it with `python scripts/build-index.py` after adding or renaming a skill.

## Frontend & UI

| Skill | What it does |
| --- | --- |
| [frontend-design](frontend-design/SKILL.md) | Guidance for distinctive, intentional visual design when building new UI or reshaping an existing one — aesthetic direction, typography, and choices that don't read as templated defaults. |
| [web-design-guidelines](web-design-guidelines/SKILL.md) | Review UI code for Web Interface Guidelines compliance. Use for 'review my UI', 'check accessibility', 'audit design', 'review UX', or 'check my site against best practices'. Takes a file or glob pattern as argument. |
| [google-design-system](google-design-system/SKILL.md) | Apply Google Design principles across 16 domains: Material 3 Expressive, motion design, Google Sans Flex typography, AI/Gemini visual design, global accessibility, design sprints, UX writing, brand building, design culture, and XR/AI glasses (Glimmer). Use for any task involving Google design standards. |
| [css-architecture](css-architecture/SKILL.md) | Scaffold and manage CSS file architecture for TailwindCSS-first projects. Use to organize CSS files, prevent or fix 'CSS hell', add custom styles alongside Tailwind, set up structural design tokens, configure PostCSS imports, enforce lint rules, or migrate a messy stylesheet. |
| [ui-checker](ui-checker/SKILL.md) | Systematically audit web UIs across four dimensions: theme compliance (CSS variables/design tokens vs. hardcoded values, Tailwind and shadcn .dark setups), layout integrity (dimensions, spacing, overflow, breakpoints), browser rendering via a live clickable inspector artifact, and accessibility polish (WCAG contrast, alt text, focus styles, fixed px fonts, reduced motion). |
| [vercel-react-best-practices](vercel-react-best-practices/SKILL.md) | React and Next.js performance optimization guidelines from Vercel Engineering. Use when writing, reviewing, or refactoring React/Next.js code — components, pages, data fetching, bundle optimization, performance improvements. |
| [threejs-3d](threejs-3d/SKILL.md) | Build high-performance, production-grade Three.js and 3D web experiences. Triggers on Three.js, WebGL/WebGPU, GLTF/GLB/OBJ/FBX/STL, shaders (GLSL/TSL), particles, skeletal animation, HDRI/PBR, instancing, raycasting, camera rigs, postprocessing (bloom, DoF, AA, tone mapping), R3F/Drei, point clouds, terrain, GPU compute. |
| [flutter](flutter/SKILL.md) | Flutter/Dart application engineering — architecture, layout debugging, responsive design, and widget previews. Triggers on 'structure my Flutter project', 'RenderFlex overflowed', 'unbounded height viewport', 'make this responsive', 'add a widget preview', and similar. |

## Backend & Data

| Skill | What it does |
| --- | --- |
| [java-api-performance](java-api-performance/SKILL.md) | Java Spring Boot backend API performance optimization. Use when writing, reviewing, or refactoring Java/Spring Boot code to fix slow APIs, memory issues, or database inefficiencies — loop optimization, caching, pagination, query tuning, N+1 problems, indexing, async processing, connection pooling (HikariCP). |
| [supabase-senior](supabase-senior/SKILL.md) | Senior-level Supabase + Prisma architecture and engineering. Activates on Supabase, Prisma ORM, schema design, RLS, migrations, connection pooling, Supabase Auth, Edge Functions, Realtime, Storage, migration planning (Postgres → Supabase), and query optimization. |
| [data-analyze](data-analyze/SKILL.md) | Answer data questions end-to-end, from a quick metric lookup to multi-dimensional analysis to a formal report. Triggers on any request that requires querying, aggregating, or interpreting data from a warehouse, table, CSV/Excel, or pasted results. |

## Quality, Security & Performance

| Skill | What it does |
| --- | --- |
| [owasp-top-10-2025](owasp-top-10-2025/SKILL.md) | Security review and vulnerability analysis based on the OWASP Top 10 2025. Use when auditing code for security flaws, reviewing authentication, checking for injection, or ensuring cryptographic correctness — broken access control, misconfiguration, vibe-coding risks, memory management, supply chain, resilience failures. |
| [security](security/SKILL.md) | Senior-level security architecture covering OAuth2 authorization flows and leveled API key design. Activates on OAuth2, access tokens, authorization flows, API key management and rotation, key compromise, leveled permissions, resource server security, and agent authentication patterns. |
| [clean-code-javascript](clean-code-javascript/SKILL.md) | Clean Code principles and best practices for JavaScript/TypeScript. Use when writing, reviewing, or refactoring JS/TS to improve readability, maintainability, and correctness — naming, function design, class structure, SOLID, error handling, testing patterns, formatting. |
| [lighthouse](lighthouse/SKILL.md) | Diagnose and fix a website to earn high Lighthouse scores across Performance, Accessibility, Best Practices, SEO, and Agentic Browsing on both desktop and mobile. Triggers on shared Lighthouse/PageSpeed/Core Web Vitals reports or failing metrics (FCP, LCP, TBT, CLS, INP, Speed Index). |
| [ai-web-product-craft](ai-web-product-craft/SKILL.md) | Guidance for web pages and apps that load images/iframes/embeds and/or include an AI feature (chatbot, agent, summarizer, recommender, generative UI). Combines HTML delivery performance (TTFB, caching, compression, CDNs, lazy loading, embed facades) with responsible AI product design (privacy, fairness, calibrated trust, AI UX pattern choice). |
| [debug-master](debug-master/SKILL.md) | Deep debugging and auto-fix across file system inspection, logic and workflow tracing, and algorithm analysis. Triggers on any error message, stack trace, broken path, missing module, wrong output, or vague "something is wrong" report. Covers Python, JS/TS, Go, Bash, SQL, and agent workflows (LangChain/LangGraph, AutoGen, CrewAI). |
| [tracking-and-debugging](tracking-and-debugging/SKILL.md) | Autonomous bug triage, root-cause diagnosis, and issue reporting for PERN/MERN full-stack projects. Outputs a structured issue report and fix guidance without follow-up questions. Thai triggers included (แก้บัค, หา bug, ช้า, memory leak, login ไม่ได้). |

## Process & Delivery

| Skill | What it does |
| --- | --- |
| [long-horizon-engineering-workflow](long-horizon-engineering-workflow/SKILL.md) | A six-stage gated delivery workflow (Requirements → Design → Development → QA → UAT → Deployment) to keep long, multi-session, or multi-stage builds from drifting. Use for any 'build me X' request too big for one shot; not for snippets or small well-specified fixes. |
| [requirement-gathering](requirement-gathering/SKILL.md) | Autonomous requirement extraction and documentation for PERN/MERN full-stack projects with micro design standards. Produces a complete Markdown requirements document without asking follow-up questions. Thai triggers included (วิเคราะห์ code, เขียน spec, ทำ requirements, audit component). |
| [senior-leadership-advisor](senior-leadership-advisor/SKILL.md) | Acts as senior leadership (CTO/VP/Staff-level) across engineering, product, design, quality, architecture, data/AI, and prompt engineering. Auto-detects which discipline(s) a request touches and answers in that voice. Skip for casual conversation or trivial lookups. |
| [deploy-to-vercel](deploy-to-vercel/SKILL.md) | Deploy applications and websites to Vercel. Use for requests like 'deploy my app', 'push this live', 'give me the link', or 'create a preview deployment'. |
| [vercel-cli-with-tokens](vercel-cli-with-tokens/SKILL.md) | Deploy and manage projects on Vercel using token-based authentication rather than interactive login — 'deploy to vercel', 'set up vercel', 'add environment variables to vercel'. |

## Knowledge & Authoring

| Skill | What it does |
| --- | --- |
| [knowledge-base](knowledge-base/SKILL.md) | Software engineering knowledge base covering architecture patterns, component-based design, security fundamentals, software design principles, and use case + microservices design. Use when answering architecture, design pattern, system design, security, or use-case modeling questions. |
| [skill-creator](skill-creator/SKILL.md) | Create new skills, modify and improve existing skills, and measure skill performance. Use to build a skill from scratch, edit or optimize an existing one, run evals, benchmark with variance analysis, or tune a skill description for better triggering accuracy. |
| [agent-skill-creator](agent-skill-creator/SKILL.md) | Guide for creating, structuring, and organising AI agent skills — building a skill from scratch, setting up a .agents/ workspace, designing folder structures, and writing SKILL.md files with proper YAML frontmatter. |
| [cs-course-designer](cs-course-designer/SKILL.md) | Research, plan, and write course/unit outlines, Course Learning Outcomes (CLOs), lesson/teaching plans, and assessments (quizzes, exams, rubrics, project briefs) for general CS, DBMS, SQL, Python, and C. Also reviews existing CLOs, lesson plans, and assessments for alignment. Not for other languages or live 1:1 tutoring. |
| [obsidian-vault](obsidian-vault/SKILL.md) | Turn an Obsidian vault into a persistent, self-organizing knowledge base that Claude Code reads from and writes to across sessions — second brain / PKM setup, ingesting documents, URLs and transcripts into linked notes, querying past notes, and running project wikis. |
| [view-pdf](view-pdf/SKILL.md) | Interactive PDF viewer. Use when the user wants to open, show, or view a PDF and collaborate on it visually — annotate, highlight, stamp, fill form fields, place signature/initials, review markup. Not for summarization or text extraction. |

## Other

| Skill | What it does |
| --- | --- |
| [project-file-structure](project-file-structure/SKILL.md) | Rules for naming and placing every file and folder in a React + TypeScript + Node + Prisma project whose documentation lives in an Obsidian vault, plus PDF handling. |
