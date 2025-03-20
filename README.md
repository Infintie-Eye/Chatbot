Blacifer Chatbot - Streamlit Application
Welcome to the Blacifer Chatbot, a Streamlit-based application that integrates OpenAI's GPT-4 and GPT-4 Vision models to provide a versatile chatbot experience. This app allows users to interact with the chatbot for text-based conversations, image analysis, and document processing.

Features
Text-Based Chat:

Interact with the chatbot using natural language.

The chatbot is powered by OpenAI's GPT-4 model.

Image Analysis:

Upload images (JPG, JPEG, PNG) and provide a prompt for analysis.

The chatbot uses GPT-4 Vision to analyze the image and provide insights.

Document Processing:

Upload documents (TXT, CSV, PDF, JSON) and provide a query for analysis.

The chatbot extracts and processes the document content using GPT-4.

Customizable Interface:

A user-friendly interface with a navigation bar, sidebar, and tabs for easy navigation.

Custom CSS for styling the app, sidebar, and navigation bar.

Secure API Key Handling:

OpenAI API key is securely managed using Streamlit's st.secrets.

Getting Started
Prerequisites
Python 3.8+: Ensure Python is installed on your system.

OpenAI API Key: Obtain an API key from OpenAI.

Streamlit: Install Streamlit to run the app.

Installation
Clone the Repository:

bash
Copy
git clone https://github.com/Infinite-Eye/blacifer-chatbot.git
cd blacifer-chatbot
Install Dependencies:
Install the required Python libraries:

bash
Copy
pip install streamlit openai pillow pandas PyPDF2
Set Up Secrets:
Create a .streamlit/secrets.toml file and add your OpenAI API key:

toml
Copy
OPENAI_API_KEY = "your-api-key-here"
Run the App:
Start the Streamlit app:

bash
Copy
streamlit run chatbot.py
Usage
Text-Based Chat:

Navigate to the Chat Assistant tab.

Type your query in the chat input box and press Enter.

The chatbot will respond with an analysis or answer.

Image Analysis:

Navigate to the Image Analysis tab.

Upload an image (JPG, JPEG, PNG) and provide a prompt for analysis.

Click Analyze Image to get insights from the chatbot.

Document Processing:

Navigate to the Document Intelligence tab.

Upload a document (TXT, CSV, PDF, JSON) and provide a query for analysis.

Click Analyze Document to get insights from the chatbot.

Sidebar:

Use the sidebar to access quick links (Home, Support, FAQ) and provide feedback.

File Structure
Copy
blacifer-chatbot/
├── chatbot.py                # Main Streamlit application
├── .streamlit/
│   └── secrets.toml         # Secrets file for API key
├── logo.jpg                 # Logo image for the sidebar
├── stylepage.css            # Custom CSS for the main page
├── stylesidebar.css         # Custom CSS for the sidebar
├── navbar.css               # Custom CSS for the navigation bar
└── README.md                # This file
Customization
Logo:

Replace logo.jpg with your own logo file.

CSS Styling:

Modify stylepage.css, stylesidebar.css, and navbar.css to customize the app's appearance.

Navigation Bar:

Update the navigation bar buttons in chatbot.py to link to your desired pages.

Sidebar:

Customize the sidebar content in the setup_sidebar function.

Troubleshooting
API Key Not Found:

Ensure the secrets.toml file is correctly configured with your OpenAI API key.

File Upload Issues:

Streamlit has a default file upload limit of 200MB. For larger files, adjust the limit in the Streamlit configuration.

CSS Not Loading:

Ensure the CSS files (stylepage.css, stylesidebar.css, navbar.css) are in the correct directory.

Logging Errors:

Check the logs for detailed error messages. Logs are saved in the terminal where the app is running.

Contributing
Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

Fork the repository.

Create a new branch for your feature or bug fix.

Commit your changes and push to the branch.

Submit a pull request.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgments
OpenAI: For providing the GPT-4 and GPT-4 Vision models.

Streamlit: For the easy-to-use framework for building web apps.

Pillow, Pandas, PyPDF2: For handling image and document processing.

Contact
For questions or feedback, please reach out to:

Your Name: moulikkhanna2019.com

Project Repository: GitHub