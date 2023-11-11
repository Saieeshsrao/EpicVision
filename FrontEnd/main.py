import streamlit as st
from page1 import main as page1
from page2 import main as page2
from page3 import main as page3
from page4 import main as page4

st.set_page_config(page_title="EpicVision")

# Create a dictionary of page names and their respective functions
pages = {
    "Video to Frame Conversion": page1,
    "Image reconstruction": page2,
    "Face enhancement": page3,
    "Features prediction": page4,
}

# Add a sidebar for page selection
st.sidebar.title("EpicVsion")
selected_page = st.sidebar.selectbox("Go to", list(pages.keys()))

# Display the selected page
pages[selected_page]()
