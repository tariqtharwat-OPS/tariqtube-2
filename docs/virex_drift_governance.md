# 🚫 TariqTube: No-Drift Rules

To maintain high production standards in an automated system, the following "No-Drift" rules are enforced:

## 1. Personality Drift
- **Rule**: Character traits must NOT mutate over episodes unless specified in a Growth Arc.
- **Enforcement**: Gemini prompts must include the "Character Persistence Matrix" as a system instruction for every script generation.

## 2. Visual Drift
- **Rule**: Characters and recurring objects must maintain the same visual identity across scenes.
- **Enforcement**: Image generation prompts must use **Static Seed Descriptors**. 
    - *Wrong*: "A cute robot." (Too vague, creates drift).
    - *Right*: "Sparky: a small spherical blue robot with a yellow star on its chest, chrome finish." (Consistent descriptors).

## 3. Vocal Drift
- **Rule**: A character's voice must never change.
- **Enforcement**: Voice assignments are hard-coded in the Series Pack.
    - *Example*: Character "Ali" is always `ar-XA-Studio-B`.

## 4. Logical Drift
- **Rule**: Earlier plot points must not be contradicted by the AI in future episodes.
- **Enforcement**: Multi-episode summaries (Episodic Memory) are fed into Gemini 1.5 Pro's 2M context window.

## 5. Metadata Drift
- **Rule**: SEO strategies (Hashtags/Keywords) must be consistent for a series to satisfy the YouTube algorithm.
- **Enforcement**: The SEO Generator uses a specific "Series Tag Template" for all episodes in a set.

---
*Inspired by OPS3 Transactional Ledger Principles*
