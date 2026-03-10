# 📋 TariqTube 2.0: Environment Preparation Checklist

## Google Cloud Platform Setup
- [x] Create GCP Project: `tariqtube-production`.
- [x] Enable APIs: 
    - Vertex AI (Gemini, Imagen)
    - YouTube Data API v3
    - Cloud Run
    - Cloud Firestore
    - Secret Manager
- [x] Create Service Account: `tariq-worker@tariqtube-production.iam.gserviceaccount.com`.
- [x] Configure OAuth Consent Screen (Completed).
- [x] Create Storage Bucket: `gs://tariqtube-assets-production`.
- [x] Create Firestore Database (Native Mode).
- [x] Prepare and Verify OAuth 2.0 Desktop Client and Token.

## Local Credentials
- `tariq-worker-key.json`: Service account key (ADC).
- `client_secret.json`: OAuth client ID for YouTube API.
- `token.pickle`: Local storage for YouTube API access/refresh tokens.

---
*Generated based on TariqTube 2.0 Blueprint*
