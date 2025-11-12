"""
Main application file for Blacifer Chatbot.
Professional AI assistant with Gemini 2.0 Flash integration.
"""
import streamlit as st
import logging
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from config.settings import settings, validate_settings
from src.core.gemini_client import gemini_client
from src.utils.file_processor import file_processor
from src.ui.components import (
    render_header, render_sidebar, render_chat_interface,
    render_image_analysis_tab, render_document_analysis_tab,
    render_loading_spinner, render_success_message, render_error_message,
    render_warning_message, render_info_message, render_response_container,
    render_tabs, apply_custom_css
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def initialize_app():
    """Initialize the Streamlit application."""
    # Set page configuration
    st.set_page_config(
        page_title=settings.page_title,
        page_icon=settings.page_icon,
        layout=settings.layout,
        initial_sidebar_state="expanded"
    )

    # Apply custom CSS
    apply_custom_css()

    # Validate settings
    try:
        validate_settings()
    except ValueError as e:
        st.error(f"Configuration Error: {str(e)}")
        st.stop()

    logger.info("Application initialized successfully with Gemini 2.0 Flash")

def handle_chat_interaction(prompt: str) -> str:
    """Handle chat interactions with Gemini 2.0 Flash."""
    try:
        system_instruction = """You are Conrux, a helpful AI assistant created by Blacifer, powered by Google's Gemini 2.0 Flash model. 
        You are knowledgeable, friendly, and professional. Provide accurate, comprehensive, and helpful responses 
        to user queries. Always be respectful and maintain a professional tone. Use your enhanced capabilities 
        to provide detailed and contextual responses."""

        response = gemini_client.generate_text_response(
            prompt=prompt,
            system_instruction=system_instruction
        )
        return response
    except Exception as e:
        logger.error(f"Chat interaction error: {str(e)}")
        return "I apologize, but I encountered an error while processing your request. Please try again."

def handle_image_analysis(image, prompt: str) -> str:
    """Handle image analysis with Gemini 2.0 Flash Vision."""
    try:
        system_instruction = """You are an expert image analyst powered by Gemini 2.0 Flash. Analyze the provided image 
        carefully and provide detailed, accurate descriptions based on the user's prompt. Use your enhanced 
        vision capabilities to identify objects, text, scenes, emotions, and context. Be descriptive, 
        informative, and helpful in your analysis."""

        response = gemini_client.analyze_image(
            image=image,
            prompt=prompt,
            system_instruction=system_instruction
        )
        return response
    except Exception as e:
        logger.error(f"Image analysis error: {str(e)}")
        return "I apologize, but I encountered an error while analyzing the image. Please try again."

def handle_document_processing(content: str, query: str, file_type: str) -> str:
    """Handle document processing with Gemini 2.0 Flash."""
    try:
        system_instruction = """You are a document analysis expert powered by Gemini 2.0 Flash. Analyze the provided document 
        content and answer the user's query accurately and comprehensively. Use your enhanced language understanding 
        to provide structured, helpful responses with relevant insights from the document. Extract key information, 
        summarize when appropriate, and provide actionable insights."""

        response = gemini_client.process_document(
            content=content,
            query=query,
            file_type=file_type,
            system_instruction=system_instruction
        )
        return response
    except Exception as e:
        logger.error(f"Document processing error: {str(e)}")
        return "I apologize, but I encountered an error while processing the document. Please try again."


def display_model_info():
    """Display model information in the sidebar."""
    with st.sidebar:
        with st.expander("🔧 Model Information", expanded=False):
            st.markdown("**Current Model:** Gemini 2.0 Flash")
            st.markdown(f"**Version:** {settings.app_version}")
            st.markdown(f"**Max Tokens:** {settings.max_tokens}")
            st.markdown(f"**Temperature:** {settings.temperature}")
            st.markdown(f"**Max File Size:** {settings.max_file_size_mb}MB")

            # Test connection button
            if st.button("Test Connection", key="test_connection"):
                with st.spinner("Testing connection..."):
                    test_result = gemini_client.test_connection()
                    if test_result['status'] == 'success':
                        st.success("✅ Connection successful!")
                        st.code(test_result['response_preview'])
                    else:
                        st.error(f"❌ Connection failed: {test_result['error']}")

def main():
    """Main application function."""
    # Initialize the application
    initialize_app()

    # Render header
    render_header()

    # Render sidebar
    render_sidebar()

    # Display model info
    display_model_info()

    # Main content area
    st.title(f"🤖 {settings.app_name}")
    st.markdown("### Your AI-Powered Assistant with Gemini 2.0 Flash")

    # Show enhanced capabilities
    st.info("""
    🚀 **Enhanced with Gemini 2.0 Flash:**
    • Faster response times • Improved reasoning • Better context understanding • Enhanced vision capabilities
    """)

    # Create tabs
    tab1, tab2, tab3 = render_tabs()

    # Tab 1: Chat Assistant
    with tab1:
        st.header("💬 Chat Assistant")
        st.markdown("Ask me anything! I'm powered by Gemini 2.0 Flash for enhanced conversations.")

        # Render chat interface
        prompt = render_chat_interface()

        if prompt:
            with st.chat_message("assistant"):
                with render_loading_spinner("Thinking with Gemini 2.0 Flash..."):
                    response = handle_chat_interaction(prompt)

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})

    # Tab 2: Image Analysis
    with tab2:
        uploaded_image, image_prompt, analyze_btn = render_image_analysis_tab()

        if analyze_btn:
            if uploaded_image and image_prompt:
                # Validate file
                is_valid, error_msg = file_processor.validate_file(uploaded_image)

                if not is_valid:
                    render_error_message(error_msg)
                else:
                    # Process image
                    success, image, error_msg = file_processor.process_image_file(uploaded_image)

                    if success:
                        with render_loading_spinner("Analyzing image with Gemini 2.0 Flash Vision..."):
                            response = handle_image_analysis(image, image_prompt)

                        render_response_container(response, "analysis")
                        render_success_message("Image analysis completed with enhanced vision capabilities!")
                    else:
                        render_error_message(error_msg)
            else:
                render_warning_message("Please upload an image and enter an analysis prompt.")

    # Tab 3: Document Processing
    with tab3:
        uploaded_file, file_query, analyze_btn = render_document_analysis_tab()

        if analyze_btn:
            if uploaded_file and file_query:
                # Validate file
                is_valid, error_msg = file_processor.validate_file(uploaded_file)

                if not is_valid:
                    render_error_message(error_msg)
                else:
                    # Get file info
                    file_info = file_processor.get_file_info(uploaded_file)
                    file_extension = file_info.get('extension', '')

                    if file_processor.is_text_file(file_extension):
                        # Process text file
                        success, content, error_msg = file_processor.process_text_file(uploaded_file)

                        if success:
                            with render_loading_spinner("Processing document with Gemini 2.0 Flash..."):
                                response = handle_document_processing(content, file_query, file_extension)

                            # Show file info
                            with st.expander("📋 File Information", expanded=False):
                                st.json(file_info)

                            render_response_container(response, "analysis")
                            render_success_message("Document analysis completed with enhanced understanding!")
                        else:
                            render_error_message(error_msg)
                    else:
                        render_error_message("Unsupported file type for document processing.")
            else:
                render_warning_message("Please upload a document and enter an analysis query.")

    # Footer
    st.markdown("---")
    st.markdown(
        f"<div style='text-align: center; color: #666; padding: 1rem;'>"
        f"© 2024 {settings.company_name} | {settings.app_name} v{settings.app_version} | "
        f"Powered by Google Gemini 2.0 Flash AI"
        f"</div>",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        st.error(f"An unexpected error occurred: {str(e)}")
        st.error("Please check your configuration and try again.")
