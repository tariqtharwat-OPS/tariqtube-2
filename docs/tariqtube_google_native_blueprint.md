# 🎬 TariqTube 2.0: Google-Native Blueprint (Master Control Document)

## 📋 1. Core Architectural Principle: Project-Centric Autonomy & Localization
TariqTube 2.0 is a **Project-Centric** and **Multilingual** system. 
- **The Project is the Source of Truth.**
- **Episodes are synchronized production units across languages.**
- **The Master Video is generated once; Variants swap narration and metadata.**

---

## 🏗️ 2. App Logic & Data Model: System Entities

The following entities define the hierarchical structure of the system:

| Entity | Description | Ownership |
| :--- | :--- | :--- |
| **Workspace** | High-level organizational boundary. | Base Layer |
| **Project** | **Master Entity.** Defines style and asset registry. | Belongs to Workspace |
| **Series** | Grouping for episodic content with sequential ordering. | Belongs to Project |
| **Episode** | **The Production Anchor.** One story beat, one visual master. | Belongs to Series |
| **LanguageVariant**| **The Linguistic Anchor.** Reuses master video with localized audio. | Belongs to Episode |
| **Character** | Persistent visual/vocal identity (Visual Seed + Multi-Lang Voice Map). | Belongs to Project |
| **Environment** | Persistent visual stage (Stage Seed). | Belongs to Project |
| **Voice Profile** | Defined TTS configuration per character/language. | Belongs to Project |
| **Content Unit** | Media deliverable (Full, Teaser, Short) per Language Variant. | Belongs to Variant |
| **Channel** | A publishing destination (Specific to a language/region). | Platform Map |
| **Publishing Route** | Mapping logic between a Variant's Content Unit and a Channel. | Workflow Config |
| **Schedule Item** | A queued release task for a specific Language Variant. | Belongs to Router |

---

## 🔐 3. Ownership & Master Logic
1.  **Source of Truth**: The `Project` record holds the master asset registry.
2.  **Multilingual Synchronization**: `Episode` (Visual Master) → `LanguageVariant` (Audio/SEO).
    - Episode numbering (`order`) is identical across all variants to maintain multi-channel continuity.
3.  **Asset Persistence**: Voices are mapped at the `Project` level as a **Character -> Language -> Voice** matrix.
4.  **Channel Decoupling**: Language Variants are routed to specific language-tracked channels (e.g., "TariqTube Arabic" vs "TariqTube English").

---

## 🌍 4. The Localization Layer (The "One-Video-Many-Voices" Goal)
To ensure cost efficiency and production speed, the system implements a strict Localization Layer:

1.  **Master Production**:
    - The **Production Engine** renders the "Master Video" (Muted or BGM-only) and stores it in GCS.
    - Status is tracked at the **Episode** level.
2.  **Variant Generation**:
    - For each enabled locale, the engine generates **Language-Specific Narration** using the Character's language-mapped Voice Profile.
    - FFmpeg overlays the localized audio onto the Master Video to create the **Final Render** for that variant.
3.  **SEO Localization**:
    - Gemini generates localized Titles, Descriptions, and Hashtags for each variant.
4.  **Independent Routing**:
    - The **Publishing Router** pushes the `ar-variant` to the Arabic channel and the `en-variant` to the English channel simultaneously or on offset schedules.

---

## 📦 5. Content Unit Relationships
A production trigger on an **Episode** entity generates multiple **Language Variants**, each spawning localized **Content Units**:
- **Parent**: `Episode_001` (Visual Master)
    - → **Language Variant**: `AR (Arabic)`
        - → **Unit**: `Full MP4 (AR)`, `Teaser (AR)`, `Short (AR)`
    - → **Language Variant**: `EN (English)`
        - → **Unit**: `Full MP4 (EN)`, `Teaser (EN)`, `Short (EN)`

---

## 🚦 6. Episode & Variant Tracking
- **Episode Status**: Tracks rendering of the Visual Master.
- **Variant Status**: Tracks Narration Gen, Final Overlay Rendering, and Publishing.

---

## 🕒 7. Scheduling & Cadence Logic
The **Schedule Manager** supports synchronized releases:
- **Global Drop**: All language variants publish at the same UTC time.
- **Regional Drop**: Variants publish at peak hours for their respective target markets (Timezone-offset).

---

## 💾 8. Data Schema Proposals

### Firestore Schema (v4.0)
- `projects/{id}/assets/` (sub-collection)
    - `{asset_id}`: {type, spec, voice_map: { "ar": "VoiceID_1", "en": "VoiceID_2" }}
- `series/{id}/episodes/` (sub-collection)
    - `{episode_id}`: {order, visual_master_path, visual_status}
    - `variants/`: (sub-collection)
        - `{locale_id}`: {status, audio_path, final_render_path, video_id, seo_metadata}
- `publishing/schedule/`: {timestamp, variant_id, content_type, channel_id}

### Cloud Storage (GCS) Layout
- `tariqtube-production/`
    - `projects/{pj_id}/series/{sr_id}/episodes/{ep_id}/`
        - `master/` (Visual Master .mp4 - No Narration)
        - `locales/`
            - `ar/` (Arabic Audio .mp3 + Raw Metadata)
            - `en/` (English Audio .mp3 + Raw Metadata)
        - `locales_final/`
            - `ar/` (Full .mp4, Teaser .mp4, Short .mp4)
            - `en/` (Full .mp4, Teaser .mp4, Short .mp4)

---
*Blueprint Version: 4.0 (Multilingual Implementation Specification)*
*Author: TariqTube Architecture Team*
