# 🎬 TariqTube 2.0: Master Architectural Blueprint (v4.1)

## 📋 1. Core Architectural Principle: Multilingual Content Factory
TariqTube 2.0 is an enterprise-grade, **Project-Centric** and **Multilingual** content factory. 
- **The Project is the Source of Truth**: All logic, character persistence, and narrative memory live at the Project level.
- **Visual-First Production**: One "Master Visual Episode" is rendered for all languages to ensure cost efficiency.
- **Linguistic Branching**: Localized narration, SEO, and metadata are generated as sub-units of the Visual Master.
- **Platform Agnostic**: Publishing logic is decoupled from production, enabling eventual deployment to YouTube, TikTok, Instagram, and more without core restructuring.

---

## 🏗️ 2. Detailed Data Model: System Entities

### A. Organizational Layer
| Entity | Description | Ownership |
| :--- | :--- | :--- |
| **Workspace** | Top-level container for organizational boundaries. | Base |
| **Project** | **Master Entity.** Owns the Asset Registry, Visual Style, and target Audience. | Belongs to Workspace |

### B. Production & Localization Layer
| Entity | Description | Ownership |
| :--- | :--- | :--- |
| **Series** | Grouping for episodic content with sequential logic. | Belongs to Project |
| **Episode** | **The Visual Anchor.** One story, one master video render. Shared ID across languages. | Belongs to Series |
| **LanguageVariant**| **The Linguistic Anchor.** Localized version of an Episode. Owns audio and SEO. | Belongs to Episode |
| **Asset** | Persistent entities (Characters, Environments) with cross-language specs. | Belongs to Project |

### C. Distribution Layer
| Entity | Description | Ownership |
| :--- | :--- | :--- |
| **Content Unit** | Specific media file (Full, Teaser, Short) derived from a Variant. | Belongs to Variant |
| **Channel** | Specific social account (e.g., @TariqTubeAr-YT). Tracked per platform. | Base Map |
| **Publishing Route** | Mapping logic (SEO templates, regional schedules). | Workflow Config |
| **Post/Video Result** | The output of a publish (External ID, URL, Analytics Link). | Belongs to Variant |

---

## 🔐 3. LanguageVariant Implementation Detail
A **LanguageVariant** represents a final localized product. It is an implementation-grade entity that MUST track:
- **ID**: `{episode_id}_{language_code}` (e.g., `ep101_ar`)
- **Language Code**: `ar`, `en`, `es`, etc.
- **Production Spec**: 
    - `translated_script`: The localized screenplay.
    - `vocal_assignment`: Character -> TTS Voice Mapping (Locale-specific).
- **SEO & Metadata**:
    - `localized_title`, `localized_description`, `localized_hashtags`.
    - `localized_subtitles`: (e.g., SRT/VTT paths).
- **Media Assets**:
    - `localized_audio_path`: GCS path to the narration track.
    - `final_render_path`: GCS path to the multiplexed localized video.
- **Status & Results**:
    - `variant_status`: (Generating-Audio, Multiplexing, Ready-to-Publish).
    - `publishing_results`: Array of `{platform_id, external_video_id, url}`.

---

## 🎨 4. Character & Voice Localization Matrix
Character assets are defined by a **Vocal Matrix** to maintain identity across tongues:
- **Character Asset**: `Sparky_the_Robot`
    - `ar`: `ar-XA-Studio-B` (Voice Signature 1)
    - `en`: `en-US-Studio-O` (Voice Signature 2)
    - `es`: `es-ES-Studio-F` (Voice Signature 3)
- **Visual Persistence**: Sparky's "Visual Seed" (Imagen Prompt) remains constant regardless of the language variant being produced.

---

## 🚀 5. Platform-Agnostic Publishing Router
The system is built for **Multi-Platform expansion**:
- **Router Logic**: Accepts a `Content Unit`, identifies its `Target Platforms` (YT, TT, IG), and executes the platform-specific API driver.
- **Content Adaptation**: The router automatically selects the correct aspect ratio (16:9 for YouTube, 9:16 for Shorts/TikTok) based on the `Publishing Route`.
- **Targeting**: One Project can route its English variants to a global YouTube channel and its Arabic variants to a regional Instagram account simultaneously.

---

## 🕒 6. Scheduling & Cadence Logic
- **Synchronized Numbering**: All language variants for `Episode 50` are produced in parallel to ensure global release parity.
- **Release Cadence**: Defined at the **Series** level (e.g., "Mondays and Thursdays").
- **Timezone Offsets**: The **Schedule Manager** adjusts posting times for each variant to hit peak local hours (e.g., 6 PM in Cairo vs 6 PM in London).

---

## 💾 7. System Infrastructure Proposal

### Firestore Schema (v4.1)
- `projects/{pj_id}/`
    - `registry/`: (sub-collection) {type, visual_seed, voices: {ar: id, en: id}}
- `series/{sr_id}/`
    - `episodes/{ep_id}/`
        - `metadata`: {order, visual_status, master_video_path}
        - `variants/`: (sub-collection)
            - `ar`: {status, script, audio, render_path, yt_id, tt_id, ig_id}
            - `en`: {status, script, audio, render_path, yt_id, tt_id, ig_id}
- `publishing/queue/`: {timestamp, variant_path, platform}

### Cloud Storage (GCS) Hierarchy
- `tariqtube-production/`
    - `projects/{pj_id}/assets/` (Master Character Ref Sheets)
    - `episodes/{ep_id}/`
        - `visual_master.mp4` (High-bitrate, no narration)
        - `renders/`
            - `ar/` (full_ar.mp4, teaser_ar.mp4, short_ar.mp4)
            - `en/` (full_en.mp4, teaser_en.mp4, short_en.mp4)
        - `audio/` (Local narration tracks)

---
*Blueprint Version: 4.1 (Enterprise Content Factory)*
*Author: TariqTube Architecture Team*
