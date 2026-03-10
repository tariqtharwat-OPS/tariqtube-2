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

## 4. Voice Profile & Vocal Signatures
Voice Profiles are mapped to the **Google Cloud TTS Studio** engine.
- **Locked Vocal ID**: Fixed Studio voice ID (e.g., `en-US-Studio-O`).
- **Signature Settings**: Static pitch (+/-), speaking rate, and volume gain.
- **Episodic Context**: The Production Engine maintains a history of character "emotional states" from previous scenes to ensure narrative voice consistency.

---

## 5. Series & Episode Lifecycle Integration
The **Series Manager** maintains the production pipeline via these mechanisms:
- **Episode Pointer**: An atomic counter in Firestore tracking `last_imported_index`, `last_produced_index`, and `last_published_index`.
- **Episodic Memory Buffer**: A 250,000-token summary of world history and previous episode plot points, injected into Gemini 1.5 Pro's 2M context window for every new script generation.
- **Continuity Ledger**: Track items like "Is the window broken?" or "Is the character holding a key?" across episodes.

---

## 6. Asset-Based Episode Construction Workflow
1.  **Selection**: Project Manager identifies the Project and Series.
2.  **Asset Pull**: Series Manager retrieves required Asset Record IDs (Firestore).
3.  **Prompt Assembly**:
    - Final Scene Prompt = `(Series Style Prefix) + (Character Visual Specs) + (Environment Stage Seed) + (Scene-Specific Action)`.
4.  **Production**: Production Engine triggers parallel GCloud Run tasks for Video (Cloud Run), Audio (TTS API), and Visuals (Vertex AI).
5.  **Status Sync**: UI tracks every stage from `Story: Approved` to `Publishing: Live`.

---
*Based on TariqTube 2.0 Architectural Blueprint v3.0*
