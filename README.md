# Blacifer Chatbot - Conrux

This project is a Streamlit-based chatbot application designed to provide intelligent assistance through text, image, and document analysis. The chatbot leverages OpenAI's GPT-4 and GPT-4 Vision models to process user queries, analyze images, and interpret document content.

## Features

### 1. **Chat Assistant**
- **Purpose**: Provides text-based conversational support.
- **Functionality**:
  - Users can input text queries, and the chatbot responds with intelligent answers.
  - Supports context-aware conversations by maintaining a session state.

### 2. **Image Analysis**
- **Purpose**: Analyzes uploaded images based on user prompts.
- **Functionality**:
  - Users can upload images (JPG, JPEG, PNG) and provide a prompt for analysis.
  - The chatbot processes the image and provides a detailed response based on the prompt.

### 3. **Document Processing**
- **Purpose**: Analyzes uploaded documents (TXT, CSV, PDF, JSON) based on user queries.
- **Functionality**:
  - Users can upload documents and provide a query for analysis.
  - The chatbot processes the document content and provides a detailed response based on the query.

## Technologies Used

- **Streamlit**: Framework for building and deploying the web application.
- **OpenAI API**: Powers the chatbot's intelligence using GPT-4 and GPT-4 Vision models.
- **PIL (Pillow)**: Handles image processing and manipulation.
- **Pandas**: Used for processing CSV files.
- **PyPDF2**: Extracts text from PDF documents.
- **Base64**: Encodes images for processing by the OpenAI API.

## Setup

### Prerequisites
- Python 3.8 or higher.
- OpenAI API key (stored in Streamlit secrets or environment variables).

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/blacifer-chatbot.git
   cd blacifer-chatbot