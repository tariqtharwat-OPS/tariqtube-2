import os
from google.cloud import firestore

# Use the service account key
credential_path = r"d:\TariqTube\tariqtubserviceaccount.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

db = firestore.Client(project="tariqtube-production")

def finalize_chroniquest_registration():
    print("Finalizing ChroniQuest Series Registration (Step 7)...")
    
    project_id = "chroniquest_001"
    project_ref = db.collection("projects").document(project_id)
    
    # 1. Series Entry (Season 1)
    series_id = "chroniquest_s1"
    series_ref = project_ref.collection("series").document(series_id)
    series_ref.set({
        "title": "Season 1: The Sands of Time",
        "total_episodes": 10,
        "current_episode_index": 0,
        "status": "planned",
        "created_at": firestore.SERVER_TIMESTAMP
    })
    
    # 2. Episode 01 Initialization (Episodic Tracking)
    episode_id = "ep001"
    episode_ref = series_ref.collection("episodes").document(episode_id)
    episode_ref.set({
        "episode_number": 1,
        "title": "The Awakening of Merit",
        "status": "imported", # Imported -> Prepared -> Generated -> Approved -> Published
        "imported_at": firestore.SERVER_TIMESTAMP,
        "visual_master_path": None,
        "next_episode_pointer": "ep002",
        "chapter": 1,
        "season": 1
    })
    
    # 3. Language Variants for Ep 01
    import datetime
    locales = ["en", "ar"]
    for locale in locales:
        variant_ref = episode_ref.collection("variants").document(locale)
        variant_ref.set({
            "locale": locale,
            "status": "pending_generation",
            "review_status": "pending_review",
            "revision_history": [
                {
                    "revision_id": 1,
                    "updated_at": datetime.datetime.now(),
                    "change_reason": "Initial Ingestion",
                    "active": True
                }
            ],
            "metadata": {
                "title": None,
                "description": None,
                "tags": []
            },
            "publishing_results": {
                "youtube_id": None,
                "tiktok_id": None
            }
        })
    
    # 4. Job Tracking (Pipeline Observability)
    job_ref = db.collection("jobs").document("job_init_ep001")
    job_ref.set({
        "type": "pre_production_preflight",
        "project_id": project_id,
        "episode_id": episode_id,
        "status": "completed",
        "results": "Series, Episode, and Variants initialized in Firestore."
    })

    # 5. Publishing Route (Example for YT-English)
    route_ref = db.collection("publishing").document("route_cq_en_yt")
    route_ref.set({
        "project_id": project_id,
        "lang_code": "en",
        "platform": "youtube",
        "channel_id": "UC_TEST_EN", # Placeholder
        "schedule_pattern": "weekly",
        "timezone": "UTC"
    })

    print(f"ChroniQuest Season 1, Episode 01, and Language Variants registered successfully.")

if __name__ == "__main__":
    finalize_chroniquest_registration()
