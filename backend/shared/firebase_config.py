"""
Shared Firebase configuration
"""
import os
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Initialize Firebase
cred_path = os.getenv("FIREBASE_CREDENTIALS", "./firebase-credentials.json")

if not firebase_admin._apps:
    if os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    else:
        # Use default credentials in production
        firebase_admin.initialize_app()

# Firestore client
db = firestore.client()


def verify_token(token: str):
    """Verify Firebase ID token"""
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid token: {e}")


def get_user_id(token: str) -> str:
    """Extract user ID from token"""
    decoded = verify_token(token)
    return decoded['uid']
