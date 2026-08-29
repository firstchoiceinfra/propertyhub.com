import streamlit as st
from views import property_page, vendor_page

st.set_page_config(page_title="PropertyHub Ecosystem", layout="wide", initial_sidebar_state="expanded")

# प्रीमियम कस्टम CSS (ब्लैक बैकग्राउंड की जगह क्लीन लुक)
st.markdown("""
    <style>
    [data-testid="stSidebar"] {
        background-color: #f4f6f9; 
        border-right: 1px solid #d1d5db;
    }
    div.stRadio > div {
        background-color: transparent;
        padding: 10px;
        border-radius: 8px;
    }
    .main-title { color: #1e3a8a; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

def show_home():
    st.markdown('<h1 class="main-title">प्रॉपर्टी हब इकोसिस्टम में आपका स्वागत है</h1>', unsafe_allow_html=True)
    st.write("प्रॉपर्टी खोजने से लेकर, घर बनाने और गृह प्रवेश तक का वन-स्टॉप सॉल्यूशन।")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("कुल प्रॉपर्टीज़", "1,250+")
    col2.metric("वेरिफाइड वेंडर्स", "340+")
    col3.metric("हैप्पी कस्टमर्स", "5,000+")

def main():
    st.sidebar.title("नेविगेशन")
    
    # सिंगल पेज राउटिंग मेनू
    menu = ["🏠 होम (Dashboard)", "🏢 प्रॉपर्टी लिस्टिंग", "🛠️ वेंडर इकोसिस्टम"]
    choice = st.sidebar.radio("मेनू चुनें:", menu)
    
    st.sidebar.divider()
    st.sidebar.info("सिंगल-पेज आर्किटेक्चर - बिना किसी फ्लिकर के तेज़ नेविगेशन।")

    # पेज राउटिंग लॉजिक
    if choice == "🏠 होम (Dashboard)":
        show_home()
    elif choice == "🏢 प्रॉपर्टी लिस्टिंग":
        property_page.show_advanced_filters()
    elif choice == "🛠️ वेंडर इकोसिस्टम":
        vendor_page.show_vendor_ecosystem()

if __name__ == "__main__":
    main()
