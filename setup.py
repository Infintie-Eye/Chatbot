#!/usr/bin/env python3
"""
Setup script for Blacifer Chatbot
Helps with initial project setup and configuration
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_banner():
    """Print setup banner."""
    print("=" * 60)
    print("🤖 BLACIFER CHATBOT - SETUP WIZARD")
    print("=" * 60)
    print("Welcome to the Blacifer Chatbot setup!")
    print("This script will help you get started quickly.\n")


def check_python_version():
    """Check if Python version is compatible."""
    print("🔍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} - OK\n")


def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    directories = [
        "logs",
        "assets",
        "temp",
        "uploads"
    ]

    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   Created: {directory}/")
    print("✅ Directories created successfully!\n")


def setup_environment():
    """Setup environment file."""
    print("🔧 Setting up environment configuration...")

    env_example = Path(".env.example")
    env_file = Path(".env")

    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  IMPORTANT: Please edit .env and add your Gemini API key!")
        print("   GEMINI_API_KEY=your_actual_api_key_here\n")
    elif env_file.exists():
        print("✅ .env file already exists\n")
    else:
        print("❌ .env.example not found!\n")


def install_dependencies():
    """Install Python dependencies."""
    print("📦 Installing Python dependencies...")

    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully!\n")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies!")
        print("   Please run: pip install -r requirements.txt\n")


def validate_gemini_key():
    """Validate Gemini API key setup."""
    print("🔑 Checking Gemini API key...")

    try:
        from dotenv import load_dotenv
        load_dotenv()

        api_key = os.getenv("GEMINI_API_KEY")
        if api_key and api_key != "your_gemini_api_key_here":
            print("✅ Gemini API key found in environment\n")
            return True
        else:
            print("❌ Gemini API key not configured!")
            print("   Please edit your .env file and add your API key.\n")
            return False
    except ImportError:
        print("⚠️  Cannot validate API key (python-dotenv not installed)\n")
        return False


def run_health_check():
    """Run basic health check."""
    print("🏥 Running health check...")

    try:
        # Import main modules to check for issues
        sys.path.append("src")
        from config.settings import settings
        print("✅ Configuration loaded successfully")

        from src.core.gemini_client import GeminiClient
        print("✅ Gemini client module loaded")

        from src.utils.file_processor import FileProcessor
        print("✅ File processor module loaded")

        print("✅ All core modules loaded successfully!\n")
        return True

    except Exception as e:
        print(f"❌ Health check failed: {str(e)}")
        print("   Please check your configuration and dependencies.\n")
        return False


def print_next_steps():
    """Print next steps for the user."""
    print("🎉 SETUP COMPLETE!")
    print("=" * 60)
    print("Next steps:")
    print("1. Edit your .env file and add your Gemini API key")
    print("2. Run the application: streamlit run main.py")
    print("3. Open your browser to http://localhost:8501")
    print("\nFor help and documentation:")
    print("- README.md file in this directory")
    print("- GitHub: https://github.com/your-username/blacifer-chatbot")
    print("- Support: support@blacifer.com")
    print("=" * 60)


def main():
    """Main setup function."""
    print_banner()

    # Basic checks
    check_python_version()

    # Setup steps
    create_directories()
    setup_environment()
    install_dependencies()

    # Validation
    api_key_valid = validate_gemini_key()
    health_check_passed = run_health_check()

    # Final steps
    print_next_steps()

    if not api_key_valid:
        print("\n⚠️  WARNING: API key not configured. Please update your .env file!")

    if not health_check_passed:
        print("\n⚠️  WARNING: Health check failed. Please check your setup!")
        sys.exit(1)

    print("\n🚀 Ready to launch your AI chatbot!")


if __name__ == "__main__":
    main()
