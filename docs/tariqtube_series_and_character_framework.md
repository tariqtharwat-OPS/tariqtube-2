# 👤 TariqTube: Asset & Series Framework (v4.1 Detail)

## 1. Asset-First Philosophy: Global Production Specs
In TariqTube 2.0, Assets (Characters, Environments, Voices) are **Persistent Production Units** stored in Firestore. They are initialized once in the Project Registry and then versioned as the project evolves. This eliminates visual and vocal drift over hundreds of episodes.

---

## 2. Character Registry: Multi-Tongue Identity
Characters are the most critical assets for global series consistency and project recognition.

### A. Visual Identity (Imagen 3)
- **Master Visual Seed**: A frozen, high-detail Imagen 3 prompt block.
    - *Example (Sparky)*: `[Sparky]: Sphere-shaped blue metallic body, single orange digital eye, white antennae, small chrome legs.`
- **Multimodal Audit**: Gemini 1.5 Pro performs a multimodal comparison between the "Visual Master Reference" and the "Generated Scene Frames". If deviation occurs (e.g., body shape shifts), the scene is flagged.

### B. Vocal Identity (Cloud TTS Studio)
Character identity is maintained across languages through a strict **Multilingual Vocal Matrix**:
| Locale | Voice ID | Pitch | Speaking Rate | Vocal Archetype |
| :--- | :--- | :--- | :--- | :--- |
| **Arabic** | `ar-XA-Studio-B` | -2.0 | 1.05 | Wise/Patient |
| **English** | `en-US-Studio-O` | +1.0 | 1.00 | Curious/Energetic |
| **Spanish** | `es-ES-Studio-F` | 0.0 | 0.95 | Energetic |

**Technical Rule**: The "Prosody Inheritance" engine ensures that the character's emotional state in any master scene (e.g., "excited") is translated into the localized vocal markers of every Language Variant.

---

## 3. Environment Registry: Persistent Stages
Environments provide the constant background for the Visual Master render.
- **Stage Seed**: A static prompt fragment defining the atmosphere, lighting lux, and constant landmarks.
- **Visual Consistency**: The environment is rendered once per scene and shared by all localized audio tracks.

---

## 4. Series Continuity & Multi-Variant Synchronization
The **Series Manager** ensures that episodic progress is tracked as a unified global entity:
- **Episode Numbering (Order)**: If `Episode 45` is released, all enabled Language Variants for `45` are synchronized and released as a block.
- **Global Project Memory**: Gemini 1.5 Pro reads the summaries of the last 5 episodes to maintain plot logic. These summaries are maintained in a "Global Registry" so all language variants benefit from the same narrative context.

---

## 5. Asset-Based Infrastructure (Firestore Proposal)
- `projects/{pj_id}/registry/assets/`
    - `type`: 'character' | 'environment' | 'voice'
    - `visual_seed`: (Prompt Fragment)
    - `vocal_matrix`: {ar: id, en: id, es: id}
    - `reference_images`: [GCS_URLs] (For multimodal drift audit)
    - `version`: v1.0.0

---

## 6. Construction Workflow (The Content Factory)
1.  **Ingestion**: Select Project → Series → target Locales.
2.  **Asset Pull**: Retrieve all Character/Environment IDs.
3.  **Visual Master Render**:
    - Script Generation.
    - Scene Generation (Visual Seeds only).
    - Assembly of the **Mute Visual Master MP4**.
4.  **Local Branching (Parallel)**:
    - **Arabic Branch**: Local Narration Gen → Overlay → Meta Gen.
    - **English Branch**: Local Narration Gen → Overlay → Meta Gen.
5.  **Audit & Publish**: Multimodal drift check before the Publishing Router triggers.

---
*Version: 4.1 (Global Specs)*
*Author: TariqTube Asset Governance*
