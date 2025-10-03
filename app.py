import streamlit as st
import os
import time
from prompts import PROMPT
from datetime import datetime
import base64
import json
import urllib.parse
import pyperclip
import re

try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if API_KEY:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
    else:
        st.error("Google API Key not found in .env file. Please create a .env file with GOOGLE_API_KEY=\"YOUR_API_KEY_HERE\"")
        st.stop()
except ImportError as e:
    st.error(f"Error importing google.generativeai: {e}. Please ensure it's installed correctly in your virtual environment.")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred during API setup: {e}")
    st.stop()

# Function to load the PDF and create a RAG-like system (placeholder)
def load_knowledge_bank(file_path):
    return f"Knowledge bank '{file_path}' conceptually loaded as part of the prompt."

# Custom CSS for styling
st.markdown("""
<style>
    .reportview-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        margin: 20px;
        padding: 30px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    }
    .stChatMessage {
        background: transparent !important;
        border: none !important;
        padding: 10px 0 !important;
    }
    .stChatMessage[data-testid="chatMessage"] {
        margin: 10px 0 !important;
    }
    .stChatMessage[data-testid="chatMessage"] .stMarkdown {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 15px 20px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .stChatMessage[data-testid="chatMessage"][data-role="user"] .stMarkdown {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left-color: #2196f3;
        margin-left: auto;
        margin-right: 0;
        max-width: 80%;
    }
    .stChatMessage[data-testid="chatMessage"][data-role="assistant"] .stMarkdown {
        background: linear-gradient(135deg, #f3e5f5 0%, #e1bee7 100%);
        border-left-color: #9c27b0;
        margin-right: auto;
        margin-left: 0;
        max-width: 80%;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 4px 10px !important;
        font-size: 11px !important;
        font-weight: 400 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 1px 3px rgba(102, 126, 234, 0.2) !important;
        min-width: 45px !important;
        text-align: center !important;
        letter-spacing: 0.3px !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%) !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 2px 6px rgba(102, 126, 234, 0.3) !important;
    }
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        padding: 15px 25px !important;
        border: 2px solid #e0e0e0 !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1) !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 5px 20px rgba(102, 126, 234, 0.3) !important;
    }
    .stExpander > div > div {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        margin-top: 15px !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1) !important;
        border-left: 4px solid #667eea !important;
    }
    .stExpander > div > div > div:first-child {
        font-weight: bold !important;
        color: #495057 !important;
        font-size: 18px !important;
    }
    .stCaption {
        color: #6c757d !important;
        font-size: 12px !important;
        font-style: italic !important;
        margin-top: 5px !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stApp {
        padding-bottom: 0px !important;
    }
    .stForm {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        box-shadow: 0 -5px 20px rgba(0,0,0,0.1);
        z-index: 999;
        backdrop-filter: blur(10px);
    }
    @keyframes toneshift-animation {
        0% { background-position: 0% 50%; filter: hue-rotate(0deg); opacity: 1; }
        50% { background-position: 100% 50%; filter: hue-rotate(180deg); opacity: 0.7; }
        100% { background-position: 0% 50%; filter: hue-rotate(360deg); opacity: 1; }
    }
    .toneshift-spinner {
        font-size: 1.5em;
        font-weight: bold;
        background: linear-gradient(90deg, #FF6B6B, #FFD166, #6a11cb, #2575fc);
        background-size: 200% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: toneshift-animation 3s ease infinite;
        display: inline-block;
        margin-bottom: 10px;
    }
</style>



""", unsafe_allow_html=True)

# Logo base64 encode function
def get_base64_image(image_path):
    if not os.path.exists(image_path):
        return "R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw=="
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Dummy logo (replace with your actual logo file path)
dummy_logo_path = "./ToneShift_logo.png"

# Function to handle copy operation
def copy_text_to_clipboard(text_to_copy):
    try:
        pyperclip.copy(text_to_copy)
        st.toast("Text copied to clipboard!")
    except Exception as e:
        st.error(f"Failed to copy: {e}")



