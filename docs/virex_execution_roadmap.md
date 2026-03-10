# 🎬 TariqTube 2.0: Execution Roadmap (v4.1)

## Phase 1: Project-Centric & Multilingual Foundation
*   [ ] Initialize Firestore Master Schema (v4.1): Workspaces, Projects, Series, Episodes, Assets.
*   [ ] Implement **Asset Manager** (v1): Persistent registry for Characters and Environments.
*   [ ] Implement **Multilingual Vocal Matrix**: Character -> Language -> Voice mapping.
*   [ ] Build the **Project State Monitor** to track imported vs generated vs published states across languages.
*   **Milestone**: Project structure enabled for multi-language production synchronization.

## Phase 2: Production Hardening (Visual Master Rendering)
*   [x] Verify Gemini 1.5 Pro for multi-scene visual scripting (Prototype).
*   [x] Verify Imagen 3 for style-consistent frame generation (Prototype).
*   [ ] Implement **Visual Master Render Worker** (Cloud Run): Assemblies a high-quality narration-free video unit using FFmpeg/MoviePy.
*   **Milestone**: One visual master generated and stored in a shared GCS path.

## Phase 3: The Localization Layer (Variant Generation)
*   [ ] Implement **Localization Pipeline**: Automated script translation → Local Audio Gen → FFmpeg Audio Overlay.
*   [ ] Implement **SEO Localizer**: Locale-specific Titles, Descriptions, and Hashtags per Variant.
*   [ ] Batch render logic to produce multiple Language Variant MP4s (ar/en/es) from one Visual Master.
*   **Milestone**: 2+ localized localized MP4s ready for multi-channel distribution.

## Phase 4: Platform-Agnostic Publishing Router
*   [x] Verify YouTube Data API v3 for headless publishing (Prototype).
*   [ ] Implement **Publishing Router Core**: Logic to identify and route Content Units to their respective Platform Adapters.
*   [ ] Implement **Schedule Manager**: Timezone-aware regional posting windows.
*   [ ] (Optional) Add TikTok/Instagram Platform Adapters.
*   **Milestone**: Synchronized global drop on YouTube-Arabic and YouTube-English channels.

## Phase 5: Managed Asset Evolution & QA
*   [ ] Implement **Multimodal Drift Checks**: Automated visual audits using Gemini 1.5 Vision to flag character/style drift.
*   [ ] **Asset Versioning Logic**: Support for visual updates (e.g., "Season 2 outfits") without breaking archive episodes.
*   [ ] Performance Feedback Loop: Analytics polling to inform future AI scripting and prompt tuning.

---
*Status: Architecture Locked (v4.1) | Awaiting Phase 1 Schema Initialization*
*Proof of Prototype (V1 to V2 transition)*: [Watch Verified Video Result](https://www.youtube.com/watch?v=bikYlOQhCQg)
