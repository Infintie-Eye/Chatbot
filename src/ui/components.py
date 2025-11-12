"""
Reusable UI components for the Streamlit interface.
"""
import streamlit as st
from typing import Optional, List, Dict, Any
from config.settings import settings


def render_header():
    """Render the application header with navigation."""
    st.markdown(f"""
        <div class="header-container">
            <div class="nav-bar">
                <div class="nav-left">
                    <img src="assets/logo.jpg" alt="Logo" class="nav-logo">
                    <span class="company-name">{settings.company_name}</span>
                </div>
                <div class="nav-right">
                    <a href="#" class="nav-button">Home</a>
                    <a href="#" class="nav-button">Services</a>
                    <a href="#" class="nav-button">Pricing</a>
                    <a href="#" class="nav-button">Contact</a>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with company information and quick links."""
    with st.sidebar:
        # Company logo and title
        try:
            st.image("assets/logo.jpg", width=150)
        except:
            st.write("🤖")  # Fallback if logo is not found

        st.title(f"{settings.company_name} Assistant")
        st.markdown("Welcome to our AI-powered assistant! How can I help you today?")

        # Quick links section
        st.subheader("🔗 Quick Links")
        st.markdown("""
        - [🏠 Home](https://www.blacifer.com)
        - [🛠️ Support](https://www.blacifer.com/support)
        - [❓ FAQ](https://www.blacifer.com/faq)
        - [📧 Contact](https://www.blacifer.com/contact)
        """)

        # Features section
        st.subheader("✨ Features")
        st.markdown("""
        - 💬 **Text Chat**: Ask any question
        - 🖼️ **Image Analysis**: Upload and analyze images
        - 📄 **Document Processing**: Analyze various file types
        - 🔍 **Smart Search**: Context-aware responses
        """)

        # Contact form
        with st.expander("💬 Feedback", expanded=False):
            feedback = st.text_area("Your feedback or questions:", placeholder="Share your thoughts...")
            if st.button("Send Feedback", key="feedback_btn"):
                if feedback.strip():
                    st.success("Thank you for your feedback! We'll get back to you soon.")
                    # Here you could implement actual feedback collection
                else:
                    st.warning("Please enter your feedback before sending.")


def render_chat_interface():
    """Render the main chat interface."""
    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat container
    chat_container = st.container()

    with chat_container:
        # Display chat history
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                if message["role"] == "assistant":
                    st.markdown(message["content"])
                else:
                    st.write(message["content"])

        # Input area
        if prompt := st.chat_input("Type your message here..."):
            # Add user message to session state
            st.session_state.messages.append({"role": "user", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.write(prompt)

            return prompt

    return None


def render_image_analysis_tab():
    """Render the image analysis tab interface."""
    st.header("🖼️ Image Analysis")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Upload Image")
        uploaded_image = st.file_uploader(
            "Choose an image file",
            type=settings.supported_image_formats,
            help=f"Supported formats: {', '.join(settings.supported_image_formats)}"
        )

        if uploaded_image:
            st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    with col2:
        st.subheader("Analysis Prompt")
        image_prompt = st.text_area(
            "What would you like to know about this image?",
            placeholder="Describe what you see, identify objects, analyze the scene...",
            height=200
        )

        analyze_btn = st.button("🔍 Analyze Image", type="primary")

    return uploaded_image, image_prompt, analyze_btn


def render_document_analysis_tab():
    """Render the document analysis tab interface."""
    st.header("📄 Document Analysis")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Upload Document")
        uploaded_file = st.file_uploader(
            "Choose a document file",
            type=settings.supported_text_formats,
            help=f"Supported formats: {', '.join(settings.supported_text_formats)}"
        )

        if uploaded_file:
            file_details = {
                "Name": uploaded_file.name,
                "Size": f"{uploaded_file.size / 1024:.2f} KB",
                "Type": uploaded_file.type if hasattr(uploaded_file, 'type') else 'Unknown'
            }
            st.json(file_details)

    with col2:
        st.subheader("Analysis Query")
        file_query = st.text_area(
            "What would you like to know about this document?",
            placeholder="Summarize the content, extract key information, analyze data...",
            height=200
        )

        analyze_btn = st.button("🔍 Analyze Document", type="primary")

    return uploaded_file, file_query, analyze_btn


def render_loading_spinner(message: str = "Processing..."):
    """Render a loading spinner with custom message."""
    return st.spinner(message)


def render_success_message(message: str):
    """Render a success message."""
    st.success(f"✅ {message}")


def render_error_message(message: str):
    """Render an error message."""
    st.error(f"❌ {message}")


def render_warning_message(message: str):
    """Render a warning message."""
    st.warning(f"⚠️ {message}")


def render_info_message(message: str):
    """Render an info message."""
    st.info(f"ℹ️ {message}")


def render_response_container(response: str, response_type: str = "text"):
    """Render response in a formatted container."""
    with st.container():
        if response_type == "text":
            st.markdown("### 🤖 Assistant Response")
            st.markdown(response)
        elif response_type == "analysis":
            st.markdown("### 📊 Analysis Results")
            st.markdown(response)
        elif response_type == "error":
            st.markdown("### ❌ Error")
            st.error(response)


def render_tabs():
    """Render the main application tabs."""
    return st.tabs(["💬 Chat Assistant", "🖼️ Image Analysis", "📄 Document Processing"])


def render_metrics(metrics: Dict[str, Any]):
    """Render metrics in columns."""
    if not metrics:
        return

    cols = st.columns(len(metrics))

    for i, (key, value) in enumerate(metrics.items()):
        with cols[i]:
            st.metric(label=key, value=value)


def render_file_info(file_info: Dict[str, Any]):
    """Render file information."""
    if file_info:
        st.subheader("📋 File Information")
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Name:** {file_info.get('name', 'Unknown')}")
            st.write(f"**Size:** {file_info.get('size_mb', 0)} MB")

        with col2:
            st.write(f"**Type:** {file_info.get('extension', 'Unknown').upper()}")
            st.write(f"**Format:** {file_info.get('type', 'Unknown')}")


def apply_custom_css():
    """Apply custom CSS styling."""
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding-top: 2rem;
    }
    
    /* Header styling */
    .header-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem 0;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    
    .nav-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 2rem;
    }
    
    .nav-left {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .nav-logo {
        width: 40px;
        height: 40px;
        border-radius: 50%;
    }
    
    .company-name {
        font-size: 1.5rem;
        font-weight: bold;
        color: white;
    }
    
    .nav-right {
        display: flex;
        gap: 1rem;
    }
    
    .nav-button {
        color: white;
        text-decoration: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    
    .nav-button:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Chat styling */
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* File uploader styling */
    .uploadedFile {
        border: 2px dashed #667eea;
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
    }
    
    /* Metrics styling */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* Success message styling */
    .success {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 0.75rem 1.25rem;
        border-radius: 0.375rem;
    }
    
    /* Error message styling */
    .error {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 0.75rem 1.25rem;
        border-radius: 0.375rem;
    }
    </style>
    """, unsafe_allow_html=True)
