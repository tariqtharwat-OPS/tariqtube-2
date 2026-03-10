"""
Google-Native Story Pipeline for TariqTube 2.0
Uses Gemini, Google Cloud TTS (Studio), and Imagen 3.
Tracks state in Firestore and uploads to YouTube via Data API.
"""

import os
import json
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import shutil

# Google Cloud Libraries
from google import genai
from google.cloud import texttospeech
from google.cloud import firestore
from google.cloud import storage
import vertexai
from vertexai.preview.vision_models import ImageGenerationModel

# Add the project root to path
import sys
sys.path.append(str(Path(__file__).parent.parent))

from lite_stories_next.posting.youtube_oauth2_upload import YouTubeOAuth2Uploader

logger = logging.getLogger('GoogleStoryPipeline')

class GoogleStoryPipeline:
    def __init__(self, project_id: str = "tariqtube-production", location: str = "us-central1"):
        self.project_id = project_id
        self.location = location
        
        # Determine path to credentials (assume tariq-worker-key.json exists in root)
        self.creds_path = Path(__file__).parent.parent / "tariq-worker-key.json"
        if self.creds_path.exists():
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = str(self.creds_path)
            logger.info(f"Using credentials from {self.creds_path}")
        
        # Initialize Clients
        vertexai.init(project=self.project_id, location=self.location)
        self.db = firestore.Client(project=self.project_id)
        self.storage_client = storage.Client(project=self.project_id)
        self.tts_client = texttospeech.TextToSpeechClient()
        
        # We'll use the legacy SDK for Gemini 3.1 for now since we verified it works best
        import google.generativeai as genai_legacy
        self.gemini = genai_legacy.GenerativeModel('models/gemini-3.1-pro-preview')
        
        # Output directories
        project_root = Path(__file__).parent.parent
        self.output_dir = project_root / "output"
        self.projects_dir = self.output_dir / "google_projects"
        self.final_videos_dir = self.output_dir / "final_videos"
        
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.final_videos_dir.mkdir(parents=True, exist_ok=True)

    def run_pipeline(self, theme: str, language: str = "English", voice_name: str = "en-US-Studio-O", scenes_count: int = 5, auto_upload: bool = False) -> Dict[str, Any]:
        """Runs the full pipeline from script generation to final video."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = f"g_{timestamp}_{theme.lower().replace(' ', '_')}"
        project_dir = self.projects_dir / project_name
        project_dir.mkdir(exist_ok=True)
        
        # Initialize Firestore record
        doc_ref = self.db.collection("story_projects").document(project_name)
        doc_ref.set({
            "project_id": project_name,
            "theme": theme,
            "language": language,
            "status": "Starting",
            "created_at": firestore.SERVER_TIMESTAMP,
            "steps": {}
        })

        try:
            # 1. Generate Script
            self._update_status(doc_ref, "Scripting", f"Generating {scenes_count}-scene story script with Gemini 3.1")
            script = self._generate_script_gemini(theme, language, scenes_count=scenes_count)
            doc_ref.update({"script": script, "title": script['title']})
            
            # 2. Generate SEO Content
            self._update_status(doc_ref, "SEO", "Optimizing metadata for YouTube")
            seo = self._generate_seo(script, language)
            doc_ref.update({"seo": seo})
            
            # 3. Generate Voice Narration (TTS)
            self._update_status(doc_ref, "Voices", "Synthesizing Studio-quality narration")
            voice_dir = project_dir / "voice"
            voice_dir.mkdir(exist_ok=True)
            voice_files = self._generate_voices(script['scenes'], voice_dir, language, voice_name)
            
            # 4. Generate Images (Imagen 3)
            self._update_status(doc_ref, "Imaging", "Generating scenes with Imagen 3")
            image_dir = project_dir / "images"
            image_dir.mkdir(exist_ok=True)
            image_files = self._generate_images(script['scenes'], image_dir)
            
            # 5. Video Assembly
            self._update_status(doc_ref, "Assembly", "Merging assets into final video")
            video_dir = project_dir / "video"
            video_dir.mkdir(exist_ok=True)
            final_video_path = self._assemble_video(image_files, voice_files, video_dir)
            
            # 6. Optional Upload
            upload_result = None
            if auto_upload:
                self._update_status(doc_ref, "Publishing", "Uploading to YouTube (API)")
                upload_result = self._upload_to_youtube(final_video_path, seo)
                doc_ref.update({"youtube_result": upload_result})
            
            # 7. Finalize
            self._update_status(doc_ref, "Success", "Project finalized")
            doc_ref.update({
                "final_video_path": str(final_video_path),
                "status": "Completed"
            })
            
            return {
                "project_id": project_name, 
                "video": str(final_video_path),
                "youtube": upload_result
            }

        except Exception as e:
            logger.error(f"Pipeline failed: {e}")
            self._update_status(doc_ref, "Failed", str(e))
            raise

    def _update_status(self, doc_ref, phase: str, detail: str):
        print(f"[{phase}] {detail}")
        doc_ref.update({
            f"steps.{phase}": {
                "detail": detail,
                "timestamp": firestore.SERVER_TIMESTAMP
            },
            "current_phase": phase
        })

    def _generate_script_gemini(self, theme: str, language: str, scenes_count: int = 5) -> Dict:
        prompt = f"""Write a children's story about "{theme}" in {language}.
