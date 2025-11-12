# 🚀 Quick Setup Guide - Blacifer Chatbot (Gemini 2.0 Flash)

## 📋 Prerequisites

- Python 3.8+ installed
- **Google Gemini API key** (with 2.0 Flash access)
- Git (optional, for cloning)

## ⚡ Quick Start (5 minutes)

### 1. Get Your Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with Google account
3. Click "Get API Key" → Create new project
4. **Important:** Ensure access to Gemini 2.0 Flash models
5. Copy your API key

### 2. Setup Environment
```bash
# Create .env file
copy .env.example .env

# Edit .env file and add your API key:
# GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Install Dependencies
```bash
# Install required packages (includes pydantic-settings)
pip install -r requirements.txt
```

### 4. Run the Application
```bash
# Start the chatbot with Gemini 2.0 Flash
streamlit run main.py
```

### 5. Open Browser
- Go to: `http://localhost:8501`
- Experience **Gemini 2.0 Flash** power! 🎉

## 🛠️ Automated Setup (Recommended)

Run the setup script for automatic configuration:
```bash
python setup.py
```

This will:
- ✅ Check Python version
- ✅ Create necessary directories
- ✅ Setup environment file
- ✅ Install dependencies (including pydantic-settings)
- ✅ Validate Gemini 2.0 Flash configuration
- ✅ Run enhanced health checks

## 📁 Project Structure Overview

```
Blacifer-Chatbot/
├── main.py              # ← Main application (USE THIS) - Gemini 2.0 Flash
├── app.py               # ← Old version (deprecated)
├── .env                 # ← Your API keys (create from .env.example)
├── requirements.txt     # ← Dependencies (updated for 2.0 Flash)
├── setup.py            # ← Setup script
├── 📁 src/             # ← Source code
│   ├── core/           # ← Gemini 2.0 Flash AI client
│   ├── ui/             # ← Enhanced interface components  
│   └── utils/          # ← Improved file processing (20MB limit)
├── 📁 config/          # ← Settings (updated for 2.0 Flash)
├── 📁 assets/          # ← Images, CSS
└── 📁 logs/            # ← Application logs
```

## 🆘 Common Issues

### ❌ "Module not found" errors
```bash
pip install -r requirements.txt
```

### ❌ "BaseSettings import error"

```bash
pip install pydantic-settings
```

### ❌ "API key not configured"
- Check your `.env` file exists
- Verify `GEMINI_API_KEY=your_actual_key`
- **Ensure your key has Gemini 2.0 Flash access**

### ❌ "Model not found" error

- Your API key might not have 2.0 Flash access yet
- Try changing `.env` to use: `TEXT_MODEL=gemini-1.5-pro`

### ❌ "Port already in use"
```bash
streamlit run main.py --server.port 8502
```

### ❌ File upload issues

- Check file size < **20MB** (increased limit)
- Use supported formats: TXT, PDF, CSV, JSON, DOCX, XLSX, JPG, PNG

## 🚀 What's New in 2.0 Flash

### ⚡ **Performance Upgrades**

- **Faster responses** - Lightning-quick generation
- **Better reasoning** - Enhanced logical capabilities
- **8192 token context** - Larger document processing
- **Improved vision** - More accurate image analysis

### 🔧 **Technical Improvements**

- **Unified model** - Single model for text + vision
- **Enhanced safety** - Better content filtering
- **Connection testing** - Real-time status monitoring
- **Better error handling** - Improved user experience

### 🎯 **Usage Tips**

- Use the **connection test** in sidebar to verify performance
- Check **model information** for real-time status
- Enjoy **faster image analysis** with enhanced vision
- Process **larger documents** with 8192 token context

## 📞 Need Help?

- 📖 **Full Documentation**: `README.md` (updated for 2.0 Flash)
- 🐛 **Issues**: Create GitHub issue
- 💬 **Support**: support@blacifer.com

## 🧪 Testing Your Setup

After starting the app, test these features:

1. **Text Chat**: Ask a complex question - notice faster responses
2. **Image Analysis**: Upload an image - see enhanced vision capabilities
3. **Document Processing**: Upload a large file - experience better understanding
4. **Connection Test**: Use sidebar button to verify 2.0 Flash connection

---

**🎯 Goal**: Experience Gemini 2.0 Flash power in under 5 minutes!

**✅ Success**: When you see the enhanced Streamlit interface with 2.0 Flash features at `http://localhost:8501`

**🚀 Bonus**: Test the connection button in the sidebar to confirm you're using Gemini 2.0 Flash!