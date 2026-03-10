#!/usr/bin/env python3
"""
YouTube OAuth2 Upload Module
Uploads videos to personal YouTube channel using OAuth2 authentication
"""

import os
import json
import pickle
from pathlib import Path
from typing import Dict, Any, Optional, List
import google.auth
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# OAuth2 configuration
SCOPES = [
    'https://www.googleapis.com/auth/youtube.upload',
    'https://www.googleapis.com/auth/youtube'
]

# File paths
CREDENTIALS_FILE = Path("D:/TariqTube/tariqtube_next/posting/client_secret.json")
TOKEN_FILE = Path(__file__).parent / "token.pickle"

class YouTubeOAuth2Uploader:
    """YouTube uploader using OAuth2 authentication for personal channel"""
    
    def __init__(self):
        self.youtube = None
        self.credentials = None
        self._authenticated = False
        
    def authenticate(self) -> bool:
        """Authenticate using OAuth2 with token caching"""
        try:
            logger.info("🔐 Starting OAuth2 authentication...")
            
            # Check if we have valid cached credentials
            if TOKEN_FILE.exists():
                logger.info("📁 Found cached token, loading...")
                with open(TOKEN_FILE, 'rb') as token:
                    self.credentials = pickle.load(token)
            
            # If no valid credentials available, let the user log in
            if not self.credentials or not self.credentials.valid:
                if self.credentials and self.credentials.expired and self.credentials.refresh_token:
                    logger.info("🔄 Refreshing expired token...")
                    self.credentials.refresh(Request())
                else:
                    if not CREDENTIALS_FILE.exists():
                        logger.error(f"❌ OAuth2 credentials file not found: {CREDENTIALS_FILE}")
                        return False
                    
                    logger.info("🌐 Opening browser for OAuth2 consent...")
                    logger.info("💡 If you get an access_denied error, please:")
                    logger.info("   1. Go to Google Cloud Console")
                    logger.info("   2. Navigate to APIs & Services > OAuth consent screen")
                    logger.info("   3. Add your email as a test user")
                    logger.info("   4. Or create a new OAuth2 app with a different name")
                    logger.info("   5. Make sure YouTube Data API v3 is enabled")
                    
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(CREDENTIALS_FILE), SCOPES)
                    # Use port 0 to let system choose available port
                    self.credentials = flow.run_local_server(port=0)
                
                # Save the credentials for the next run
                logger.info("💾 Saving token for future use...")
                with open(TOKEN_FILE, 'wb') as token:
                    pickle.dump(self.credentials, token)
            
            # Build the YouTube service
            self.youtube = build('youtube', 'v3', credentials=self.credentials)
            self._authenticated = True
            logger.info("✅ OAuth2 authentication successful")
            return True
            
        except Exception as e:
            logger.error(f"❌ OAuth2 authentication failed: {e}")
            return False
    
    def get_channel_info(self) -> Optional[Dict[str, Any]]:
        """Get information about the authenticated user's channel"""
        try:
            if not self._authenticated or not self.youtube:
                logger.error("YouTube service not initialized")
                return None
            
            request = self.youtube.channels().list(
                part="snippet,contentDetails,statistics",
                mine=True
            )
            response = request.execute()
            
            if 'items' in response and response['items']:
                channel = response['items'][0]
                logger.info(f"📺 Channel: {channel['snippet']['title']}")
                logger.info(f"📊 Subscribers: {channel['statistics'].get('subscriberCount', 'Hidden')}")
                return channel
            else:
                logger.warning("No channels found for this account")
                return None
                
        except Exception as e:
            logger.error(f"Error getting channel info: {e}")
            return None
    
    def upload_video(self, 
                    video_path: str, 
                    title: str, 
                    description: str = "", 
                    privacy: str = "public",
                    tags: List[str] = None,
                    category_id: str = "22",  # People & Blogs
                    made_for_kids: bool = False) -> Dict[str, Any]:
        """
        Upload a video to YouTube
        
        Args:
            video_path: Path to the video file
            title: Video title
            description: Video description
            privacy: private, unlisted, or public
            tags: List of tags
            category_id: YouTube category ID
            made_for_kids: Whether the video is made for kids
            
        Returns:
            Dict with success, video_id, url, and error (if any)
        """
        try:
            if not self._authenticated or not self.youtube:
                logger.error("YouTube service not initialized")
                return {'success': False, 'error': 'Not authenticated'}
            
            # Validate video file
            video_file = Path(video_path)
            if not video_file.exists():
                logger.error(f"Video file not found: {video_path}")
                return {'success': False, 'error': f'Video file not found: {video_path}'}
            
            logger.info(f"🚀 Starting upload: {video_file.name}")
            logger.info(f"📝 Title: {title}")
            logger.info(f"🔒 Privacy: {privacy}")
            
            # Prepare video metadata
            body = {
                'snippet': {
                    'title': title,
                    'description': description,
                    'tags': tags or [],
                    'categoryId': category_id,
                    'madeForKids': made_for_kids
                },
                'status': {
                    'privacyStatus': privacy,
                    'selfDeclaredMadeForKids': made_for_kids
                }
            }
            
            # Create media upload object
            media = MediaFileUpload(
                str(video_file),
                chunksize=1024*1024,  # 1MB chunks
                resumable=True
            )
            
            # Start upload
            request = self.youtube.videos().insert(
                part=",".join(body.keys()),
                body=body,
                media_body=media
            )
            
            # Monitor upload progress
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = int(status.progress() * 100)
                    logger.info(f"📤 Uploaded {progress}%")
            
            video_id = response['id']
            video_url = f"https://www.youtube.com/watch?v={video_id}"
            
            logger.info(f"✅ Upload successful!")
            logger.info(f"🎬 Video ID: {video_id}")
            logger.info(f"🔗 Video URL: {video_url}")
            
            return {
                'success': True,
                'video_id': video_id,
                'url': video_url
            }
            
        except HttpError as e:
            logger.error(f"❌ HTTP Error during upload: {e}")
            error_details = e.error_details if hasattr(e, 'error_details') else str(e)
            logger.error(f"🔍 Error details: {error_details}")
            return {'success': False, 'error': str(e)}
            
        except Exception as e:
            logger.error(f"❌ Upload error: {e}")
            return {'success': False, 'error': str(e)}

