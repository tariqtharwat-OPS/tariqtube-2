# 👤 TariqTube: Asset & Series Framework (v4.1 Detail)

## 1. The Asset-First Philosophy: Global Production Specs
In TariqTube 2.0, Assets (Characters, Environments, Voices) are **Production Specifications** stored in Firestore. They ensure that a Project maintains a unified identity across multiple languages and series. An asset is initialized once and versioned as the project evolves.

---

## 2. Character Registry: Multi-Tongue Identity
A Character in TariqTube is a bundle of visual and vocal seeds that remain synchronized across all production branches.

### A. Visual Consistency (Imagen 3)
- **Master Seed**: A frozen Imagen 3 prompt block. 
    - *Example*: `[Sparky]: Sphere-shaped blue robot, 30cm tall, single orange digital eye, metallic finish.`
- **Multimodal Audit**: Gemini 1.5 Pro compares generated frames against the `master_seed_reference.png` in GCS. If the "Visual Signature" drifts (e.g., eye color changes), the frame is rejected.

### B. Vocal Consistency (Cloud TTS Studio)
Characters maintain their "soul" across languages through a **Multilingual Vocal Matrix**:
| Language | Voice ID | Pitch | Rate | Style |
| :--- | :--- | :--- | :--- | :--- |
| **Arabic** | `ar-XA-Studio-B` | -2.0 | 1.05 | Narrative |
| **English** | `en-US-Studio-O` | +1.0 | 1.00 | Professional |
| **Spanish** | `es-ES-Studio-F` | 0.0 | 0.95 | Energetic |

**Technical Rule**: Prosody inheritance ensures that if a Character is "excited" in the master script, the emotional markers are carried over into the localized TTS generation for all enabled variants.

---

## 3. Environment Registry: Persistent Stages
Environments are "Stages" that provide the constant background for the Visual Master render.
- **Stage Seed**: A static prompt fragment defining the atmosphere, lighting, and landmarks.
- **Master Render**: The Environment is rendered once per scene and shared by all language variants, ensuring zero background drift between localizations.

---

## 4. Series Continuity & Multi-Variant Sync
The **Series Manager** ensures that episodic progress is tracked globally:
- **Global Index**: If a project has Arabic and English branches, both are locked to the same `episode_order` (e.g., Ep 45 is the same story in both).
- **History Memory**: Gemini 1.5 Pro reads the previous 5 episodes' summaries to maintain plot logic. These summaries are maintained in a "Global Project Log" so all language variants benefit from the same narrative memory.

---

## 5. Asset-Based Construction Workflow (v4.1)
1.  **Ingestion**: Select Project → Series → target Locales (`ar`, `en`).
2.  **Asset Load**: Retrieve Character/Environment specs and the **Vocal Matrix**.
3.  **Visual Master Render**: 
    - Generate Script (Master Language).
    - Generate Frames (Visual Seeds).
    - Assemble **Visual Master MP4** (BGM + Visuals, no speech).
4.  **Local Branching (Parallel)**:
    - **AR Variant**: Translate script → Generate AR Narration → Overlay on Master → SEO Gen.
    - **EN Variant**: Translate script → Generate EN Narration → Overlay on Master → SEO Gen.
5.  **Multi-Platform Routing**:
    - Route `AR` to Arabic YT/IG.
    - Route `EN` to English YT/TT.

---
*Version: 4.1 (Global Identity Standards)*
*Author: TariqTube Asset Governance*