# Function to clean AI response content
def clean_ai_content(content):
    if not content:
        return ""
    
    # Remove any HTML button code and JavaScript
    content = re.sub(r'<button.*?</button>', '', content, flags=re.DOTALL)
    content = re.sub(r'onclick=.*?\)', '', content)
    content = re.sub(r'navigator\.clipboard.*?\)', '', content)
    content = re.sub(r'this\.innerHTML.*?Copy', '', content)
    
    # Remove any HTML tags completely
    content = re.sub(r'<[^>]+>', '', content)
    
    # Remove any raw JSON or configuration text
    content = re.sub(r'Raw text:.*?}', '', content, flags=re.DOTALL)
    content = re.sub(r'\{[^}]*copy_button[^}]*\}', '', content)
    content = re.sub(r'ui_style.*?background.*?}', '', content, flags=re.DOTALL)
    content = re.sub(r'style=.*?Copy', '', content, flags=re.DOTALL)
    
    # Remove any backtick-wrapped content that looks like code
    content = re.sub(r'`[^`]*`', '', content)
    
    # Remove any remaining problematic patterns
    content = re.sub(r'copy_button.*?Copy', '', content, flags=re.DOTALL)
    content = re.sub(r'background.*?Copy', '', content, flags=re.DOTALL)
    
    # Clean up list markers
    content = content.replace("\n+ ", "\n- ")
    content = content.replace("\n* ", "\n- ")
    
    # Remove extra whitespace and normalize
    content = re.sub(r'\n\s*\n', '\n\n', content)
    content = re.sub(r'^\s+', '', content, flags=re.MULTILINE)
    content = re.sub(r'\s+$', '', content, flags=re.MULTILINE)
    
    # Remove any lines that contain only technical terms
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Skip lines that are just technical markup
        if not re.match(r'^[\s\-*+`{}[\]]*$', line.strip()):
            cleaned_lines.append(line)
    
    content = '\n'.join(cleaned_lines)
    
    return content.strip()

# Initialize chat history and chat session in session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.knowledge_loaded = load_knowledge_bank("ToneShift Model_ Knowledge Bank.pdf")
    st.session_state.chat = model.start_chat(history=[])

# --- UI Rendering Logic ---

# Create a placeholder for the initial content (logo, starters)
initial_content_placeholder = st.empty()

# Check if conversation has started
conversation_started = len(st.session_state.messages) > 0

# Initial state: Centered Logo and Conversation Starters
if not conversation_started:
    with initial_content_placeholder.container():
        st.markdown(
            """
            <style>
            .centered-container {{
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 70vh;
                text-align: center;
            }}
            .logo-text {{
                font-size: 3em;
                font-weight: bold;
                background: linear-gradient(45deg, #FF6B6B, #FFD166);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin-bottom: 20px;
            }}
            .logo-image {{
                width: 150px;
                height: 150px;
                margin-bottom: 20px;
                border-radius: 20%;
                box-shadow: 0 8px 16px rgba(0,0,0,0.2);
            }}
            </style>
            <div class="centered-container">
                <img src="data:image/png;base64,{logo_base64}" alt="ToneShift Logo" class="logo-image">
                <div class="logo-text">ToneShift</div>
            </div>
            """.format(logo_base64=get_base64_image(dummy_logo_path)),
            unsafe_allow_html=True
        )

        st.markdown("---")
        st.markdown("<h3 style='text-align: center;'>Conversation Starters:</h3>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        conversation_starters = [
            "Make this sound like [@Wendys]",
            "Explain Newton's law of motion to a 5-year-old",
            "Turn this text into a LinkedIn post"
        ]
        with col1:
            if st.button(conversation_starters[0], key="starter1", type="primary"):
                st.session_state.messages.append({"role": "user", "content": conversation_starters[0], "time": datetime.now().strftime("%H:%M")})
                st.rerun()
        with col2:
            if st.button(conversation_starters[1], key="starter2", type="primary"):
                st.session_state.messages.append({"role": "user", "content": conversation_starters[1], "time": datetime.now().strftime("%H:%M")})
                st.rerun()
        with col3:
            if st.button(conversation_starters[2], key="starter3", type="primary"):
                st.session_state.messages.append({"role": "user", "content": conversation_starters[2], "time": datetime.now().strftime("%H:%M")})
                st.rerun()

