# 🎮 Virex Engine: Master Architectural Blueprint (v5.0)

## 📋 1. Core Architectural Principle: Virexa AI Content Factory
Virexa AI is a **Project-Centric**, **Multilingual**, and **Governance-Enabled** content factory. The **Virex Engine** is designed to produce consistent, episodic content at scale across multiple languages and social platforms from a single master production source.

### Key Pillars:
- **Projects as the Source of Truth**: All production state, character persistence, and episodic memory live at the Project level.
- **Virex Multilingual Synchronization**: One **Visual Master** (Visual Anchor) is rendered once. Multiple **Language Variants** (Linguistic Anchors) branch from it.
- **Virex Human Governance Layer**: Integrated review workflows for scripts, renders, and metadata.
- **Platform-Agnostic Routing**: Decoupled adapters for global synchronization (YouTube, TikTok, Instagram).

---

## 🏗️ 2. Detailed Data Model: System Entities

### A. Organizational Layer
| Entity | Description | Ownership |
| :--- | :--- | :--- |
| **Workspace** | Top-level administrative container. | L1 |
| **Project** | **The Master Owner.** Owns the Asset Registry and **LocaleConfig**. | Belongs to Workspace |
| **LocaleConfig** | Language-specific defaults (voices, SEO templates, targeting). | Belongs to Project |

### B. Production & Localization Layer
| Entity | Description | Ownership |
| :--- | :--- | :--- |
| **Series** | Grouping for episodic content with sequential ordering. | Belongs to Project |
| **Episode** | **The Visual Anchor.** One visual master render. Shared ID. | Belongs to Series |
| **LanguageVariant**| **The Linguistic Anchor.** Owns localized audio, SEO, and Revision History. | Belongs to Episode |
| **Asset** | Persistent entities (Characters, Environments) with Vocal Matrices. | Belongs to Project |

### C. Distribution & Performance Layer
| Entity | Description | Ownership |
| :--- | :--- | :--- |
| **Content Unit** | Specific media deliverables (Full, Teaser, Short). | Belongs to Variant |
| **Channel** | A publishing destination (Specific to a platform/locale). | Flat Link |
| **Publishing Route** | Mapping logic (Timezones, CAD, Regional Rules). | Config |
| **PerformanceRecord**| Analytics poll result (Views, CTR, Retention, BQ-ready). | Belongs to Project |

---

## 🔐 3. Virex Governance & Human Review Layer
The engine implements a strict **Review Logic** between generation and publishing:
- **Reviewable Units**: Script, Translated Script, Thumbnail, Visual Master, Localized Render, SEO Metadata.
- **States**: `review_not_required`, `pending_review`, `approved`, `rejected`, `needs_revision`.
- **Metadata Tracks**: 
    - `reviewer_id`, `reviewer_notes`, `decision_reason`, `decision_timestamp`.
    - **Reason Codes**: `translation_risk`, `policy_risk`, `visual_drift`, `voice_mismatch`.
- **Workflow**: `Regenerate` → `QA Auto-Audit` → `Human Review (if triggered)` → `Approve` → `Router Publishing`.

---

## 🌍 4. Localization: LanguageVariant & Visual Override
The **LanguageVariant** represents a final localized product and tracks **Revision History**:
- **Entity Identification**: `{episode_id}_{locale}`.
- **Locale Logic**: Script, SEO (Title, Desc, Tags), Subtitles.
- **Optional Visual Override**: Supports region-specific frames (signage, localized on-screen text) without breaking the master visual sequence.
- **Revision Support**: Tracks `revision_id`, `previous_revision_id`, `change_reason`, and `active_revision` for all narration and metadata edits.

---

## 🚀 5. platform-Agnostic Publishing & Scheduling
The **Virex Publishing Router** supports adapter-based extension:
- **Scheduling States**: `queued`, `scheduled`, `delayed`, `paused`, `cancelled`, `published`.
- **Synchronization**: Automatically manages teaser insertion and calculates cadence offsets when production delays occur.
- **Timezone Awareness**: Routes are locale-anchored to hit regional peak hours.

---

## 🕒 6. Observability & Pipeline Monitoring
Every major stage (Generation, Assembly, Localization, Publishing) must be traceable:
- **Job Status Tracking**: `job_id`, `retry_count`, `failure_reason`, `correlation_id`.
- **Timing Invariants**: Every stage logs `started_at`, `completed_at`, and `worker_instance_id`.
- **Failure Analysis**: Automatic reporting of Cloud Run container exit codes for FFmpeg/MoviePy renders.

---

## 💾 7. Final System Infrastructure

### Firestore Schema Specification (v5.0)
- `workspaces/{ws_id}/` (Admin settings)
- `projects/{pj_id}/`
    - `registries/assets/`: {type, visual_seed, voices: {ar: id, en: id}, reference_images}
    - `locale_configs/{lang_code}/`: {default_voice, seotemplate, channel_targets, cultural_rules}
    - `series/{sr_id}/episodes/`
        - `episodes/{ep_id}/`: {order, visual_status, master_render_path, revisions: []}
        - `variants/`: (sub-collection)
            - `{locale_code}`: {status, script, audio, render_path, seo, review_status, revision_history: []}
- `publishing/routes/`: {project_id, lang_code, platform, channel_id, schedule_pattern}
- `publishing/schedule/`: {timestamp, variant_path, unit_type, status, error_log}
- `analytics/performance/`: {platform, external_id, views, ctr, retention, source_variant_id, timestamp}

### Cloud Storage (GCS) Hierarchy
- `virexa-production/`
    - `projects/{pj_id}/assets/` (Virex Master character Sheets)
    - `episodes/{ep_id}/`
        - `master/` (Visual Master .mp4)
        - `variants/`
            - `{locale}/` (localized narration, localized renders, signage overrides)
        - `history/` (Old revisions of audio and metadata)

---
*Virex Engine v1.0 (Enterprise Specification)*
*Author: Virexa AI Architecture Governance*
