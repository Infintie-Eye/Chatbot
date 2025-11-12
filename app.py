"""
DEPRECATED: This file has been superseded by main.py

The Blacifer Chatbot has been completely refactored with a professional 
directory structure and upgraded to use Google's Gemini API.

Please use main.py instead:
    streamlit run main.py

For setup instructions, see README.md or run:
    python setup.py
"""

import streamlit as st
import sys


def show_migration_notice():
    """Show migration notice to users."""

    st.set_page_config(
        page_title="⚠️ Migration Notice - Blacifer Chatbot",
        page_icon="⚠️",
        layout="wide"
    )

    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 10px; margin-bottom: 2rem;">
        <h1 style="color: white; text-align: center; margin: 0;">
            ⚠️ IMPORTANT: Application Migrated
        </h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    ## 🚀 Welcome to the New Blacifer Chatbot!
    
    This application has been **completely rebuilt** with:
    
    ### ✨ New Features
    - 🧠 **Google Gemini AI** (upgraded from OpenAI)
    - 🏗️ **Professional code structure** 
    - 🎨 **Modern UI/UX design**
    - 📁 **Better file processing**
    - 🔧 **Enhanced configuration**
    - 🐛 **Improved error handling**
    
    ### 🎯 How to Use the New Version
    
    1. **Stop this application** (Ctrl+C in terminal)
    2. **Run the new version:**
       ```bash
       streamlit run main.py
       ```
    3. **First time setup:**
       ```bash
       python setup.py
       ```
    
    ### 📚 Need Help?
    - Check the **README.md** file for complete instructions
    - Visit our documentation
    - Contact support@blacifer.com
    
    ---
    
    **The old app.py file is now deprecated and will be removed in future versions.**
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("📖 **Read README.md** for setup instructions")

    with col2:
        st.success("🚀 **Run:** `streamlit run main.py`")

    with col3:
        st.warning("⚠️ **Setup:** `python setup.py`")

    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: #666;'>"
        "© 2024 Blacifer | Professional AI Chatbot v2.0"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    show_migration_notice()