# Clear initial content if conversation has started and display top-left logo
if conversation_started:
    initial_content_placeholder.empty()
    st.markdown(
        """
        <style>
        .top-left-logo {{
            display: flex;
            align-items: center;
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1000;
            background-color: rgba(255,255,255,0.8);
            padding: 5px 10px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        .top-left-logo-image {{
            width: 40px;
            height: 40px;
            margin-right: 8px;
            border-radius: 15%;
        }}
        .top-left-logo-text {{
            font-size: 1.2em;
            font-weight: bold;
            background: linear-gradient(45deg, #FF6B6B, #FFD166);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        </style>
        <div class="top-left-logo">
            <img src="data:image/png;base64,{logo_base64}" alt="ToneShift Logo" class="top-left-logo-image">
            <div class="top-left-logo-text">ToneShift</div>
        </div>
        """.format(logo_base64=get_base64_image(dummy_logo_path)),
        unsafe_allow_html=True
    )

    # Display chat messages
    for i, message in enumerate(st.session_state.messages):
        content = message["content"]
        
        if message["role"] == "user":
            # User message - right aligned
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; margin: 10px 0;">
                <div style="max-width: 70%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 15px 20px; border-radius: 18px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3); color: white;">
                    {content}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Copy button and timestamp in a row - aligned to extreme right
            col1, col2, col3, col4 = st.columns([0.6, 0.1, 0.1, 0.2])
            with col4:
                # Copy button and timestamp in same row
                col_button, col_timestamp = st.columns([0.7, 0.3])
                with col_button:
                    # Copy button with premium visual feedback
                    if f"copy_user_status_{i}" not in st.session_state:
                        st.session_state[f"copy_user_status_{i}"] = False
                    
                    if st.button("Copy", key=f"copy_user_{i}", use_container_width=True):
                        try:
                            pyperclip.copy(content)
                            st.session_state[f"copy_user_status_{i}"] = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Failed to copy: {e}")
                    
                    if st.session_state.get(f"copy_user_status_{i}", False):
                        st.markdown("✅", help="Copied successfully")
                with col_timestamp:
                    st.markdown(f"<div style='text-align: center; color: #6c757d; font-size: 12px; font-style: italic;'>{message['time']}</div>", unsafe_allow_html=True)

        else: # role == "assistant"
            # AI message - left aligned
            # Parse the AI response more carefully
            if "---### 📜 **Style Report**" in content:
                parts = content.split("---### 📜 **Style Report**", 1)
                if len(parts) == 2:
                    rewritten_text = parts[0].strip()
                    style_report = parts[1].strip()
                    
                    # Clean the rewritten text
                    rewritten_text = clean_ai_content(rewritten_text)
                    
                    # Display the rewritten text
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                        <div style="max-width: 70%; background: #f8f9fa; padding: 15px 20px; border-radius: 18px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: #333; border: 1px solid #e9ecef;">
                            {rewritten_text}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Copy button and timestamp in a row
                    col1, col2, col3, col4 = st.columns([0.2, 0.1, 0.1, 0.6])
                    with col1:
                        # Copy button with premium visual feedback
                        if f"copy_assistant_status_{i}" not in st.session_state:
                            st.session_state[f"copy_assistant_status_{i}"] = False
                        
                        if st.button("Copy", key=f"copy_assistant_{i}", use_container_width=True):
                            try:
                                pyperclip.copy(rewritten_text)
                                st.session_state[f"copy_assistant_status_{i}"] = True
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Failed to copy: {e}")
                        
                        if st.session_state.get(f"copy_assistant_status_{i}", False):
                            st.markdown("✅", help="Copied successfully")
                    with col2:
                        st.markdown(f"<div style='text-align: center; color: #6c757d; font-size: 12px; font-style: italic;'>{message['time']}</div>", unsafe_allow_html=True)
                    
                    # Display style report in expander
                    if style_report:
                        with st.expander("📜 Style Report (Click to expand)"):
                            # Clean the style report content
                            clean_style_report = clean_ai_content(style_report)
                            st.markdown(clean_style_report, unsafe_allow_html=False)
                else:
                    # Fallback if parsing fails
                    clean_content = clean_ai_content(content)
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                        <div style="max-width: 70%; background: #f8f9fa; padding: 15px 20px; border-radius: 18px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: #333; border: 1px solid #e9ecef;">
                            {clean_content}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Copy button and timestamp in a row
                    col1, col2, col3, col4 = st.columns([0.2, 0.1, 0.1, 0.6])
                    with col1:
                        # Copy button with premium visual feedback
                        if f"copy_fallback_status_{i}" not in st.session_state:
                            st.session_state[f"copy_fallback_status_{i}"] = False
                        
                        if st.button("Copy", key=f"copy_fallback_{i}", use_container_width=True):
                            try:
                                pyperclip.copy(clean_content)
                                st.session_state[f"copy_fallback_status_{i}"] = True
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Failed to copy: {e}")
                        
                        if st.session_state.get(f"copy_fallback_status_{i}", False):
                            st.markdown("✅", help="Copied successfully")
                    with col2:
                        st.markdown(f"<div style='text-align: center; color: #6c757d; font-size: 12px; font-style: italic;'>{message['time']}</div>", unsafe_allow_html=True)
            else:
                # No style report, just display the content
                clean_content = clean_ai_content(content)
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin: 10px 0;">
                    <div style="max-width: 70%; background: #f8f9fa; padding: 15px 20px; border-radius: 18px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); color: #333; border: 1px solid #e9ecef;">
                        {clean_content}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Copy button and timestamp in a row
                col1, col2, col3, col4 = st.columns([0.2, 0.1, 0.1, 0.6])
                with col1:
                    # Copy button with premium visual feedback
                    if f"copy_simple_status_{i}" not in st.session_state:
                        st.session_state[f"copy_simple_status_{i}"] = False
                    
                    if st.button("Copy", key=f"copy_simple_{i}", use_container_width=True):
                        try:
                            pyperclip.copy(clean_content)
                            st.session_state[f"copy_simple_status_{i}"] = True
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Failed to copy: {e}")
                    
                    if st.session_state.get(f"copy_simple_status_{i}", False):
                        st.markdown("✅", help="Copied successfully")
                with col2:
                    st.markdown(f"<div style='text-align: center; color: #6c757d; font-size: 12px; font-style: italic;'>{message['time']}</div>", unsafe_allow_html=True)

