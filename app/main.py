import streamlit as st
from google import genai
from google.genai.types import  Part, Image, Content
from pathlib import Path
from PIL import Image as PILImage


# Page configuration
st.set_page_config(
    page_title="OCR with Gemma3",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description in main area
IMAGE_URL = "https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/dark/gemma-color.png"

st.markdown(f"""
    # <img src="{IMAGE_URL}" width="50" style="vertical-align: -12px;"> OCR with Gemma3
""", unsafe_allow_html=True)

# Add clear button to top right
col1, col2 = st.columns([6,1])
with col2:
    if st.button("Clear 🗑️"):
        if 'ocr_result' in st.session_state:
            del st.session_state['ocr_result']
        st.rerun()

st.markdown('<p style="margin-top: -20px;">Extract structured text from images using Gemma-3 Vision!</p>', unsafe_allow_html=True)
st.markdown("---")

# Move upload controls to sidebar
with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = PILImage.open(uploaded_file)
        st.image(image, caption="Uploaded Image")
        filename = uploaded_file.name 
        img_ext= Path(filename).suffix 
        
        if st.button("Extract Text 🔍", type="primary"):
            with st.spinner("Processing image..."):
                try:
                    img_bytes = uploaded_file.getvalue()
                    contents = Content(
                        role='user',
                        parts=[Part.from_bytes(data=img_bytes,mime_type=f"image/{img_ext[1:]}"),Part.from_text(text="Analyze the text in the provided image. Extract all readable content and present it in a structured Markdown format that is clear, concise, and well-organized. Ensure proper formatting (e.g., headings, lists, or code blocks) as necessary to represent the content effectively.")]
                    )
                    client = genai.Client()
                    response = client.models.generate_content(
                        model='gemma-3-27b-it',
                        contents=contents
                    )
                    st.session_state['ocr_result'] = response.candidates[0].content.parts[0].text
                except Exception as e:
                    st.error(f"Error processing image: {str(e)}")

# Main content area for results
if 'ocr_result' in st.session_state:
    st.markdown(st.session_state['ocr_result'])
else:
    st.info("Upload an image and click 'Extract Text' to see the results here.")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Gemma-3 Vision Model")