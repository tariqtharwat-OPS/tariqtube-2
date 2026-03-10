"""
Story Pipeline Module for Stories Channels App
Handles complete workflow: script → voice → images → video → SEO
"""

import os
import json
import time
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
from PIL import Image, ImageDraw, ImageFont
import random

# Import shared modules
import sys
sys.path.append(str(Path(__file__).parent.parent))

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

# ElevenLabs is now handled via direct API calls with requests
# No need for the elevenlabs library - we use requests directly
ELEVENLABS_AVAILABLE = True  # Always true since we use requests

try:
    from moviepy.editor import ImageClip, AudioFileClip, CompositeVideoClip, concatenate_videoclips, VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False

logger = logging.getLogger('StoryPipeline')

class StoryPipeline:
    """Complete story generation and production pipeline"""
    
    def __init__(self, config_manager):
        self.config_manager = config_manager
        
        # Use centralized path configuration
        import sys
        from pathlib import Path
        
        # Load paths from config
        try:
            # Load environment variables from env.txt
            env_file = Path(__file__).parent.parent / "env.txt"
            if env_file.exists():
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            os.environ[key.strip()] = value.strip()
            
            # Get paths from environment with fallbacks
            project_root = Path(os.getenv("PROJECT_ROOT", Path(__file__).parent.parent))
            self.output_dir = project_root / "output"
            self.projects_dir = Path(os.getenv("PROJECTS_DIR", str(self.output_dir / "projects")))
            self.final_videos_dir = Path(os.getenv("FINAL_VIDEOS_DIR", str(self.output_dir / "final_videos")))
            
            # Ensure directories exist
            self.projects_dir.mkdir(parents=True, exist_ok=True)
            self.final_videos_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"📁 Using centralized paths:")
            logger.info(f"   Projects: {self.projects_dir.absolute()}")
            logger.info(f"   Final videos: {self.final_videos_dir.absolute()}")
            
        except Exception as e:
            logger.warning(f"⚠️ Path config error: {e}, using fallback")
            # Fallback to manual path construction
            current_file = Path(__file__).resolve()
            project_root = current_file.parent.parent
            self.output_dir = project_root / "output"
            self.projects_dir = self.output_dir / "projects"
            self.final_videos_dir = self.output_dir / "final_videos"
            self.projects_dir.mkdir(parents=True, exist_ok=True)
            self.final_videos_dir.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Fallback paths: Projects={self.projects_dir.absolute()}")
        
        # Initialize API clients
        self._setup_apis()
    
    def _ensure_env_loaded(self):
        """Ensure environment variables are loaded from env.txt"""
        try:
            env_file = Path(__file__).parent.parent / "env.txt"
            if env_file.exists():
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            # Only set if not already in environment
                            if key.strip() not in os.environ:
                                os.environ[key.strip()] = value.strip()
        except Exception as e:
            logger.warning(f"Could not load env file: {e}")
    
    def _setup_apis(self):
        """Setup API clients"""
        # OpenAI
        if OPENAI_AVAILABLE:
            # Try environment variable first, then config
            openai_key = os.getenv("OPENAI_API_KEY") or self.config_manager.get_api_key("openai")
            if openai_key:
                openai.api_key = openai_key
                logger.info("OpenAI API configured")
            else:
                logger.warning("OpenAI API key not found")
        
        # ElevenLabs
        if ELEVENLABS_AVAILABLE:
            # Try environment variable first, then config
            elevenlabs_key = os.getenv("ELEVENLABS_API_KEY") or self.config_manager.get_api_key("elevenlabs")
            if elevenlabs_key:
                os.environ["ELEVEN_API_KEY"] = elevenlabs_key
                logger.info("ElevenLabs API configured")
            else:
                logger.warning("ElevenLabs API key not found")
    
    def generate_story_content(self, language: str, theme: str, characters: List[str] = None, 
                             channel_id: str = None, auto_upload_youtube: bool = False, 
                             selected_voice_id: str = None) -> Dict[str, Any]:
        """Generate complete story content"""
        logger.info(f"Starting story generation: {language}, theme: {theme}")
        
        # Use provided voice ID or fallback to config
        voice_id = selected_voice_id
        if not voice_id:
            # Try environment variable first, then fallback
            voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
        
        logger.info(f"🎤 Using voice ID for story generation: {voice_id}")
        logger.info(f"🎤 Voice selection priority: provided={selected_voice_id}, env={os.getenv('ELEVENLABS_VOICE_ID')}")
        
        # Create project directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_name = f"{timestamp}_{theme.lower().replace(' ', '_')}"
        project_dir = self.projects_dir / project_name
        project_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (project_dir / "voice").mkdir(exist_ok=True)
        (project_dir / "images").mkdir(exist_ok=True)
        (project_dir / "video").mkdir(exist_ok=True)
        
        project_data = {
            "project_id": project_name,
            "project_dir": str(project_dir),
            "language": language,
            "theme": theme,
            "characters": characters or [],
            "channel_id": channel_id,
            "voice_id": voice_id,
            "created_at": datetime.now().isoformat(),
            "status": "generating"
        }
        
        try:
            # Step 1: Generate story script
            logger.info("Step 1: Generating story script")
            story_data = self._generate_story_script(language, theme, characters)
            project_data["story"] = story_data
            
            # Save script
            script_path = project_dir / "script.txt"
            with open(script_path, 'w', encoding='utf-8') as f:
                f.write(f"Title: {story_data['title']}\n")
                f.write(f"Voice ID: {voice_id}\n\n")
                for i, scene in enumerate(story_data['scenes'], 1):
                    f.write(f"Scene {i}: {scene['title']}\n")
                    f.write(f"Description: {scene['description']}\n")
                    f.write(f"Narration: {scene['narration']}\n\n")
            
            # Step 2: Generate voice narration with selected voice
            logger.info(f"Step 2: Generating voice narration with voice ID: {voice_id}")
            voice_files = self._generate_voice_narration(story_data['scenes'], project_dir / "voice", language, voice_id)
            project_data["voice_files"] = voice_files
            
            # Step 3: Generate scene images
            logger.info("Step 3: Generating scene images")
            image_files = self._generate_scene_images(story_data['scenes'], project_dir / "images", theme)
            project_data["image_files"] = image_files
            
            # Step 4: Create animated videos
            logger.info("Step 4: Creating animated videos")
            video_files = self._create_animated_videos(image_files, voice_files, project_dir / "video")
            project_data["video_files"] = video_files
            
            # Step 5: Assemble final video
            logger.info("Step 5: Assembling final video")
            final_video = self._assemble_final_video(video_files, project_dir / "video")
            project_data["final_video"] = final_video
            
            # Step 6: Generate SEO content
            logger.info("Step 6: Generating SEO content")
            seo_data = self._generate_seo_content(story_data, language, theme)
            project_data["seo"] = seo_data
            
            # Step 7: Auto-post to all platforms (optional)
            project_data["status"] = "completed"
            
            # Copy final video to final_videos directory with proper naming
            if final_video:
                final_video_name = f"{project_name}.mp4"
                final_video_destination = self.final_videos_dir / final_video_name
                
                try:
                    import shutil
                    shutil.copy2(final_video, final_video_destination)
                    logger.info(f"🎬 Final video saved to: {final_video_destination}")
                    project_data["final_video_path"] = str(final_video_destination)
                except Exception as e:
                    logger.warning(f"Could not copy final video: {e}")
                    project_data["final_video_path"] = final_video
            
            if auto_upload_youtube and final_video and seo_data:
                logger.info("Step 7: Auto-posting to all platforms...")
                try:
                    from browser_posting import BrowserManager
                    browser_manager = BrowserManager(self.config_manager)
                    
                    # Get the final video path (use the copied one if available)
                    video_path = project_data.get("final_video_path", final_video)
                    
                    # Generate platform-specific content
                    title = seo_data.get('title', story_data.get('title', 'Amazing Story'))
                    
                    # YouTube - Full SEO description
                    youtube_description = seo_data.get('description', 'A wonderful children\'s story.')
                    youtube_hashtags = seo_data.get('hashtags', '#story #children #education')
                    
                    # TikTok - Short catchy title with trending hashtags
                    tiktok_title = f"✨ {title[:40]}..." if len(title) > 40 else f"✨ {title}"
                    tiktok_description = "Amazing children's story! 📚✨"
                    tiktok_hashtags = "#story #kids #storytelling #education #fyp #viral #children"
                    
                    # Instagram - Visual-focused description
                    instagram_title = f"🌟 {title}"
                    instagram_description = f"A magical story for kids! 📖✨\n\nWatch and learn with us!"
                    instagram_hashtags = "#story #kids #children #education #storytelling #learning #magical"
                    
                    # Post to all platforms
                    selected_platforms = ["youtube", "tiktok", "instagram"]
                    
                    logger.info(f"🌐 Starting multi-platform posting...")
                    logger.info(f"📹 Video path: {video_path}")
                    logger.info(f"🎯 Platforms: {', '.join(selected_platforms)}")
                    
                    # Post to YouTube
                    logger.info("\n" + "="*50)
                    logger.info("🚀 POSTING TO YOUTUBE")
                    logger.info("="*50)
                    youtube_success = browser_manager.post_to_platform(
                        "youtube", video_path, title, youtube_description, youtube_hashtags
                    )
                    project_data["youtube_uploaded"] = youtube_success
                    
                    # Post to TikTok
                    logger.info("\n" + "="*50)
                    logger.info("🚀 POSTING TO TIKTOK")
                    logger.info("="*50)
                    tiktok_success = browser_manager.post_to_platform(
                        "tiktok", video_path, tiktok_title, tiktok_description, tiktok_hashtags
                    )
                    project_data["tiktok_uploaded"] = tiktok_success
                    
                    # Post to Instagram
                    logger.info("\n" + "="*50)
                    logger.info("🚀 POSTING TO INSTAGRAM")
                    logger.info("="*50)
                    instagram_success = browser_manager.post_to_platform(
                        "instagram", video_path, instagram_title, instagram_description, instagram_hashtags
                    )
                    project_data["instagram_uploaded"] = instagram_success
                    
                    # Summary
                    logger.info("\n" + "="*50)
                    logger.info("📊 MULTI-PLATFORM POSTING SUMMARY")
                    logger.info("="*50)
                    
                    total_success = sum([youtube_success, tiktok_success, instagram_success])
                    
                    youtube_status = "✅ SUCCESS" if youtube_success else "❌ FAILED"
                    tiktok_status = "✅ SUCCESS" if tiktok_success else "❌ FAILED"
                    instagram_status = "✅ SUCCESS" if instagram_success else "❌ FAILED"
                    
                    logger.info(f"YOUTUBE: {youtube_status}")
                    logger.info(f"TIKTOK: {tiktok_status}")
                    logger.info(f"INSTAGRAM: {instagram_status}")
                    logger.info(f"\n🎯 Overall Success: {total_success}/3 platforms")
                    
                    if total_success > 0:
                        logger.info("🎉 Multi-platform posting completed! Check your social media accounts.")
                    else:
                        logger.warning("⚠️ All platform uploads failed - video saved locally for manual posting")
                        
                except Exception as e:
                    logger.warning(f"⚠️ Multi-platform posting error: {e}")
                    project_data["youtube_uploaded"] = False
                    project_data["tiktok_uploaded"] = False
                    project_data["instagram_uploaded"] = False
            else:
                project_data["youtube_uploaded"] = False
                project_data["tiktok_uploaded"] = False  
                project_data["instagram_uploaded"] = False
            
            project_data["status"] = "completed"
            logger.info(f"Story generation completed: {project_name}")
            
        except Exception as e:
            logger.error(f"Story generation failed: {e}")
            project_data["status"] = "failed"
            project_data["error"] = str(e)
        
        # Save project metadata
        metadata_path = project_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(project_data, f, indent=2, ensure_ascii=False)
        
        return project_data
    
    def _generate_story_script(self, language: str, theme: str, characters: List[str] = None) -> Dict[str, Any]:
        """Generate story script using OpenAI"""
        if not OPENAI_AVAILABLE or not self.config_manager.get_api_key("openai"):
            return self._generate_fallback_story(language, theme, characters)
        
        try:
            # Create prompt based on language
            if language.lower() == "arabic":
                prompt = f"""اكتب قصة قصيرة للأطفال باللغة العربية حول موضوع "{theme}".
القصة يجب أن تكون:
- مناسبة للأطفال (عمر 3-8 سنوات)
- تحتوي على 5-7 مشاهد
- كل مشهد له عنوان ووصف وسرد
- مدة كل مشهد حوالي 15-20 ثانية
- تحمل رسالة إيجابية

{"الشخصيات: " + ", ".join(characters) if characters else ""}

أعطني النتيجة بصيغة JSON مع المفاتيح التالية:
- title: عنوان القصة
- scenes: قائمة المشاهد، كل مشهد يحتوي على:
  - title: عنوان المشهد
  - description: وصف المشهد للرسام
  - narration: النص المقروء للمشهد"""
            else:
                prompt = f"""Write a short children's story in English about "{theme}".
The story should be:
- Suitable for children (ages 3-8)
- Contain 5-7 scenes
- Each scene has a title, description, and narration
- Each scene duration about 15-20 seconds
- Carry a positive message

{"Characters: " + ", ".join(characters) if characters else ""}

Give me the result in JSON format with these keys:
- title: story title
- scenes: list of scenes, each scene contains:
  - title: scene title
  - description: scene description for illustrator
  - narration: narration text for the scene"""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative children's story writer. Always respond with valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1500
            )
            
            # Safety check for OpenAI response
            if not response or 'choices' not in response or not response['choices']:
                logger.error("No valid response from OpenAI.")
                raise ValueError("Invalid OpenAI response")
            
            # Parse response
            content = response.choices[0].message.content.strip()
            
            # Try to extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            story_data = json.loads(content)
            
            # Validate structure
            if not isinstance(story_data.get("scenes"), list):
                raise ValueError("Invalid story structure")
            
            return story_data
            
        except Exception as e:
            logger.error(f"OpenAI story generation failed: {e}")
            return self._generate_fallback_story(language, theme, characters)
    
    def _generate_fallback_story(self, language: str, theme: str, characters: List[str] = None) -> Dict[str, Any]:
        """Generate fallback story when AI is not available"""
        if language.lower() == "arabic":
            return {
                "title": f"قصة رائعة عن {theme}",
                "scenes": [
                    {
                        "title": "البداية",
                        "description": f"مشهد جميل يظهر {theme} في بيئة طبيعية",
                        "narration": f"في يوم من الأيام، كان هناك {theme} جميل يعيش في مكان رائع."
                    },
                    {
                        "title": "المغامرة",
                        "description": f"{theme} يبدأ مغامرة شيقة",
                        "narration": f"قرر {theme} أن يخرج في مغامرة جديدة ومثيرة."
                    },
                    {
                        "title": "التحدي",
                        "description": f"{theme} يواجه تحدياً",
                        "narration": f"واجه {theme} تحدياً كبيراً، لكنه لم يستسلم."
                    },
                    {
                        "title": "الحل",
                        "description": f"{theme} يجد الحل",
                        "narration": f"بذكائه وشجاعته، وجد {theme} الحل المناسب."
                    },
                    {
                        "title": "النهاية السعيدة",
                        "description": f"{theme} سعيد ومحاط بالأصدقاء",
                        "narration": f"وهكذا انتهت القصة بنهاية سعيدة، وتعلم الجميع درساً مهماً."
                    }
                ]
            }
        else:
            return {
                "title": f"Amazing Story About {theme}",
                "scenes": [
                    {
                        "title": "The Beginning",
                        "description": f"Beautiful scene showing {theme} in natural environment",
                        "narration": f"Once upon a time, there was a wonderful {theme} living in a magical place."
                    },
                    {
                        "title": "The Adventure",
                        "description": f"{theme} starts an exciting adventure",
                        "narration": f"The {theme} decided to go on a new and exciting adventure."
                    },
                    {
                        "title": "The Challenge",
                        "description": f"{theme} faces a challenge",
                        "narration": f"The {theme} faced a big challenge, but didn't give up."
                    },
                    {
                        "title": "The Solution",
                        "description": f"{theme} finds the solution",
                        "narration": f"With wisdom and courage, the {theme} found the perfect solution."
                    },
                    {
                        "title": "Happy Ending",
                        "description": f"{theme} happy and surrounded by friends",
                        "narration": f"And so the story ended happily, and everyone learned an important lesson."
                    }
                ]
            }
    
    def generate_voice_narration(self, text, output_path, voice_id=None):
        """Generate voice narration using ElevenLabs with selected voice ID"""
        if not ELEVENLABS_AVAILABLE:
            logger.warning("ElevenLabs not available, creating placeholder")
            return False
            
        try:
            # Load environment file first to ensure API key is available
            env_file = Path(__file__).parent.parent / "env.txt"
            if env_file.exists():
                with open(env_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            # Only set if not already in environment
                            if key.strip() not in os.environ:
                                os.environ[key.strip()] = value.strip()
            
            # Get API key from environment or config
            api_key = os.getenv("ELEVENLABS_API_KEY") or self.config_manager.get_api_key("elevenlabs")
            
            if not api_key:
                logger.warning("ElevenLabs API key not found")
                return False
            
            # Use provided voice_id or get from environment
            if not voice_id:
                voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
                logger.info(f"🎤 No voice_id provided, using from env: {voice_id}")
            else:
                logger.info(f"🎤 Using provided voice_id: {voice_id}")
                
            logger.info(f"🗣️ Generating voice with ID: {voice_id} for text: {text[:30]}...")
            
            # Generate audio using ElevenLabs
            import requests
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/mpeg",
                "Content-Type": "application/json",
                "xi-api-key": api_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            response = requests.post(url, json=data, headers=headers, timeout=30)
            
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"✅ ElevenLabs voice generated successfully: {output_path}")
                return True
            else:
                error_msg = response.text
                logger.error(f"❌ ElevenLabs API error (status {response.status_code}): {error_msg}")
                
                # Check for specific errors
                if "quota_exceeded" in error_msg.lower() or response.status_code == 429:
                    logger.warning("🚫 ElevenLabs quota exceeded - will use placeholder audio")
                elif "unauthorized" in error_msg.lower() or response.status_code == 401:
                    logger.warning("🔑 ElevenLabs API key invalid - will use placeholder audio") 
                elif "voice" in error_msg.lower() and "not found" in error_msg.lower():
                    logger.warning(f"🎤 Voice ID {voice_id} not found - will use placeholder audio")
                else:
                    logger.warning(f"🔧 Unexpected ElevenLabs error - will use placeholder audio")
                
                return False
                
        except requests.exceptions.Timeout:
            logger.error("❌ ElevenLabs request timeout - will use placeholder audio")
            return False
        except Exception as e:
            logger.error(f"❌ ElevenLabs generation error: {e} - will use placeholder audio")
            return False

    def _generate_voice_narration(self, scenes: List[Dict], voice_dir: Path, language: str, voice_id: str) -> List[str]:
        """Generate voice narration for all scenes"""
        voice_files = []
        
        # Log voice selection details
        if voice_id:
            logger.info(f"🎤 Voice generation will use: {voice_id}")
        else:
            logger.warning(f"⚠️ No voice ID selected, will use ElevenLabs default or fallback to placeholder")
        
        for i, scene in enumerate(scenes, 1):
            narration = scene.get('narration', '')
            filename = f"scene_{i:02d}_narration.mp3"
            filepath = voice_dir / filename
            
            logger.info(f"Generating voice for scene {i}: {narration[:50]}...")
            
            # Try ElevenLabs voice generation with selected voice
            if self.generate_voice_narration(narration, str(filepath), voice_id=voice_id):
                logger.info(f"Generated voice for scene {i}")
                voice_files.append(str(filepath))
                print(f"✅ Voice file for scene saved: {filepath}")
            else:
                # Fallback to placeholder
                logger.warning(f"Voice generation failed for scene {i}, creating placeholder")
                self._create_placeholder_audio(filepath, narration)
                voice_files.append(str(filepath))
                print(f"✅ Voice file for scene saved: {filepath}")
        
        return voice_files
    
    def _create_placeholder_audio(self, filepath: Path, text: str, duration: int = 15):
        """Create placeholder audio file using pydub for better compatibility"""
        try:
            from pydub import AudioSegment
            from pydub.generators import Sine
            
            logger.info(f"Generating placeholder audio for {filepath}")
            
            # Create a gentle tone instead of silence
            tone = Sine(440).to_audio_segment(duration=duration * 1000).apply_gain(-20)  # duration in ms
            
            # Export as MP3
            tone.export(str(filepath), format="mp3")
            logger.info(f"Created placeholder audio: {filepath}")
            return str(filepath)
            
        except ImportError:
            logger.warning("pydub not available, using MoviePy fallback")
            return self._create_placeholder_audio_moviepy(filepath, text, duration)
        except Exception as e:
            logger.error(f"Failed to create placeholder audio: {e}")
            return self._create_placeholder_audio_moviepy(filepath, text, duration)
    
    def _create_placeholder_audio_moviepy(self, filepath: Path, text: str, duration: int = 15):
        """Fallback method using MoviePy"""
        try:
            # Create a simple beep sound as placeholder
            import numpy as np
            from scipy.io.wavfile import write
            
            sample_rate = 44100
            t = np.linspace(0, duration, int(sample_rate * duration))
            frequency = 440  # A4 note
            audio_data = np.sin(2 * np.pi * frequency * t) * 0.1
            
            # Convert to WAV first, then to MP3 if possible
            wav_path = filepath.with_suffix('.wav')
            write(str(wav_path), sample_rate, (audio_data * 32767).astype(np.int16))
            
            # Try to convert to MP3
            if MOVIEPY_AVAILABLE:
                from moviepy.editor import AudioFileClip
                audio_clip = AudioFileClip(str(wav_path))
                # Fixed: Remove verbose parameter that's causing the error
                audio_clip.write_audiofile(str(filepath), logger=None)
                audio_clip.close()
                wav_path.unlink()  # Remove WAV file
            else:
                # Keep as WAV
                filepath.with_suffix('.wav').rename(filepath)
            
            return str(filepath)
                
        except Exception as e:
            logger.error(f"Failed to create placeholder audio with MoviePy: {e}")
            # Create minimal audio file
            try:
                from pydub import AudioSegment
                silence = AudioSegment.silent(duration=duration * 1000)
                silence.export(str(filepath), format="mp3")
                return str(filepath)
            except:
                # Last resort: create empty file
                filepath.touch()
                return str(filepath)
    
    def _generate_scene_images(self, scenes: List[Dict], images_dir: Path, theme: str) -> List[str]:
        """Generate images for scenes"""
        image_files = []
        
        for i, scene in enumerate(scenes, 1):
            filename = f"scene_{i:02d}_image.jpg"
            filepath = images_dir / filename
            
            try:
                # Try Leonardo.AI API if available
                if self._generate_leonardo_image(scene["description"], filepath):
                    logger.info(f"Generated Leonardo image for scene {i}")
                else:
                    # Create placeholder image
                    self._create_placeholder_image(filepath, scene["title"], scene["description"])
                    logger.info(f"Created placeholder image for scene {i}")
                
                image_files.append(str(filepath))
                
            except Exception as e:
                logger.error(f"Image generation failed for scene {i}: {e}")
                self._create_placeholder_image(filepath, scene["title"], scene["description"])
                image_files.append(str(filepath))
        
        return image_files
    
    def _generate_leonardo_image(self, description: str, filepath: Path) -> bool:
        """Generate image using Leonardo.AI API with proper implementation"""
        leonardo_key = self.config_manager.get_api_key("leonardo")
        if not leonardo_key:
            logger.info("Leonardo API key not found, using placeholder image")
            return False
        
        try:
            import requests
            import time
            
            # Leonardo.AI API - Create Generation
            headers = {
                "Authorization": f"Bearer {leonardo_key}",
                "Content-Type": "application/json"
            }
            
            # Enhanced prompt for better children's book style
            enhanced_prompt = f"{description}, children's book illustration, cartoon style, colorful, friendly, high quality, digital art, vibrant colors, suitable for kids"
            
            payload = {
                "prompt": enhanced_prompt,
                "modelId": "6bef9f1b-29cb-40c7-b9df-32b51c1f67d3",  # Leonardo Creative model
                "width": 1024,
                "height": 1024,
                "num_images": 1,
                "guidance_scale": 7,
                "num_inference_steps": 15
            }
            
            logger.info(f"Requesting Leonardo image generation for: {enhanced_prompt[:50]}...")
            
            # Create generation request
            response = requests.post(
                "https://cloud.leonardo.ai/api/rest/v1/generations",
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                generation_id = result.get("sdGenerationJob", {}).get("generationId")
                
                if generation_id:
                    # Poll for completion
                    max_attempts = 30  # 30 attempts with 2-second intervals = 1 minute max
                    for attempt in range(max_attempts):
                        time.sleep(2)
                        
                        check_response = requests.get(
                            f"https://cloud.leonardo.ai/api/rest/v1/generations/{generation_id}",
                            headers=headers,
                            timeout=10
                        )
                        
                        if check_response.status_code == 200:
                            check_result = check_response.json()
                            generated_images = check_result.get("generations_by_pk", {}).get("generated_images", [])
                            
                            if generated_images:
                                image_url = generated_images[0].get("url")
                                if image_url:
                                    # Download the image
                                    img_response = requests.get(image_url, timeout=30)
                                    if img_response.status_code == 200:
                                        with open(filepath, 'wb') as f:
                                            f.write(img_response.content)
                                        logger.info(f"Leonardo image saved: {filepath}")
                                        return True
                                    
                        elif check_response.status_code == 404:
                            # Generation not found yet, continue waiting
                            continue
                        else:
                            logger.warning(f"Leonardo check failed: {check_response.status_code}")
                            break
                    
                    logger.warning("Leonardo image generation timeout")
                else:
                    logger.error("No generation ID received from Leonardo")
            else:
                logger.error(f"Leonardo API request failed: {response.status_code} - {response.text}")
            
        except Exception as e:
            logger.error(f"Leonardo API failed: {e}")
        
        return False
    
    def _create_placeholder_image(self, filepath: Path, title: str, description: str):
        """Create placeholder image"""
        try:
            # Create a colorful placeholder image
            width, height = 1024, 1024
            
            # Generate random colors
            colors = [
                (255, 182, 193),  # Light pink
                (173, 216, 230),  # Light blue
                (144, 238, 144),  # Light green
                (255, 218, 185),  # Peach
                (221, 160, 221),  # Plum
            ]
            
            bg_color = random.choice(colors)
            
            # Create image
            img = Image.new('RGB', (width, height), bg_color)
            draw = ImageDraw.Draw(img)
            
            # Try to load a font
            try:
                font_size = 48
                font = ImageFont.truetype("arial.ttf", font_size)
            except:
                font = ImageFont.load_default()
            
            # Draw title
            text_bbox = draw.textbbox((0, 0), title, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            x = (width - text_width) // 2
            y = height // 3
            
            draw.text((x, y), title, fill=(50, 50, 50), font=font)
            
            # Draw decorative elements
            for _ in range(10):
                x1 = random.randint(0, width)
                y1 = random.randint(0, height)
                x2 = x1 + random.randint(20, 100)
                y2 = y1 + random.randint(20, 100)
                color = random.choice([(255, 255, 255, 100), (0, 0, 0, 50)])
                draw.ellipse([x1, y1, x2, y2], fill=color[:3])
            
            # Save image
            img.save(filepath, 'JPEG', quality=85)
            
        except Exception as e:
            logger.error(f"Failed to create placeholder image: {e}")
            # Create minimal image
            img = Image.new('RGB', (1024, 1024), (200, 200, 200))
            img.save(filepath, 'JPEG')
    
    def _create_animated_videos(self, image_files: List[str], voice_files: List[str], 
                              video_dir: Path) -> List[str]:
        """Create animated videos from images and voice"""
        video_files = []
        
        if not MOVIEPY_AVAILABLE:
            logger.warning("MoviePy not available - skipping video creation")
            return video_files
        
        for i, (image_path, voice_path) in enumerate(zip(image_files, voice_files), 1):
            try:
                filename = f"scene_{i:02d}_animated.mp4"
                filepath = video_dir / filename
                
                # Check if files exist and are valid
                if not voice_path or not os.path.exists(voice_path):
                    logger.error(f"Skipping scene {i} - voice file missing: {voice_path}")
                    continue
                
                if not image_path or not os.path.exists(image_path):
                    logger.error(f"Skipping scene {i} - image file missing: {image_path}")
                    continue
                
                # Load audio to get duration with error handling
                try:
                    audio_clip = AudioFileClip(voice_path)
                    duration = max(audio_clip.duration, 5)  # Minimum 5 seconds
                except Exception as audio_error:
                    logger.error(f"Skipping scene {i} - audio error: {audio_error}")
                    continue
                
                # Create image clip and directly assign audio with safe FPS
                image_clip = ImageClip(image_path, duration=duration)
                
                # Direct audio assignment - simplest approach that works
                image_clip.audio = audio_clip
                video_clip = image_clip
                
                # Write video file
                video_clip.write_videofile(
                    str(filepath),
                    fps=24,
                    logger=None,
                    codec='libx264',
                    audio_codec='aac'
                )
                
                # Clean up
                video_clip.close()
                audio_clip.close()
                image_clip.close()
                
                video_files.append(str(filepath))
                logger.info(f"Created animated video for scene {i}")
                
            except Exception as e:
                logger.error(f"Video creation failed for scene {i}: {e}")
                continue
        
        return video_files
    
    def _assemble_final_video(self, video_files: List[str], video_dir: Path) -> Optional[str]:
        """Assemble final video from scene videos"""
        if not video_files or not MOVIEPY_AVAILABLE:
            return None
        
        try:
            final_filename = "final_story.mp4"
            final_filepath = video_dir / final_filename
            
            # Load all video clips
            clips = []
            for video_path in video_files:
                if Path(video_path).exists():
                    clip = VideoFileClip(video_path)
                    clips.append(clip)
            
            if not clips:
                logger.error("No valid video clips to assemble")
                return None
            
            # Concatenate clips
            final_video = concatenate_videoclips(clips, method="compose")
            
            # Write final video
            final_video.write_videofile(
                str(final_filepath),
                fps=24,
                logger=None,
                codec='libx264',
                audio_codec='aac'
            )
            
            # Clean up
            final_video.close()
            for clip in clips:
                clip.close()
            
            logger.info("Final video assembled successfully")
            
            # Save final video to consistent output folder
            import shutil
            import os
            
            try:
                # Extract project name from the video directory path
                project_name = video_dir.parent.name if video_dir.parent.name != "output" else "final_story"
                
                # Copy final video to consistent location using centralized path
                final_output_path = self.final_videos_dir / f"{project_name}.mp4"
                shutil.copy2(str(final_filepath), str(final_output_path))
                
                logger.info(f"🎬 Final video saved to: {final_output_path}")
                print(f"\n✅ Final VIDEO FILE: {final_output_path}\n")
                
            except Exception as copy_error:
                logger.error(f"Failed to copy final video: {copy_error}")
            
            return str(final_filepath)
            
        except Exception as e:
            logger.error(f"Final video assembly failed: {e}")
            return None
    
    def _generate_seo_content(self, story_data: Dict, language: str, theme: str = "adventure") -> Dict[str, Any]:
        """Generate SEO content (title, description, hashtags)"""
        try:
            if OPENAI_AVAILABLE and self.config_manager.get_api_key("openai"):
                # Use OpenAI for SEO generation
                if language.lower() == "arabic":
                    prompt = f"""بناءً على هذه القصة: "{story_data['title']}"
اكتب محتوى SEO مناسب لليوتيوب وتيك توك وانستغرام:
- عنوان جذاب (أقل من 60 حرف)
- وصف مختصر (100-150 حرف)
- 10 هاشتاغات مناسبة باللغة العربية والإنجليزية

أعطني النتيجة بصيغة JSON."""
                else:
                    prompt = f"""Based on this story: "{story_data['title']}"
Write appropriate SEO content for YouTube, TikTok, and Instagram:
- Catchy title (under 60 characters)
- Brief description (100-150 characters)
- 10 relevant hashtags in English

Give me the result in JSON format."""
                
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an SEO expert. Always respond with valid JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7,
                    max_tokens=500
                )
                
                # Safety check for OpenAI response
                if not response or 'choices' not in response or not response['choices']:
                    logger.error("No valid response from OpenAI for SEO generation.")
                    raise ValueError("Invalid OpenAI response for SEO")
                
                content = response.choices[0].message.content.strip()
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0].strip()
                
                return json.loads(content)
                
        except Exception as e:
            logger.warning(f"SEO generation failed, using fallback. Reason: {e}")
        
        # Enhanced fallback SEO content
        project_title = story_data.get('title', 'Amazing Story')
        theme = story_data.get('theme', 'adventure')
        
        if language.lower() == "arabic":
            return {
                "title": f"{project_title} | قصة ملهمة قصيرة للأطفال",
                "description": f"هذه قصة ملهمة مولدة بالذكاء الاصطناعي للأطفال حول {theme}, مروية بأصوات وصور جميلة.",
                "hashtags": "#قصص_أطفال #حكايات #ذكاء_اصطناعي #تعليم #ترفيه #StoryTime #KidsStories #AIStory #ElevenLabs #LeonardoAI"
            }
        else:
            return {
                "title": f"{project_title} | Inspiring Short Story for Kids",
                "description": f"This is an inspiring AI-generated children's story about {theme.lower()}, narrated with beautiful voices and visuals.",
                "hashtags": "#StoryTime #KidsStories #AIStory #ElevenLabs #LeonardoAI #ChildrensStories #Educational #Bedtime #Animation #Kids"
            }
    
    def get_project_status(self, project_id: str) -> Optional[Dict[str, Any]]:
        """Get project status"""
        project_dir = self.projects_dir / project_id
        metadata_path = project_dir / "metadata.json"
        
        if metadata_path.exists():
            try:
                with open(metadata_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"Failed to load project metadata: {e}")
        
        return None
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects"""
        projects = []
        
        try:
            for project_dir in self.projects_dir.iterdir():
                if project_dir.is_dir():
                    metadata_path = project_dir / "metadata.json"
                    if metadata_path.exists():
                        try:
                            with open(metadata_path, 'r', encoding='utf-8') as f:
                                project_data = json.load(f)
                                
                                # Safety checks for project data
                                if not project_data or not isinstance(project_data, dict):
                                    logger.warning(f"Invalid project data in {project_dir.name}")
                                    continue
                                
                                # Safe extraction with fallbacks
                                story_data = project_data.get("story") or {}
                                title = "Unknown"
                                if isinstance(story_data, dict):
                                    title = story_data.get("title") or "Unknown"
                                
                                projects.append({
                                    "id": project_data.get("project_id") or f"project_{project_dir.name}",
                                    "title": title,
                                    "language": project_data.get("language") or "Unknown",
                                    "status": project_data.get("status") or "Unknown",
                                    "created_at": project_data.get("created_at") or "Unknown"
                                })
                        except Exception as e:
                            logger.error(f"Failed to read project {project_dir.name}: {e}")
                            continue
        except Exception as e:
            logger.error(f"Failed to list projects: {e}")
        
        # Sort by creation date, with safe fallback
        try:
            projects.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        except Exception as e:
            logger.error(f"Failed to sort projects: {e}")
        
        return projects 