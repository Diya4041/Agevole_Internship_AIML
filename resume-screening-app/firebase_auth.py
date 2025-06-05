import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin.exceptions import FirebaseError
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

class FirebaseAuth:
    def __init__(self):
        self.initialized = False
        self.initialize_firebase()

    def initialize_firebase(self):
        """Initialize Firebase with proper error handling"""
        if not firebase_admin._apps and not self.initialized:
            try:
                # Get environment variables
                project_id = os.getenv("FIREBASE_PROJECT_ID")
                private_key = os.getenv("FIREBASE_PRIVATE_KEY")
                client_email = os.getenv("FIREBASE_CLIENT_EMAIL")
                
                # Validate environment variables
                if None in (project_id, private_key, client_email):
                    missing = []
                    if project_id is None: missing.append("FIREBASE_PROJECT_ID")
                    if private_key is None: missing.append("FIREBASE_PRIVATE_KEY")
                    if client_email is None: missing.append("FIREBASE_CLIENT_EMAIL")
                    raise ValueError(f"Missing Firebase config: {', '.join(missing)}. Check your .env file")

                # Additional validation for private key
                if private_key is None or not private_key.startswith("-----BEGIN PRIVATE KEY-----"):
                    raise ValueError("Invalid private key format in .env file")

                # Format private key
                formatted_key = private_key.replace('\\n', '\n')
                
                cred = credentials.Certificate({
                    "type": "service_account",
                    "project_id": project_id,
                    "private_key": formatted_key,
                    "client_email": client_email,
                    "token_uri": "https://oauth2.googleapis.com/token"
                })
                firebase_admin.initialize_app(cred)
                self.initialized = True
                st.success("Firebase initialized successfully")
                return True
            except Exception as e:
                st.error(f"Firebase initialization failed: {str(e)}")
                st.error("Please check your .env file configuration")
                st.stop()
        return True

    def get_current_user(self):
        """Get current user from Streamlit session state"""
        return st.session_state.get('firebase_user')

    def login_with_email_and_password(self, email: str, password: str):
        try:
            # In production, use Firebase Client SDK for actual login
            user = auth.get_user_by_email(email)
            st.session_state.firebase_user = {
                'uid': user.uid,
                'email': user.email,
                'email_verified': user.email_verified,
                'name': user.display_name or email.split('@')[0]
            }
            return True
        except (auth.UserNotFoundError, ValueError, FirebaseError):
            st.error("Invalid email or password")
            return False

    def create_user(self, email: str, password: str):
        try:
            if len(password) < 6:
                st.error("Password must be at least 6 characters")
                return False
                
            user = auth.create_user(
                email=email,
                password=password,
                email_verified=False
            )
            # Send verification email
            auth.generate_email_verification_link(email)
            return True
        except auth.EmailAlreadyExistsError:
            st.error("Email already registered")
            return False
        except ValueError:
            st.error("Invalid email format")
            return False
        except FirebaseError as e:
            st.error(f"Registration failed: {str(e)}")
            return False

    def logout(self):
        """Clear user session"""
        if 'firebase_user' in st.session_state:
            del st.session_state['firebase_user']
        st.rerun()

# Initialize FirebaseAuth instance
firebase_auth = FirebaseAuth()