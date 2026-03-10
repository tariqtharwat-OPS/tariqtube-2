# 👤 TariqTube: Series and Character Framework

## 1. Core Philosophy
TariqTube 2.0 moves from "One-off Stories" to **Episodic Series Production**. This requires a strict framework for character persistence and world-building to ensure Gemini maintains consistency over 100+ episodes.

## 2. Character Persistence Matrix
Any character introduced in a series must have a defined **Persistence Profile**:
- **Name & Age**: Static identification.
- **Personality**: Detailed description (2M token context allows for full backstory retention).
- **Appearance (Imagen Prompts)**: Standardized visual descriptors to prevent "visual drift".
    - *Example*: "Sparky the robot, small blue chassis, single large orange eye, white antennae."
- **Growth Arc**: How the character develops over the series.
- **Voice Profile**: Mapping to a specific Google Cloud TTS (Studio) voice ID to ensure narration consistency.

## 3. World Framework
Each series has a defined **World Context**:
- **Setting**: Primary locations and atmosphere.
- **Rules**: Logics of the world (e.g., animals can talk, gravity is low).
- **History**: Previous episode summary/knowledge available to Gemini via episodic memory.

## 4. Episode Ingestion Workflow
1.  **Series Pack**: A JSON-based definition of characters, settings, and themes.
2.  **State Tracking**: Gemini reads the "Last 3 Episode Summaries" to ensure plot continuity.
3.  **Storyboard Generation**: Specific Imagen 3 prompts derived from the Character Persistence Profile.
4.  **Production**: Scripting, SEO, Media Gen, and Assembly.

---
*Based on TariqTube 2.0 Production Goals*
