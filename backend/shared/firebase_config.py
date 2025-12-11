"""
Shared Firebase configuration (Optional)
Firebase is used for real-time updates but is NOT required for basic functionality
"""
import os

# Try to import Firebase, but don't fail if not available
try:
    import firebase_admin
    from firebase_admin import credentials, firestore, auth
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False
    print("⚠️  Firebase not available - real-time features disabled")

# Initialize Firebase only if available and configured
db = None

if FIREBASE_AVAILABLE:
    cred_path = os.getenv("FIREBASE_CREDENTIALS", "./firebase-credentials.json")

    if not firebase_admin._apps:
        try:
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                db = firestore.client()
                print("✅ Firebase initialized successfully")
            else:
                print("⚠️  Firebase credentials not found - running without Firebase")
        except Exception as e:
            print(f"⚠️  Firebase initialization failed: {e}")
            print("   System will work without real-time features")


def verify_token(token: str):
    """Verify Firebase ID token"""
    if not FIREBASE_AVAILABLE or not db:
        raise ValueError("Firebase not configured")

    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise ValueError(f"Invalid token: {e}")


def get_user_id(token: str) -> str:
    """Extract user ID from token"""
    decoded = verify_token(token)
    return decoded['uid']
