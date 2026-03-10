# 🎬 TariqTube 2.0: Execution Roadmap (v4.1)

## Phase 1: Project-Centric & Multilingual Foundation
*   [ ] Initialize Firestore Master Schema (v4.1): Workspaces, Projects, Series, Episodes, Assets.
*   [ ] Implement **Asset Manager** (v1): Persistent registry for Characters and Environments.
*   [ ] Implement **Multilingual Vocal Matrix**: Character -> Language -> Voice mapping.
*   [ ] Local testing of Project -> Series -> Episode synchronization logic.

## Phase 2: Production Hardening (Visual Master)
*   [x] Verify Gemini 1.5 Pro for multi-scene visual scripting (Prototype).
*   [x] Verify Imagen 3 for style-consistent frame generation (Prototype).
*   [ ] Implement **Visual Master Render Worker** (Cloud Run): Assemblies a narration-free video unit.
*   **Milestone**: One visual master generated and stored in `/master/` GCS path.

## Phase 3: The Localization Layer (Variant Generation)
*   [ ] Implement **Localization Pipeline**: Translate script → Generate Local Narration → FFmpeg Audio Overlay.
*   [ ] Implement **SEO Localizer**: Variant-specific Titles, Descriptions, and Hashtags.
*   [ ] Batch render logic for multiple Language Variants (ar, en, etc.).
*   **Milestone**: A single visual episode branching into 2+ localized MP4s.

## Phase 4: Platform-Agnostic Publishing Router
*   [x] Verify YouTube Data API v3 for headless publishing (Prototype).
*   [ ] Implement **Publishing Router**: Logic to map Variants to Platform Adapters (YT, TT, IG).
*   [ ] Implement **Schedule Manager**: Timezone-aware localized posting windows.
*   **Milestone**: Synchronized global drop on YouTube and TikTok.

## Phase 5: Managed Asset Evolution & QA
*   [ ] Implement Multimodal Drift Checks: Automated visual audits of generated frames.
*   [ ] Asset Versioning Logic: Support for "Aged Up" characters or new outfits.
*   [ ] Performance Feedback Loop: Analytics polling to inform future AI scripting.

---
*Status: Architecture Locked (v4.1) | Awaiting Phase 1 Schema Initialization*
*Video Prototype Verified*: [https://www.youtube.com/watch?v=bikYlOQhCQg](https://www.youtube.com/watch?v=bikYlOQhCQg)