# This placeholder will hold the spinner if a response is being generated
toneshift_spinner_placeholder = st.empty()

# Chat input at the bottom - simplified approach
user_query = st.chat_input("Enter your text and target tone...")

# Handle user input
if user_query:
    # Add user message to session state immediately
    st.session_state.messages.append({"role": "user", "content": user_query, "time": datetime.now().strftime("%H:%M")})
    st.rerun()

# Check if we need to generate a response for the latest user message
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    # Simple and reliable logic: always generate a response for the latest user message
    # This ensures every user message gets a response, just like ChatGPT/Gemini
    
    # Display spinner above the chat input box
    with toneshift_spinner_placeholder.container():
        st.markdown("<span class='toneshift-spinner'>ToneShifting...</span>", unsafe_allow_html=True)
        
    last_user_message_content = st.session_state.messages[-1]["content"]
    
    relevant_context = st.session_state.knowledge_loaded
    system_message = "You are a Style Adaptation Engine. NEVER include HTML tags, JavaScript code, onclick attributes, navigator.clipboard, button code, or any programming syntax. ONLY provide plain text content suitable for display."
    full_input = f"System: {system_message}\n\nPrompt: {PROMPT}\n\nRelevant Context: {relevant_context}\n\nUser Query: {last_user_message_content}"
    
    try:
        response = st.session_state.chat.send_message(full_input, stream=False)
        full_response = response.text if hasattr(response, 'text') else str(response)

    except Exception as e:
        full_response = f"Error: {e}. Please ensure your GOOGLE_API_KEY is correct and enabled for Gemini API."

    # Add assistant response to session state
    st.session_state.messages.append({"role": "assistant", "content": full_response, "time": datetime.now().strftime("%H:%M")})
    
    # Clear spinner and rerun to show complete conversation
    toneshift_spinner_placeholder.empty()
    st.rerun() 