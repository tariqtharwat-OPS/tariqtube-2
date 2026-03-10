# 👤 TariqTube: Project-Centric Asset & Series Framework (Implementation Detail)

## 1. The Asset-First Philosophy: Immutable Production Units
In TariqTube 2.0, Assets are not temporary generation prompts; they are **Persistent Data Models** in Firestore. An Asset (Character, Environment, or Voice) must be initialized in the **Project Asset Registry** before it can be referenced in an episode script.

---

## 2. Character Registry: Static Visual Scaling
Characters are the most critical assets for series consistency.
- **Visual Spec (JSON)**: Contains the base Imagen 3 seed descriptors (colors, features, materials).
- **Versioning**: When a character changes (e.g., a "New Costume"), a new asset version is created (`v2`). The Episode Tracker links each production run to a specific asset version ID.
- **Multimodal Drift Check**: Gemini 1.5 Pro performs a multimodal comparison between the master "Registry Reference Image" and the "Generated Scene Frame". If deviation (color, shape, scale) exceeds a 15% threshold, the frame is flagged for re-generation.

---

## 3. Environment Registry: Persistent Stages
Environments define the world logic.
- **Stage Seed**: A static prompt fragment defining the background style, lighting level (lux/atm), and persistent landmarks.
- **Scoping**: Assets can be assigned to `Global` (available for any series in the project) or `Series-Locked` (e.g., "The Lab" only appears in the "Robot" series).

---

## 4. Multilingual Voice Profiles (Vocal Signatures)
Character identity is maintained across languages through a strict **Vocal Matrix**:
- **Character Voice Map**: Each character in the Registry is assigned a specific **Google Cloud TTS Studio** profile for every supported language.
    - *Example (Character: Sparky)*:
        - `ar`: `ar-XA-Studio-B` (Deep, resonant)
        - `en`: `en-US-Studio-O` (Warm, intelligent)
- **Signature Consistency**: Pitch and speaking rate offsets are carried over across languages where possible to maintain the character's "energy" regardless of the tongue.
- **Episodic Context**: The Production Engine ensures that if Sparky was "surprised" in the master script, the generated audio for both `ar` and `en` variants reflects that specific prosody.

---

## 5. Series & Episode Lifecycle Integration
The **Series Manager** maintains the production pipeline via these mechanisms:
- **Episode Pointer**: An atomic counter in Firestore tracking `last_imported_index`, `last_produced_index`, and `last_published_index`.
- **Synchronization**: Language variants for a single episode share the same `series_index` to ensure that "Episode 45" is consistent across all global channels.
- **Episodic Memory Buffer**: Summaries are translated/maintained to ensure Gemini's context for a variant is accurate to the local language nuances.

---

## 6. Asset-Based Episode Construction Workflow
1.  **Selection**: Project Manager identifies the Project and Series.
2.  **Asset Pull**: Series Manager retrieves required Asset Record IDs (Firestore).
3.  **Visual Master Render**: Production Engine renders the mute video master.
4.  **Variant Branching**: 
    - Engine reads script and pulls **Locale-Specific Voice Profiles**.
    - Cloud TTS generates parallel audio tracks (`ar`, `en`, etc.).
    - FFmpeg assembles localized final renders.
5.  **Status Sync**: UI tracks every stage from `Visual Master: Done` to `Variant [locale]: Published`.

---
*Based on TariqTube 2.0 Architectural Blueprint v4.0*
