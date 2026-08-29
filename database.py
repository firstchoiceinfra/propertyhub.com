import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st

# 1. Database Connection Logic
@st.cache_resource
def init_firebase():
    if not firebase_admin._apps:
        # Fetch secrets and convert to a standard Python dictionary
        firebase_secrets = dict(st.secrets["firebase"])
        
        # CRITICAL FIX: Ensures newlines in the private key are parsed correctly
        firebase_secrets["private_key"] = firebase_secrets["private_key"].replace("\\n", "\n")
        
        # Initialize credentials
        cred = credentials.Certificate(firebase_secrets)
        firebase_admin.initialize_app(cred)
        
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
