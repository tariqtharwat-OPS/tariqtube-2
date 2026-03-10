# 👤 Virex Engine: Asset & Series Framework (v5.0 Detail)

## 1. Asset-First Philosophy: Global Production Specs
In the **Virexa AI Content Factory**, Assets (Characters, Environments, Voices) are **Persistent Production Units** stored in the **Virex Registry**. They are initialized once and then versioned as the project evolves, ensuring identity continuity across multiple platforms and languages.

---

## 2. Character Registry: Multi-Tongue Identity
Characters are the primary carriers of project branding and narrative soul.

### A. Visual Consistency (Imagen 3)
- **Master Visual Seed**: A static prompt fragment in the Registry defines the base appearance.
    - *Example (Sparky)*: `[Sparky]: Sphere-shaped blue metallic body, single orange digital eye, white antennae, small chrome legs.`
- **Multimodal Drift Audit**: Gemini 1.5 Pro performs a comparison between the "Visual Master Reference" and generated scene frames. If drift occurs (e.g., eye color shifts), the scene is flagged by the **Review Layer**.

### B. Vocal Consistency (Cloud TTS Studio)
Character identity is maintained across languages through a strict **Multilingual Vocal Matrix**:
| Locale | Voice ID | Pitch | Rate | Style |
| :--- | :--- | :--- | :--- | :--- |
| **Arabic** | `ar-XA-Studio-B` | -2.0 | 1.05 | Narrative |
| **English** | `en-US-Studio-O` | +1.0 | 1.00 | Professional |
| **Spanish** | `es-ES-Studio-F` | 0.0 | 0.95 | Energetic |

**Virex Technical Rule**: The **LocaleConfig** (Project Level) defines the default voice and character mappings for each region, allowing for consistent brand voices without manual per-episode configuration.

---

## 3. Environment Registry: Persistent Stages
Environments provide the constant background for the **Visual Master** render.
- **Stage Seed**: A static prompt fragment defining the atmosphere, lighting, and landmarks.
- **Visual Consistency**: The environment is rendered once per scene and shared by all localized audio tracks.

---

## 4. Optional Visual Override (Regional Localization)
The **Virex Engine** supports localized on-screen text or regional signage through an optional **Visual Override** mechanism in the Production Pipeline:
- **Signage Swap**: Replace English signs with Arabic/Spanish localized textures for specific renders.
- **Master-Variant Logic**: The Engine renders the Visual Master first, then performs localized patches only where an override is defined.

---

## 5. Series Continuity & Multi-Variant Synchronization
The **Series Manager** ensures that episodic progress is tracked as a unified global entity:
- **Global Episode Index**: Episode `45` is the same story globally.
- **Synchronized Posting**: All Language Variants for an episode are synchronized in the **Schedule Manager** to hit their respective regional release windows simultaneously.

---

## 6. Revision History & Audit
- All assets and variants track **Revision History**.
- If a voice profile is changed mid-series, the `updated_at` and `change_reason` are logged to preserve the lineage of the production evolution.

---
*Virex Asset Governance v5.0 (Global Standards)*
*Author: Virexa AI Architecture Hub*
