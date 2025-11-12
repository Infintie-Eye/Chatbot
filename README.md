# 🤖 Blacifer Chatbot - Conrux AI Assistant

A professional-grade AI chatbot powered by **Google's Gemini 2.0 Flash**, featuring advanced text processing, image
analysis, and document intelligence capabilities.

![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-v1.28+-red.svg)
![Gemini 2.0 Flash](https://img.shields.io/badge/Gemini-2.0--Flash-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## 🌟 Features

### 💬 **Intelligent Text Chat**

- Context-aware conversations with **Gemini 2.0 Flash**
- Enhanced reasoning and comprehension capabilities
- Professional, knowledgeable responses
- Session-based chat history with improved context retention
- Real-time typing indicators

### 🖼️ **Advanced Image Analysis**
- Upload and analyze various image formats (JPG, PNG, GIF, BMP, WebP)
- **Enhanced vision capabilities** with Gemini 2.0 Flash
- Detailed visual descriptions and object identification
- Scene analysis, emotion detection, and content extraction
- OCR capabilities for text in images
- Improved accuracy in complex image understanding

### 📄 **Document Intelligence**
- Support for multiple file formats: TXT, CSV, JSON, PDF, DOCX, XLSX
- **Enhanced document understanding** with larger context window (8192 tokens)
- Intelligent document summarization and analysis
- Advanced data extraction and pattern recognition
- Query-based document interaction with improved accuracy
- Better handling of complex document structures

### 🎨 **Professional UI/UX**

- Modern, responsive design optimized for Gemini 2.0 Flash
- Dark/light theme support
- Mobile-friendly interface
- Accessible components
- Real-time model information and connection testing

## 🚀 What's New in Gemini 2.0 Flash

### ⚡ **Performance Improvements**

- **Faster response times** - Lightning-fast generation
- **Better reasoning** - Enhanced logical thinking capabilities
- **Improved context understanding** - Up to 8192 tokens context window
- **Enhanced vision processing** - More accurate image analysis

### 🧠 **Enhanced Capabilities**

- **Unified model architecture** - Single model for text and vision
- **Better instruction following** - More accurate task completion
- **Improved safety** - Enhanced content filtering
- **Advanced multimodal understanding** - Better text-image integration

## 🏗️ Project Structure

```
Blacifer-Chatbot/
├── 📁 src/                     # Source code
│   ├── 📁 core/               # Core functionality
│   │   ├── __init__.py
│   │   └── gemini_client.py   # Gemini 2.0 Flash API client
│   ├── 📁 ui/                 # User interface components
│   │   ├── __init__.py
│   │   └── components.py      # Reusable UI components
│   ├── 📁 utils/              # Utility functions
│   │   ├── __init__.py
│   │   └── file_processor.py  # Enhanced file processing
│   └── __init__.py
├── 📁 config/                 # Configuration
│   ├── __init__.py
│   └── settings.py            # Application settings (updated for 2.0 Flash)
├── 📁 assets/                 # Static assets
│   ├── logo.jpg               # Company logo
│   └── styles.css             # Custom CSS styles
├── 📁 logs/                   # Application logs
├── main.py                    # Main application entry point
├── requirements.txt           # Python dependencies (updated)
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
└── README.md                 # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- **Google Gemini API key** (supports 2.0 Flash models)
- Git (optional, for cloning)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/blacifer-chatbot.git
   cd blacifer-chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Gemini API key:
   # GEMINI_API_KEY=your_actual_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run main.py
   ```

6. **Open your browser**
    - Navigate to `http://localhost:8501`
    - Experience the power of Gemini 2.0 Flash! 🎉

## 🔧 Configuration

### Environment Variables

| Variable           | Description             | Default                | Required |
|--------------------|-------------------------|------------------------|----------|
| `GEMINI_API_KEY`   | Google Gemini API key   | None                   | ✅ Yes    |
| `APP_NAME`         | Application name        | "Blacifer Chatbot"     | No       |
| `COMPANY_NAME`     | Company name            | "Blacifer"             | No       |
| `TEXT_MODEL`       | Gemini text model       | "gemini-2.0-flash-exp" | No       |
| `VISION_MODEL`     | Gemini vision model     | "gemini-2.0-flash-exp" | No       |
| `MAX_TOKENS`       | Maximum response tokens | 8192                   | No       |
| `TEMPERATURE`      | Model creativity (0-1)  | 0.7                    | No       |
| `MAX_FILE_SIZE_MB` | Max upload size         | 20                     | No       |
| `LOG_LEVEL`        | Logging level           | "INFO"                 | No       |

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key"
4. Create a new project or select an existing one
5. Generate and copy your API key
6. Add it to your `.env` file

**Note:** Make sure your API key has access to Gemini 2.0 Flash models.

## 📚 Usage Guide

### Text Chat
1. Navigate to the "Chat Assistant" tab
2. Type your question in the chat input
3. Experience **faster responses** with Gemini 2.0 Flash
4. Enjoy **enhanced reasoning** and **better context understanding**

### Image Analysis
1. Go to the "Image Analysis" tab
2. Upload an image file (up to 20MB now supported)
3. Enter your analysis prompt
4. Click "Analyze Image"
5. Get **more accurate and detailed** analysis results

### Document Processing
1. Switch to the "Document Processing" tab
2. Upload a document (larger files now supported)
3. Enter your query
4. Click "Analyze Document"
5. Receive **comprehensive insights** with improved understanding

## 🛠️ Development

### Code Structure

- **`src/core/gemini_client.py`**: Updated for Gemini 2.0 Flash API interactions
- **`src/ui/components.py`**: Enhanced UI components with model info display
- **`src/utils/file_processor.py`**: Improved file processing with larger size limits
- **`config/settings.py`**: Updated configuration for 2.0 Flash models
- **`main.py`**: Enhanced application logic with new capabilities

### New Features Added

1. **Model Information Display**: Real-time model status and connection testing
2. **Enhanced Error Handling**: Better error messages and recovery
3. **Improved Performance Monitoring**: Connection testing and health checks
4. **Larger File Support**: Increased file size limits (20MB)
5. **Better Token Management**: 8192 token context window

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/
```

## 🐛 Troubleshooting

### Common Issues

1. **API Key Error**
    - Ensure your Gemini API key supports 2.0 Flash models
    - Check that the key is correctly set in `.env`
    - Verify the key is active and has sufficient quota

2. **Model Not Found Error**
    - The Gemini 2.0 Flash model might not be available in your region
    - Try using `gemini-1.5-pro` as a fallback in your `.env` file

3. **File Upload Issues**
    - Check file size (new limit: 20MB)
    - Verify file format is supported
    - Ensure proper file permissions

4. **Pydantic Import Errors**
   ```bash
   pip install pydantic-settings
   ```

### Performance Tips

- **Use the connection test** in the sidebar to verify optimal performance
- **Monitor token usage** with the enhanced model information display
- **Check logs** for performance insights and optimization suggestions

## 🤝 Contributing

We welcome contributions! The project now uses Gemini 2.0 Flash, so contributions should:

1. Leverage the enhanced capabilities of 2.0 Flash
2. Maintain backward compatibility where possible
3. Include tests for new features
4. Update documentation for new capabilities

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google**: For the powerful Gemini 2.0 Flash API
- **Streamlit**: For the amazing web app framework
- **Contributors**: To all who have contributed to this project

## 📞 Support

- **Documentation**: [Project Wiki](https://github.com/your-username/blacifer-chatbot/wiki)
- **Issues**: [GitHub Issues](https://github.com/your-username/blacifer-chatbot/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/blacifer-chatbot/discussions)
- **Email**: support@blacifer.com

---

<div align="center">

**Made with ❤️ by the Blacifer Team**

**Powered by Google Gemini 2.0 Flash**

[Website](https://www.blacifer.com) • [Documentation](https://docs.blacifer.com) • [Support](https://support.blacifer.com)

</div>