Format the output as a JSON object with:
- "title": A catchy title.
- "scenes": A list of {scenes_count} scenes, each with:
  - "title": Scene name.
  - "description": Highly detailed visual prompt for an image generator (Imagen 3).
  - "narration": The text that will be spoken (15-20 seconds worth of speech).
Return ONLY the JSON."""
        
        response = self.gemini.generate_content(prompt)
        text = response.text
        # Clean up JSON if LLM included block quotes
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        return json.loads(text)

    def _generate_seo(self, script: Dict, language: str) -> Dict:
        prompt = f"""Based on this story title "{script['title']}", generate SEO metadata for YouTube.
Language: {language}
Format the output as a JSON object with:
- "title": An optimized title (under 70 chars)
- "description": A short engaging description (150-200 chars)
- "tags": A list of 10 relevant tags.
Return ONLY the JSON."""
        
        response = self.gemini.generate_content(prompt)
        text = response.text
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        return json.loads(text)

    def _upload_to_youtube(self, video_path: Path, seo: Dict) -> Dict:
        uploader = YouTubeOAuth2Uploader()
        if uploader.authenticate():
            result = uploader.upload_video(
                video_path=str(video_path),
                title=seo['title'],
                description=seo['description'],
                tags=seo['tags'],
                privacy="unlisted",  # Safer for automation
                made_for_kids=True
            )
            return result
        else:
            return {"success": False, "error": "Auth failed"}

    def _generate_voices(self, scenes: List[Dict], output_dir: Path, language: str, voice_name: str) -> List[str]:
        voice_files = []
        lang_code = "ar-XA" if "arabic" in language.lower() else "en-US"
        
        for i, scene in enumerate(scenes):
            filename = f"scene_{i:02d}.mp3"
            filepath = output_dir / filename
            
            input_text = texttospeech.SynthesisInput(text=scene['narration'])
            voice = texttospeech.VoiceSelectionParams(language_code=lang_code, name=voice_name if "Studio" in voice_name else None)
            audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
            
            response = self.tts_client.synthesize_speech(input=input_text, voice=voice, audio_config=audio_config)
            with open(filepath, "wb") as out:
                out.write(response.audio_content)
            voice_files.append(str(filepath))
        return voice_files

    def _generate_images(self, scenes: List[Dict], output_dir: Path) -> List[str]:
        image_files = []
        # Use the "fast" model which usually has higher quota/speed
        model = ImageGenerationModel.from_pretrained("imagen-3.0-fast-generate-001")
        
        for i, scene in enumerate(scenes):
            filename = f"scene_{i:02d}.png"
            filepath = output_dir / filename
            
            print(f"Generating image for scene {i}...")
            # Use the Imagen model to generate the image
            images = model.generate_images(prompt=scene['description'], number_of_images=1)
            images[0].save(location=str(filepath), include_generation_parameters=False)
            image_files.append(str(filepath))
            
            # Add a delay to avoid quota issues
            if i < len(scenes) - 1:
                print("Waiting 10s for quota reset...")
                time.sleep(10)
                
        return image_files

    def _assemble_video(self, image_files: List[str], voice_files: List[str], video_dir: Path) -> Path:
        from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
        
        clips = []
        for img, audio in zip(image_files, voice_files):
            a_clip = AudioFileClip(audio)
            i_clip = ImageClip(img, duration=a_clip.duration)
            i_clip.audio = a_clip
            clips.append(i_clip)
            
        final_video = concatenate_videoclips(clips, method="compose")
        final_path = video_dir / "final_video.mp4"
        final_video.write_videofile(str(final_path), fps=24, logger=None, codec='libx264', audio_codec='aac')
        
        # Backup to main final_videos dir
        public_path = self.final_videos_dir / f"{video_dir.parent.name}.mp4"
        shutil.copy2(final_path, public_path)
        
        return public_path
