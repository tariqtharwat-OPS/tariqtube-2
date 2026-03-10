# 👤 TariqTube: Project-Centric Asset & Series Framework

## 1. The Asset-First Philosophy
In TariqTube 2.0, **Assets** (Characters, Environments, Voice Profiles) are the foundational building blocks of a Project. They are not merely prompt descriptors but **persistent entities** stored in the Asset Manager (Firestore) to prevent visual and narrative drift.

---

## 2. Character Persistence Matrix
Each Character asset is a "Production Spec" used by the Production Engine:
- **Visual Seed**: A standardized Imagen 3 prompt block that MUST be included in every scene generation.
    - *Example*: `[Character: Sparky | Traits: spherical blue body, single orange eye, chrome finish]`
- **Vocal Signature**: A locked Google Cloud TTS Studio voice ID and specific prosody settings.
- **Narrative DNA**: Personality traits, catchphrases, and growth arc status.
- **Reference Gallery**: (Future) Stored images of the character used for reference in Gemini multimodal checks.

---

## 3. Environment Persistence
Environments are treated as "Stages" where episodes take place:
- **Environment Specs**: Constant visual prompts for recurring locations (e.g., "The Magic Forest", "Ali's Workshop").
- **Atmospheric Rules**: Color palettes, lighting styles, and specific background elements.

---

## 4. Series & Episode Management
The **Series Manager** tracks the production lifecycle of sequential content:
- **Current Pointer**: Tracks the "Last Produced Episode" and "Last Published Episode".
- **Continuity Ledger**: A summary of previous plot points stored in the Project state to feed Gemini's context.
- **Cadence Logic**: Scheduled intervals (e.g., "Every Monday at 6 PM") linked to the Schedule Manager.

---

## 5. Production Workflow (Project-Centric)
1.  **Ingestion**: Select a Project and Series context.
2.  **Asset Load**: The Asset Manager pulls persistent specs for required Characters and Environments.
3.  **Episode Construction**: 
    - Gemini generates a script using the **Continuity Ledger** + **Asset Specs**.
    - Imagen 3 generates frames using the **Visual Seeds**.
    - Cloud TTS generates audio using the **Vocal Signature**.
4.  **Content Multiplier**: The Production Engine renders the primary Episode and automatically generates derivative **Teasers** and **Shorts**.
5.  **Routing**: The Publishing Router identifies the target channels for each content unit.

---
*Based on TariqTube 2.0 Architectural Blueprint v2.1*
