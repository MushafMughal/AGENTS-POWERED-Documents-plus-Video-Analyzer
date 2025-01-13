# AI AGENTS POWERED: Documents + Video Summarizer 🖬🎥

This Streamlit application is an AI-powered tool designed to analyze and summarize both video and document content. It leverages the Gemini model from Google and integrates with DuckDuckGo for additional web research. The application allows users to upload video or document files, ask specific questions, and receive detailed, actionable insights.

## Features

- **Video Analyzer**: Upload a video file (MP4, MOV, AVI) and ask questions to get detailed insights.
- **Document Analyzer**: Upload a PDF document and ask questions to extract key information and insights.
- **Multimodal AI Agent**: Utilizes the Gemini model for content analysis and DuckDuckGo for supplementary web research.
- **Interactive UI**: User-friendly interface with options to preview uploaded files and customize queries.

![image](https://github.com/user-attachments/assets/e80a5ecd-be70-42a7-8cfd-d49aac27ceb6)
![image](https://github.com/user-attachments/assets/ab7e14b3-db48-4bc4-8382-d4421cec3c47)

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MushafMughal/AI-Summarizer-Agent.git
   cd AI-Summarizer-Agent
   ```
2. Set Up Environment Variables:
   - Create a .env file in the root directory.
   - Add your Google API key:
   ```plaintext
   GOOGLE_API_KEY=your_google_api_key_here
   ```
3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the Application:
   ```bash
   streamlit run app.py
   ```
---
# Usage

## Video Analyzer:
- Upload a video file using the sidebar.
- Enter your query in the text area.
- Click the "Analyze Video" button to get insights.

## Document Analyzer:
- Upload a PDF document using the sidebar.
- Enter your query in the text area.
- Click the "Analyze Document" button to get insights.

---

# Code Structure
- **app.py**: Main Streamlit application script.
- **requirements.txt**: List of Python dependencies.
- **.env**: Environment variables file for storing API keys.
- **Thinking-Brain.jpg**: Image used in the sidebar.

---

# Customization
- **Styling**: Custom CSS styles are applied to enhance the UI. You can modify the `image_style` variable in the script to change the appearance.
- **Agent Configuration**: The AI agent is initialized with the Gemini model and DuckDuckGo tool. You can customize the agent's configuration in the `initialize_agent` function.

---

# Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

---

# Acknowledgments
- [Streamlit](https://streamlit.io/) for the web application framework.
- [Google Generative AI](https://developers.google.com/machine-learning/generative-ai) for the Gemini model.
- [DuckDuckGo](https://duckduckgo.com/) for web search capabilities.
