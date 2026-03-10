import logging
import os
from pathlib import Path
from lite_stories.google_story_pipeline import GoogleStoryPipeline

# Configure logging
logging.basicConfig(level=logging.INFO)

def test_pipeline_with_upload():
    print("STARTING GOOGLE-NATIVE PIPELINE + UPLOAD TEST")
    print("=" * 50)
    
    pipeline = GoogleStoryPipeline()
    
    # Simple theme
    theme = "A small robot finds a flower"
    
    try:
        # We'll use 2 scenes to be quick and save quota
        result = pipeline.run_pipeline(
            theme=theme, 
            language="English", 
            voice_name="en-US-Studio-O", 
            scenes_count=2,
            auto_upload=True
        )
        
        print("\n" + "=" * 50)
        print(f"SUCCESS! Project ID: {result['project_id']}")
        print(f"Final Video: {result['video']}")
        
        youtube_res = result.get('youtube')
        if youtube_res and youtube_res.get('success'):
            print(f"YouTube Upload: SUCCESS!")
            print(f"Video URL: https://www.youtube.com/watch?v={youtube_res.get('video_id')}")
        else:
            print(f"YouTube Upload: FAILED - {youtube_res.get('error')}")
            
        print("=" * 50)
    except Exception as e:
        print(f"\nPIPELINE TEST FAILED: {e}")

if __name__ == "__main__":
    test_pipeline_with_upload()
