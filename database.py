import json
import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# 1. Database Connection Logic
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        try:
            # Method A: Raw JSON (Most stable)
            if "FIREBASE_JSON" in st.secrets:
                cred_dict = json.loads(st.secrets["FIREBASE_JSON"])
            
            # Method B: TOML Section (Fallback)
            elif "firebase" in st.secrets:
                cred_dict = dict(st.secrets["firebase"])
                if "private_key" in cred_dict:
                    # Fixes double-escaped newlines from copy-pasting
                    cred_dict["private_key"] = cred_dict["private_key"].replace("\\n", "\n").replace("\\\\n", "\n")
            else:
                st.error("Firebase secrets are missing in Streamlit Cloud!")
                st.stop()

            # Initialize Firebase
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)

        except Exception as e:
            st.error("🔥 Firebase Connection Error!")
            st.write(f"Details: {e}")
            st.write("Please update your Streamlit Secrets using the FIREBASE_JSON format.")
            st.stop()

    return firestore.client()

db = init_firebase()

# 2. Read Functions
def fetch_all_properties():
    docs = db.collection('properties').stream()
    return [doc.to_dict() for doc in docs]

def fetch_all_vendors():
    docs = db.collection('vendors').stream()
    return [doc.to_dict() for doc in docs]

# 3. Write Functions
def add_property(prop_data):
    try:
        db.collection('properties').add(prop_data)
        return True
    except Exception as e:
        st.error(f"Error adding property: {e}")
        return False

def add_vendor(vendor_data):
    try:
        db.collection('vendors').add(vendor_data)
        return True
    except Exception as e:
        st.error(f"Error adding vendor: {e}")
        return False