def upload_video(video_path: str, 
                title: str, 
                description: str = "", 
                privacy: str = "public", 
                tags: List[str] = None) -> str:
    """
    Convenience function for uploading a video
    
    Args:
        video_path: Path to video file
        title: Video title
        description: Video description
        privacy: private, unlisted, or public
        tags: List of tags
        
    Returns:
        YouTube video URL if successful, error message if failed
    """
    logger.info("🎬 Starting YouTube video upload...")
    
    uploader = YouTubeOAuth2Uploader()
    
    if not uploader.authenticate():
        error_msg = "Authentication failed"
        logger.error(f"❌ {error_msg}")
        return error_msg
    
    result = uploader.upload_video(
        video_path=video_path,
        title=title,
        description=description,
        privacy=privacy,
        tags=tags
    )
    
    if result['success']:
        logger.info("🎉 Upload completed successfully!")
        return result['url']
    else:
        error_msg = result.get('error', 'Unknown error')
        logger.error(f"❌ Upload failed: {error_msg}")
        return f"Upload failed: {error_msg}"

if __name__ == "__main__":
    # Test the uploader
    print("🧪 Testing YouTube OAuth2 Uploader")
    print("=" * 40)
    
    uploader = YouTubeOAuth2Uploader()
    
    if uploader.authenticate():
        print("✅ Authentication successful!")
        
        # Get channel info
        channel = uploader.get_channel_info()
        if channel:
            print(f"📺 Channel: {channel['snippet']['title']}")
        else:
            print("⚠️ No channel found")
    else:
        print("❌ Authentication failed") 