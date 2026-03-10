# 🚄 TariqTube: Migration Notes

## V1 (Local) to V2 (Cloud-Native) Migration

The project is transitioning from a local-heavy Windows suite to a fully scaleable Google Cloud-native architecture.

### Key Changes:
1.  **Orchestration**: `lite_stories/story_pipeline.py` (V1) is being replaced by `GoogleStoryPipeline` (V2) which uses Firestore for state tracking.
2.  **Model Shift**: OpenAI (V1) is migrated to **Gemini 1.5 Pro/3.1** (V2).
3.  **Image Generation**: Leonardo.AI (V1) is migrated to **Imagen 3.0** (V2) via Vertex AI.
4.  **Narration**: ElevenLabs (V1) is migrated to **Google Cloud Studio TTS** (V2) for zero-latency, Indistinguishable human speech.
5.  **Publishing**: Selenium/PyAutoGUI browser-based posting (V1) is migrated to **YouTube Data API v3** (V2) for headless efficiency.

### Verification of Success:
- Milestone project `g_20250621_150259_small_robot` successfully generated 2 scenes and uploaded via API.
- Video ID: `bikYlOQhCQg`
- Status: **Verified Milestone Reached**

### Next Steps:
- Porting remaining local assembly (`moviepy`) to a Dockerized Cloud Run service.
- Finalizing the "Series Pack" ingestion logic to support episodic consistency.

---
*Migration Lead: Antigravity AI*
