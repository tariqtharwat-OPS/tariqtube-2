# 🎬 TariqTube 2.0: The AI Content Factory

## 📋 Overview
TariqTube 2.0 is a serverless, event-driven AI video production suite powered by **Google Cloud Platform**. It automates the creation of children's stories from script to multi-platform distribution using state-of-the-art Generative AI.

## 🏗️ Project-Centric Architecture
TariqTube 2.0 operates on the principle that **Projects are the Source of Truth**. Unlike legacy systems that are bound to specific accounts, TariqTube 2.0 decouples production logic from distribution channels. This allows for:
- Persistent character and world consistency across series.
- Routing the same content to multiple channels (YouTube, TikTok, Instagram).
- Scaleable production independent of publishing status.

## 🚀 Key Features
- **Project Master State**: Centralized production logic in Firestore.
- **Persistent Assets**: character, Environment, and Voice profiles linked to Projects.
- **Multi-Type Content**: Automated generation of Episodes, Teasers, and Shorts from a single production unit.
- **Headless Publishing**: Direct API distribution via a dedicated Publishing Router.
- **Intelligent Scripting**: Gemini 1.5 Pro with long-term episodic memory.

## 📂 Project Structure
- `/pipeline`: Core production logic (V1 & V2 prototypes).
- `/agents`: AI orchestration (Gemini & Imagen integrations).
- `/media_generation`: Media asset creation scripts.
- `/video_assembly`: FFmpeg/MoviePy assembly workers.
- `/publishing`: Automated posting scripts (YouTube API).
- `/docs`: Architecture blueprints, roadmap, and Asset/Series frameworks.

---
*Clean Source of Truth for TariqTube 2.0 Rebuild*
