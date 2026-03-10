# 🎬 TariqTube 2.0: Google-Native Blueprint (Master Control Document)

## 📋 1. Core Architectural Principle: Project-Centric Autonomy
TariqTube 2.0 is a **Project-Centric** system. 
- **The Project is the Source of Truth.**
- **Channels are secondary publishing targets.**
- **Episodes are structured production units.**

Production logic, character persistence, and episodic memory are decoupled from specific social media accounts, allowing one Project to exist across multiple platforms or move between channels without state loss.

---

## 🏗️ 2. App Logic & Data Model: System Entities

The following entities define the hierarchical structure of the system:

| Entity | Description | Ownership |
| :--- | :--- | :--- |
| **Workspace** | High-level organizational boundary (e.g., "Tariq Production Hub"). | Base Layer |
| **Project** | **Master Entity.** Defines style, audience, and production mode (Series vs Factory). | Belongs to Workspace |
| **Series** | Grouping for episodic content with sequential ordering and pointer logic. | Belongs to Project |
| **Episode** | A single production cycle representing one story beat or installment. | Belongs to Series |
| **Character** | Persistent visual/vocal identity (Visual Seed + Vocal ID). | Belongs to Project |
| **Environment** | Persistent visual stage (Stage Seed). | Belongs to Project |
| **Voice Profile** | Defined TTS configuration (ID, Speed, Pitch, Style). | Belongs to Project |
| **Content Unit** | Media deliverable derived from an Episode (Full, Teaser, Short). | Belongs to Episode |
| **Channel** | A publishing destination (YouTube, TikTok, Instagram). | Platform Map |
| **Publishing Route** | Mapping logic (SEO, Schedule) between Content Unit and Channel. | Workflow Config |
| **Schedule Item** | A queued release task with a specific timestamp. | Belongs to Router |
| **Performance Record**| Analytics poll result for a published Content Unit. | Belongs to Project |

---

## 🔐 3. Ownership & Master Logic
To prevent restructuring risk, the following ownership rules are hard-coded into the logic:
1.  **Source of Truth**: The `Project` record holds all configuration for visual and narrative styles.
2.  **Episodic Hierarchy**: `Series` → `Episode`. A Series cannot exist without a Project; an Episode cannot exist without a Series.
3.  **Asset Persistence**: Characters, Environments, and Voice Profiles are stored at the `Project` level (`Asset Registry`). This allows them to be reused across different internal Series within the same Project. Assets can be optionally "Scoped" to a specific Series to prevent crossover contamination.
4.  **Channel Separation**: A `Channel` record only stores OAuth/Platform data. It has no knowledge of the production state until a `Publishing Route` is activated.

---

## 📦 4. Content Unit Relationships
A production trigger on an **Episode** entity generates a cluster of **Content Units**:
- **Parent**: `Episode_001`
    - → **Content Unit A**: `Full Episode` (Primary 16:9 or 9:16)
    - → **Content Unit B**: `Teaser` (15s social hook)
    - → **Content Unit C**: `Highlight Short` (cinematic cinematic snippet)
    - → **Content Unit D**: `Recap` (Summary of previous beats)

All units inherit the Episode's `series_id` and `project_id` but have unique `target_channel_id` mappings defined by the Router.

---

## 🚦 5. Episode Tracking: Comprehensive Status Models
Every Episode entity transitions through three independent status lifecycles:

### A. Story Status
1. **Imported**: Script/Episode pack received from Series source.
2. **Parsed**: Script analyzed by Gemini into scene blocks.
3. **Refined**: Prompts and Narration finalized.
4. **Approved**: Human/AI supervisor confirmed for production.

### B. Production Status
1. **Queued**: Waiting for GCloud Run worker.
2. **Generating Assets**: Imagen/TTS in progress.
3. **Assembling**: FFmpeg/MoviePy rendering.
4. **Completed**: Final `.mp4` and metadata ready in GCS.
5. **Failed**: Production error (Logged with retry count).

### C. Publishing Status
1. **Unscheduled**: Production ready but target unknown.
2. **Scheduled**: Linked to a `Schedule Item` with a timestamp.
3. **Publishing**: API upload in progress.
4. **Published**: Live on channel (Video ID returned).
5. **Revoked/Archived**: Manually removed or reached EOL.

---

## 📱 6. Channel Flexibility Models
The Publishing Router supports four distribution patterns:
1.  **1:1 (Legacy)**: One Project → One Channel (Standard).
2.  **1:N (Broadcast)**: One Project → Multiple Channels (Multi-branding).
3.  **N:1 (Shared Hub)**: Multiple Projects/Series → One Shared Channel (Aggregator).
4.  **Dynamic Evolution**: Move a Series to its own dedicated channel mid-production by updating the `Publishing Route`.

---

## 🕒 7. Scheduling & Cadence Logic
The **Schedule Manager** operates as a cron-aware state machine:
- **Recurring Cadence**: Defines intervals (e.g., "Episode every 3 days at 18:00").
- **Gap Fillers**: Automatic scheduling of **Teasers** and **Shorts** between main episode drops.
- **Next-Release Pointer**: Logic that automatically calculates the timestamp for `Episode_N+1` based on `Episode_N`'s success.
- **Queue Behavior**: If an episode fails production, subsequent ones stay "Held" until the chain is repaired or skipped.

---

## 🎨 8. Persistent Asset Logic (The Registry)
- **Character Registry**: Stores static visual seeds. Ensures "Ali" looks the same in Episode 1 and Episode 100.
- **Environment Registry**: Stores "Stage Seeds" for consistent backgrounds (The Space Lab, The Jungle).
- **Versioning Rules**: Asset updates create a new `version_id` to allow for "Timeskip" or "New Outfit" scenarios without breaking old assets.
- **QA Drift Checks**: Gemini multimodal comparison between `Episode_N` and `Registry_Master` to flag visual inconsistency.

---

## 💾 9. Data Schema Proposals

### Firestore Schema (Core)
- `projects/`
    - `{project_id}`
        - `config`: {category, style_reference_prompt, mode}
        - `assets/`: (sub-collection) {type, spec, seed_descriptors, voice_id}
- `series/`
    - `{series_id}`
        - `meta`: {name, cadence, pointer_to_current_ep}
        - `episodes/`: (sub-collection)
            - `{episode_id}`: {order, story_status, prod_status, pub_status, gcs_path, video_id}
- `publishing/`
    - `routes/`: {type_mapping, channel_map, schedule_pattern}
    - `schedule/`: {timestamp, content_unit_id, status}

### Cloud Storage (GCS) Layout
- `tariqtube-production/`
    - `workspaces/{ws_id}/`
        - `projects/{pj_id}/`
            - `assets/` (Original Character Art/Ref)
            - `series/{sr_id}/`
                - `packs/` (JSON Story Ingestion)
                - `episodes/{ep_id}/`
                    - `source/` (Gemini Script)
                    - `raw/` (Scene PNGs, Scene MP3s)
                    - `units/` (Final MP4s: full, teaser, shorts)

---

## 📊 10. Performance Loop
The system polls **Performance Records** every 24 hours post-publish. Gemini analyzes views/retention to suggest **Series Tuning** (e.g., "Make future scenes more colorful to improve CTR").

---
*Blueprint Version: 3.0 (Full Implementation Specification)*
*Author: TariqTube Architecture Team*
