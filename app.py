import streamlit as st
import openai as oai
from PIL import Image
import io
import base64
import logging
from typing import Optional, Dict, Any
from streamlit_navigation_bar import st_navbar

# Secure API key handling
if "OPENAI_API_KEY" in st.secrets:
    oai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    raise ValueError("Missing OpenAI API key in Streamlit secrets")

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Function to interact with OpenAI
def chat_with_openai(prompt, uploaded_content):
    try:
        response = oai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"File content:\n{uploaded_content}"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"
@st.cache_data(show_spinner=False, max_entries=100)
def handle_api_call(messages: list, model: str = "gpt-4") -> Optional[str]:
    """Handle OpenAI API calls with error handling and caching."""
    try:
        response = oai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1500
        )
        return response.choices[0].message.content
    except oai.APIConnectionError as e:
        logger.error(f"API Connection Error: {str(e)}")
        return "Connection error. Please check your internet connection."
    except oai.RateLimitError as e:
        logger.error(f"Rate Limit Exceeded: {str(e)}")
        return "API rate limit exceeded. Please try again later."
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        return f"An error occurred: {str(e)}"
def setup_sidebar():
    # Sidebar content for Blacifer chatbot
    st.sidebar.image("logo.jpg", width=150)  # Replace with your logo image URL
    st.sidebar.title("Blacifer Chatbot")
    st.sidebar.markdown("Welcome to Blacifer's support chatbot! Are there any other products from our company that you would like to use?")

    # Section with options
    st.sidebar.subheader("Quick Links")
    st.sidebar.markdown("[Home](https://www.blacifer.com)")  # Your homepage link
    st.sidebar.markdown("[Support](https://www.blacifer.com/support)")  # Link to support page
    st.sidebar.markdown("[FAQ](https://www.blacifer.com/faq)")  # Link to FAQ section

    # Optional: Add a contact form or quick input
    st.sidebar.subheader("Contact Us")
    contact_form = st.sidebar.text_area("Feedback or questions", "")
    if st.sidebar.button("Send"):
        st.sidebar.write("Thank you for reaching out! We will get back to you soon.")
def render_chat_interface():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input and processing
    if prompt := st.chat_input("How may I assist you today?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                response = process_text(prompt)
                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
def process_text(prompt: str, context: str = "") -> str:
    """Process text prompts with optional context."""
    messages = [{"role": "user", "content": prompt}]
    if context:
        messages.insert(0, {"role": "system", "content": context})
    return handle_api_call(messages)
def process_image(prompt: str, image: Image.Image) -> str:
    """Process image with prompt using base64 encoding."""
    try:
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
        
        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_str}"}}
            ]
        }]
        return handle_api_call(messages, model="gpt-4-vision-preview")
    except Exception as e:
        logger.error(f"Image Processing Error: {str(e)}")
        return f"Image processing failed: {str(e)}"

def process_file(file, user_query: str) -> str:
    """Process uploaded files with context-aware analysis."""
    file_content = ""
    try:
        if file.name.endswith('.txt'):
            file_content = file.read().decode("utf-8")
        elif file.name.endswith('.csv'):
            import pandas as pd
            df = pd.read_csv(file)
            file_content = df.to_csv(index=False)
        elif file.name.endswith('.json'):
            import json
            file_content = json.dumps(json.load(file), indent=2)
        elif file.name.endswith('.pdf'):
            import PyPDF2
            reader = PyPDF2.PdfReader(file)
            file_content = "\n".join([page.extract_text() for page in reader.pages])
        
        messages = [
            {"role": "system", "content": "Analyze this file content:"},
            {"role": "user", "content": f"File content:\n{file_content}"},
            {"role": "user", "content": user_query}
        ]
        return handle_api_call(messages)
    except Exception as e:
        logger.error(f"File Processing Error: {str(e)}")
        return f"File processing failed: {str(e)}"




# Title and logo of the app
st.set_page_config(page_title="Cornux", page_icon="logo.jpg")


# Custom CSS for styling of the entire app
# Function to load CSS from a file
def load_css(file_name):
    
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
load_css("stylepage.css")


# Custom CSS for styling the sidebar
# Function to load CSS from a file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
load_css("stylesidebar.css")


# Custom CSS for styling the navigation bar
# Function to load CSS from a file
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
load_css("navbar.css")


# Top Navigation Bar
st.markdown(f"""
    <div class='nav-bar'>
        <span class='company-name'>Blacifer</span>
        <button onclick="window.location.href='#'">Home</button>
        <button onclick="window.location.href='#'">Services</button>
        <button onclick="window.location.href='#'">Pricing</button>
        <button onclick="window.location.href='#'">Contact</button>
    </div>
""", unsafe_allow_html=True)






def main():    
    setup_sidebar()
    
    # Custom CSS for styling buttons
    st.markdown("""
        <style>
        .stButton > button {
            color: white; /* Change text color */
            background-color: black; /* Change button background color */
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton > button:hover {
            background-color: black; /* Change background color on hover */
        }
        </style>
        """, unsafe_allow_html=True)
    # Main content area
    st.title("Welcome to Blacifer")
    st.write("Your trusted partner for outsourcing chatbot services.")
    st.title("Conrux: Your Personal Assistant")
    
    tab1, tab2, tab3 = st.tabs(["Chat Assistant", "Image Analysis", "File Processing"])
    
    with tab1:
        st.header("Query Intelligence")
        render_chat_interface()
    
    with tab2:
        st.header("Visual Analysis System")
        uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        image_prompt = st.text_area("Image Analysis Prompt", height=100)
        
        if st.button("Analyze Image"):
            if uploaded_image and image_prompt:
                with st.spinner("Processing image..."):
                    img = Image.open(uploaded_image)
                    response = process_image(image_prompt, img)
                    st.image(img, width=300)
                    st.markdown(f"**Analysis:**\n{response}")
            else:
                st.warning("Please upload an image and enter a prompt")
    
    with tab3:
        st.header("Document Intelligence")
        uploaded_file = st.file_uploader("Upload Document", type=["txt", "csv", "pdf", "json"])
        file_query = st.text_area("Document Analysis Query", height=100)
        
        if st.button("Analyze Document"):
            if uploaded_file and file_query:
                with st.spinner("Analyzing document..."):
                    response = process_file(uploaded_file, file_query)
                    st.markdown(f"**Analysis:**\n{response}")
            else:
                st.warning("Please upload a file and enter a query")

if __name__ == "__main__":
    main()