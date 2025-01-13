import streamlit as st 
import os
from phi.agent import Agent
from phi.model.google import Gemini
from phi.tools.duckduckgo import DuckDuckGo
from google.generativeai import upload_file,get_file
import google.generativeai as genai
from streamlit_option_menu import option_menu 
import time
from pathlib import Path
import tempfile
import base64

from dotenv import load_dotenv
load_dotenv()


API_KEY=os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# Page configuration
st.set_page_config(
    page_title="AGENT POWERED: Documents + Video Analyzer",
    page_icon="🎥",
    layout="wide"
)

st.title("AI Summarizer Agent 🖬🎥")
st.sidebar.image("Thinking-Brain.jpg")

image_style = '''
<style>
    #root > div:nth-child(1) > div.withScreencast > div > div > section.stSidebar.st-emotion-cache-1wqrzgl.eczjsme18 > div.st-emotion-cache-6qob1r.eczjsme11 > div.st-emotion-cache-1gwvy71.eczjsme12 > div > div > div > div > div:nth-child(1) > div > div > div.stImage.st-emotion-cache-kn8v7q.e115fcil2 > div > img {
        border: 2px solid #ccc; /* Add a border */
        border-radius: 10px; /* Add rounded corners */
        box-shadow: 0 4px 8px ; /* Add shadow for depth */
        margin-bottom: 5px;
    }

    #root > div:nth-child(1) > div.withScreencast > div > div > section.stMain.st-emotion-cache-bm2z3a.ea3mdgi8 > div.stMainBlockContainer.block-container.st-emotion-cache-1jicfl2.ea3mdgi5 > div {
        margin-top: -40px;
    }


</style> 
'''
st.markdown(image_style, unsafe_allow_html=True)

def display_pdf(file_bytes: bytes, file_name: str):
    """Displays the uploaded PDF in an iframe."""
    base64_pdf = base64.b64encode(file_bytes).decode("utf-8")
    pdf_display = f"""
    <iframe 
        src="data:application/pdf;base64,{base64_pdf}" 
        width="100%" 
        height="600px" 
        type="application/pdf"
    >
    </iframe>
    """
    st.markdown(f"### Preview of {file_name}")
    st.markdown(pdf_display, unsafe_allow_html=True)


@st.cache_resource
def initialize_agent():
    return Agent(
        name="AI Summarizer",
        model=Gemini(id="gemini-2.0-flash-exp"),
        tools=[DuckDuckGo()],
        markdown=True,
        add_history_to_messages=True,
    )

## Initialize the agent
multimodal_Agent=initialize_agent()

selected = option_menu(menu_title=None,options=["Video Analyzer","Document Analyzer"],orientation='horizontal',
            styles={
                "nav-link": {"--hover-color": "#826fdd61"}, 
                "nav-link-selected": {"background-color": "#635994"}
                })

if selected=="Video Analyzer":

    # File uploader
    video_file = st.sidebar.file_uploader(
        "Upload a video file", type=['mp4', 'mov', 'avi'], help="Upload a video for AI analysis"
    )

    if video_file:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(video_file.read())
            video_path = temp_video.name

        with st.sidebar.expander("Video Preview",expanded=True):
            st.video(video_path, format="video/mp4", start_time=0)

        user_query = st.text_area(
            "What insights are you seeking from the video?",
            placeholder="Ask anything about the video content. The AI agent will analyze and gather additional context if needed.",
            help="Provide specific questions or insights you want from the video."
        )

        if st.button("🔍 Analyze Video", key="analyze_video_button"):
            if not user_query:
                st.warning("Please enter a question or insight to analyze the video.")
            else:
                try:
                    with st.spinner("Processing video and gathering insights..."):
                        # Upload and process video file
                        processed_video = upload_file(video_path)
                        while processed_video.state.name == "PROCESSING":
                            time.sleep(1)
                            processed_video = get_file(processed_video.name)

                        # Prompt generation for analysis
                        analysis_prompt = (
                            f"""
                            Analyze the uploaded video for content and context.
                            Respond to the following query using video insights and supplementary web research:
                            {user_query}

                            Provide a detailed, user-friendly, and actionable response.
                            """
                        )

                        # AI agent processing
                        response = multimodal_Agent.run(analysis_prompt, videos=[processed_video])

                    # Display the result
                    st.subheader("Analysis Result")
                    st.markdown(response.content)

                except Exception as error:
                    st.error(f"An error occurred during analysis: {error}")
                finally:
                    # Clean up temporary video file
                    Path(video_path).unlink(missing_ok=True)
    else:
        st.info("Upload a video file to begin analysis.")

    # Customize text area height
    st.markdown(
        """
        <style>
        .stTextArea textarea {
            height: 100px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if selected == "Document Analyzer":

    # File uploader for documents
    document_file = st.sidebar.file_uploader(
        "Upload a document file", type=['pdf'], help="Upload a document for AI analysis"
    )

    if document_file:
        with st.sidebar.expander("Document Preview", expanded=True):
            # Optionally display the PDF in the sidebar
            display_pdf(document_file.getvalue(), document_file.name)

        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_document:
            temp_document.write(document_file.read())
            document_path = temp_document.name

        user_query = st.text_area(
            "What insights are you seeking from the document?",
            placeholder="Ask anything about the document content. The AI agent will analyze and gather additional context if needed.",
            help="Provide specific questions or insights you want from the document."
        )

        if st.button("🔍 Analyze Document", key="analyze_document_button"):
            if not user_query:
                st.warning("Please enter a question or insight to analyze the document.")
            else:
                try:
                    with st.spinner("Processing document and gathering insights..."):
                        # Upload and process document file
                        processed_document = upload_file(document_path)
                        while processed_document.state.name == "PROCESSING":
                            time.sleep(1)
                            processed_document = get_file(processed_document.name)

                        # Prompt generation for analysis
                        analysis_prompt = (
                            f"""
                            Analyze the uploaded document for content and context.
                            Respond to the following query using document insights and supplementary web research:
                            {user_query}

                            Provide a detailed, user-friendly, and actionable response.
                            """
                        )

                        # AI agent processing
                        response = multimodal_Agent.run(analysis_prompt, documents=[processed_document])

                    # Display the result
                    st.subheader("Analysis Result")
                    st.markdown(response.content)

                except Exception as error:
                    st.error(f"An error occurred during analysis: {error}")
                finally:
                    # Clean up temporary document file
                    Path(document_path).unlink(missing_ok=True)
    else:
        st.info("Upload a document file to begin analysis.")

    # Customize text area height
    st.markdown(
        """
        <style>
        .stTextArea textarea {
            height: 100px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


