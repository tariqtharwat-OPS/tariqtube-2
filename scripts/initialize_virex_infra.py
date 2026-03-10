import os
from google.cloud import firestore

# Use the service account key from the legacy project
credential_path = r"d:\TariqTube\tariqtubserviceaccount.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credential_path

db = firestore.Client(project="tariqtube-production")

def init_virex_infra():
    print("Initializing Virex Engine Infrastructure on Firestore...")

    # 1. Register Workspace (Default)
    workspace_ref = db.collection("workspaces").document("virexa_main")
    workspace_ref.set({
        "name": "Virexa AI Main Workspace",
        "created_at": firestore.SERVER_TIMESTAMP,
        "status": "active"
    })

    # 2. Register ChroniQuest Project
    project_id = "chroniquest_001"
    project_ref = db.collection("projects").document(project_id)
    project_ref.set({
        "name": "ChroniQuest",
        "type": "Historical adventure / time travel exploration",
        "description": "Premium animated series following Faris and Merit through time.",
        "production_target": {
            "episode_length": "8-10 minutes",
            "style": "Cinematic Animation",
            "quality": "High-Quality Storytelling"
        },
        "languages": ["en", "ar"],
        "created_at": firestore.SERVER_TIMESTAMP,
        "workspace_id": "virexa_main"
    })

    # 3. Initialize Locale Configs for ChroniQuest
    project_ref.collection("locale_configs").document("en").set({
        "language_code": "en",
        "default_voice": "en-US-Studio-O",
        "seo_template": {
            "title": "ChroniQuest: {title}",
            "tags": ["Animation", "History", "Adventure"]
        }
    })
    
    project_ref.collection("locale_configs").document("ar").set({
        "language_code": "ar",
        "default_voice": "ar-XA-Studio-B",
        "supports_tashkeel": True,
        "seo_template": {
            "title": "ChroniQuest (Arabic): {title}",
            "tags": ["رسوم_متحركة", "تاريخ", "مغامرة"]
        }
    })

    # 4. Register Locked Assets in Project Registry
    registry_ref = project_ref.collection("registries").document("assets")
    
    registry_ref.collection("characters").document("faris").set({
        "name": "Faris",
        "role": "protagonist",
        "master_asset": "assets/characters/faris/faris_master.png",
        "age": 14,
        "heritage": "Egyptian-Italian"
    })
    
    registry_ref.collection("characters").document("merit").set({
        "name": "Merit",
        "role": "ai_guardian",
        "master_asset": "assets/characters/merit/merit_master.png"
    })
    
    registry_ref.collection("characters").document("father").set({
        "name": "Faris Father",
        "role": "archaeologist",
        "master_asset": "assets/characters/faris_family/father_master.png"
    })
    
    registry_ref.collection("characters").document("mother").set({
        "name": "Faris Mother",
        "role": "linguist",
        "master_asset": "assets/characters/faris_family/mother_master.png"
    })

    # 5. Initialize Publishing & Analytics Collections with a dummy tracker
    db.collection("publishing").document("meta").set({"last_initialized": firestore.SERVER_TIMESTAMP})
    db.collection("analytics").document("meta").set({"last_initialized": firestore.SERVER_TIMESTAMP})

    print(f"Virex Engine Infrastructure Initialized. Project ID: {project_id}")

if __name__ == "__main__":
    init_virex_infra()
