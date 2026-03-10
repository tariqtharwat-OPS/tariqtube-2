# 🎬 TariqTube 2.0: The AI Content Factory (Master Spec v3.0)

## 📋 Overview
TariqTube 2.0 is an enterprise-grade, serverless AI video production suite powered by **Google Cloud Platform**. It is designed for high-scale, consistent content creation with deep episodic logic and automated multi-platform distribution.

## 🏗️ Architectural Core
TariqTube 2.0 is built on five structural pillars that distinguish it from legacy automation:

1.  **Project-Centric**: The system logic is anchored in the **Project**, not the social account. Production state, styles, and memory are decoupled from publishing targets.
2.  **Series-Capable**: Native support for episodic storytelling, including seasons, episode ordering, release cadence, and episodic pointer tracking.
3.  **Multi-Channel Capable**: Content Units (Episodes, Teasers, Shorts) are dynamically routed to multiple platforms (YouTube, TikTok, Instagram) via a decoupled Publishing Router.
4.  **Asset-Persistent**: Core production assets (Characters, Environments, Voices) are stored in a persistent Registry to eliminate visual and narrative drift across hundreds of episodes.
5.  **Episode-Aware**: Every episode is a structured production unit with a complete state lifecycle (Story, Production, and Publishing statuses).

## 🚀 Key Modules
- **Project Manager**: Master state and style governance.
- **Series Manager**: Continuity and sequence logic.
- **Asset Manager**: Persistent visual and vocal registries.
- **Production Engine**: Vertex AI orchestration (Gemini 1.5 Pro, Imagen 3, Studio TTS).
- **Publishing Router**: Headless API distribution and scheduling.

---
*Clean Source of Truth for TariqTube 2.0 Rebuild*
