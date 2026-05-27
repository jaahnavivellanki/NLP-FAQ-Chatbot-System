import time
from datetime import datetime
import streamlit as st
import streamlit.components.v1 as components
from chatbot import get_response

st.set_page_config(
    page_title="CampusMind AI",
    page_icon="🧠",
    layout="wide" # Wide layout for a premium full-screen SaaS feel
)


st.markdown("""
<style>
    /* Hide default Streamlit headers for a pristine app feel */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Transparent header to keep native buttons clickable */
    header {
        background-color: transparent !important;
        box-shadow: none !important;
    }
    
    /* Hide right-side header menu (Deploy, Settings, etc.) */
    [data-testid="stHeaderActionElements"] {
        display: none !important;
    }
    
    /* Premium visible toggle button for the FAQ sidebar */
    [data-testid="collapsedControl"] {
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        background-color: #1F2937 !important;
        border: 1px solid #374151 !important;
        border-radius: 8px !important;
        margin: 15px !important;
        padding: 5px 15px !important;
        color: #F9FAFB !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        transition: all 0.3s ease !important;
        z-index: 9999 !important;
    }
    
    /* Add 'FAQ' text to the native toggle button */
    [data-testid="collapsedControl"]::after {
        content: "FAQ";
        font-family: 'Inter', 'Segoe UI', sans-serif;
        font-size: 14px;
        font-weight: 600;
        margin-left: 8px;
        color: #F9FAFB !important;
    }
    
    [data-testid="collapsedControl"]:hover {
        background-color: #374151 !important;
        border-color: #4B5563 !important;
        transform: scale(1.05) !important;
    }
    
    /* Ensure sidebar close button is also styled well */
    [data-testid="stSidebarCollapseButton"] {
        color: #F9FAFB !important;
        transition: transform 0.3s ease !important;
    }
    [data-testid="stSidebarCollapseButton"]:hover {
        transform: scale(1.1) !important;
    }
    
    /* Modern dark background for the main app */
    .stApp {
        background-color: #0B0F19;
        color: #F3F4F6;
    }
    
    /* Elegant Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #1F2937;
    }
    
    /* Typography */
    * {
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Center the chat container */
    .block-container {
        padding-top: 1rem;
        padding-bottom: 150px;
        max-width: 950px;
        margin: 0 auto;
    }

    /* Fixed Rounded Chat Input Box */
    [data-testid="stChatInput"] {
        background-color: #1F2937 !important;
        border: 1px solid #374151 !important;
        border-radius: 24px !important;
        padding: 8px 12px !important;
        box-shadow: 0 -10px 30px rgba(0,0,0,0.5) !important;
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatInput"]:focus-within {
        border-color: #3B82F6 !important;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.4) !important;
    }
    
    [data-testid="stChatInput"] textarea {
        color: #F3F4F6 !important;
        font-size: 16px !important;
    }
    
    /* Chat Bubble Hover Effects & Styling */
    .chat-bubble-user {
        background: linear-gradient(135deg, #2563EB, #3B82F6);
        padding: 16px 22px; 
        border-radius: 24px 24px 4px 24px; 
        color: #ffffff; 
        font-size: 16px; 
        line-height: 1.5; 
        box-shadow: 0 4px 15px rgba(37, 99, 235, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .chat-bubble-user:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(37, 99, 235, 0.3);
    }
    
    .chat-bubble-bot {
        background-color: #1E293B; 
        padding: 16px 22px; 
        border-radius: 24px 24px 24px 4px; 
        color: #F3F4F6; 
        font-size: 16px; 
        line-height: 1.5; 
        border: 1px solid #334155; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .chat-bubble-bot:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    /* Smooth transition animation for chat bubbles */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animated-msg {
        animation: fadeIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    }
    
    /* Sticky Top Navbar */
    .navbar {
        background-color: rgba(17, 24, 39, 0.85);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid #1F2937;
        padding: 15px 0;
        margin-bottom: 40px;
        position: sticky;
        top: 0;
        z-index: 999;
        text-align: center;
        border-radius: 0 0 24px 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    }
    
    /* Feature Card Hover Effects */
    .feature-card {
        background-color: #1F2937; 
        border: 1px solid #374151; 
        padding: 24px; 
        border-radius: 20px; 
        margin-bottom: 15px; 
        transition: transform 0.3s ease, background-color 0.3s ease, box-shadow 0.3s ease;
        cursor: pointer;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        background-color: #374151;
        border-color: #4B5563;
        box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }
    
    /* Interactive FAQ Items */
    .faq-item {
        background-color: #1F2937;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 10px 15px;
        margin-bottom: 10px;
        color: #D1D5DB;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.2s ease;
        display: block;
    }
    .faq-item:hover {
        background-color: #374151;
        border-color: #4B5563;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        color: #F9FAFB;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="navbar">
    <h2 style='margin: 0; color: #F9FAFB; display: inline-flex; align-items: center; gap: 10px;'>
        <span style='font-size: 28px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));'>🧠</span> CampusMind AI
    </h2>
    <p style='margin: 0; margin-top: 4px; color: #9CA3AF; font-size: 0.95rem; font-weight: 500;'>Your Smart College Assistant</p>
</div>
""", unsafe_allow_html=True)

# Professional Sidebar
with st.sidebar:
    st.markdown("""
    <div style='text-align: center; margin-bottom: 30px; padding-top: 20px;'>
        <span style='font-size: 3.5rem; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));'>🧠</span>
        <h2 style='margin-top: 10px; margin-bottom: 0; color: #F9FAFB; font-weight: 700;'>CampusMind AI</h2>
        <p style='color: #9CA3AF; font-size: 0.9rem; margin-top: 5px;'>Your Smart College Assistant</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ⚡ Quick Student Actions")
    st.markdown("""
    <div style='margin-bottom: 20px;'>
        <div class="faq-item" data-text="I need help with admission">Admission Help</div>
        <div class="faq-item" data-text="What are the fee details?">Fee Details</div>
        <div class="faq-item" data-text="Tell me about hostel information">Hostel Information</div>
        <div class="faq-item" data-text="Do you provide placement support?">Placement Support</div>
        <div class="faq-item" data-text="I have queries about scholarships">Scholarship Queries</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 💬 Popular Questions")
    st.markdown("""
    <div style='margin-bottom: 20px;'>
        <div class="faq-item" data-text="How can I apply for admission?">"How can I apply for admission?"</div>
        <div class="faq-item" data-text="What is the attendance requirement?">"What is the attendance requirement?"</div>
        <div class="faq-item" data-text="Are placements available?">"Are placements available?"</div>
        <div class="faq-item" data-text="How can I pay fees?">"How can I pay fees?"</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 🤖 AI Assistant Features")
    st.markdown("""
    <div style='color: #D1D5DB; font-size: 0.95rem; line-height: 1.8; margin-bottom: 20px;'>
    ✓ 24/7 Student Support<br>
    ✓ Instant Responses<br>
    ✓ Smart Query Matching<br>
    ✓ College Info Assistant
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# HTML Render Functions for Chat Bubbles
def render_user_msg(msg, timestamp):
    return f"""
    <div class="animated-msg" style="display: flex; justify-content: flex-end; margin-bottom: 30px;">
        <div style="display: flex; flex-direction: column; align-items: flex-end; max-width: 80%;">
            <div class="chat-bubble-user">
                {msg}
            </div>
            <span style="font-size: 11px; color: #6B7280; margin-top: 8px; font-weight: 500;">{timestamp}</span>
        </div>
    </div>
    """

def render_bot_msg(msg, timestamp):
    return f"""
    <div class="animated-msg" style="display: flex; justify-content: flex-start; margin-bottom: 30px;">
        <div style="margin-right: 18px; font-size: 32px; display: flex; align-items: flex-start; margin-top: 4px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">🧠</div>
        <div style="display: flex; flex-direction: column; align-items: flex-start; max-width: 80%;">
            <div class="chat-bubble-bot">
                {msg}
            </div>
            <span style="font-size: 11px; color: #6B7280; margin-top: 8px; font-weight: 500;">{timestamp}</span>
        </div>
    </div>
    """

# Session State & Welcome Screen
if "messages" not in st.session_state:
    st.session_state.messages = []

# If chat history is empty, show the premium welcome screen
if len(st.session_state.messages) == 0:
    st.markdown("<h1 style='text-align: center; color: #F9FAFB; margin-top: 5vh; font-size: 3.5rem; letter-spacing: -1px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));'>CampusMind AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #9CA3AF; font-size: 1.25rem; margin-bottom: 50px;'>How can I help you with your college journey today?</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="feature-card" data-text="What is the admission process for B.Tech?">
            <div style="font-size: 22px; margin-bottom: 12px; color: #F3F4F6; font-weight: 600;">🎒 Admissions</div>
            <div style="color: #9CA3AF; font-size: 15px;">"What is the admission process for B.Tech?"</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card" data-text="What are the hostel charges and mess food like?">
            <div style="font-size: 22px; margin-bottom: 12px; color: #F3F4F6; font-weight: 600;">🏢 Hostel & Fees</div>
            <div style="color: #9CA3AF; font-size: 15px;">"What are the hostel charges and mess food like?"</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card" data-text="What is the highest placement package offered?">
            <div style="font-size: 22px; margin-bottom: 12px; color: #F3F4F6; font-weight: 600;">💼 Placements</div>
            <div style="color: #9CA3AF; font-size: 15px;">"What is the highest placement package offered?"</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("""
        <div class="feature-card" data-text="When are the semester exams held?">
            <div style="font-size: 22px; margin-bottom: 12px; color: #F3F4F6; font-weight: 600;">📝 Exams</div>
            <div style="color: #9CA3AF; font-size: 15px;">"When are the semester exams held?"</div>
        </div>
        """, unsafe_allow_html=True)
# Display Chat History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(render_user_msg(msg["content"], msg["timestamp"]), unsafe_allow_html=True)
    else:
        st.markdown(render_bot_msg(msg["content"], msg["timestamp"]), unsafe_allow_html=True)

# Handle User Input
if prompt := st.chat_input("Message CampusMind AI..."):
    
    current_time = datetime.now().strftime("%I:%M %p")
    
    # 1. Immediately show user message
    st.markdown(render_user_msg(prompt, current_time), unsafe_allow_html=True)
    st.session_state.messages.append({"role": "user", "content": prompt, "timestamp": current_time})

    # 2. Add an elegant typing placeholder
    placeholder = st.empty()
    bot_time = datetime.now().strftime("%I:%M %p")
    
    # Typing indicator visual
    placeholder.markdown(render_bot_msg("<span style='color:#9CA3AF;'><i>Analyzing query...</i></span>", "Just now"), unsafe_allow_html=True)
    
    # Fetch response from backend
    response, score = get_response(prompt)
    
    # 3. Stream text simulation (Animated typing effect)
    streamed_text = ""
    words = response.split(" ")
    for word in words:
        streamed_text += word + " "
        placeholder.markdown(render_bot_msg(streamed_text + "▌", bot_time), unsafe_allow_html=True)
        time.sleep(0.04) # Smooth typing delay
        
    # Final render without the cursor
    placeholder.markdown(render_bot_msg(streamed_text, bot_time), unsafe_allow_html=True)
    
    # Save the assistant response
    st.session_state.messages.append({
        "role": "assistant", 
        "content": response, 
        "timestamp": bot_time
    })


components.html("""
<script>
if (!window.parent.document.getElementById('faq-click-handler')) {
    let scriptTag = window.parent.document.createElement('div');
    scriptTag.id = 'faq-click-handler';
    scriptTag.style.display = 'none';
    window.parent.document.body.appendChild(scriptTag);
    
    window.parent.document.addEventListener('click', function(e) {
        let target = e.target.closest('.faq-item, .feature-card');
        if (target) {
            const text = target.getAttribute('data-text');
            if (!text) return;

            const chatInput = window.parent.document.querySelector('[data-testid="stChatInput"] textarea');
            if (chatInput) {
                // Set the value using React's native value setter
                const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLTextAreaElement.prototype, "value").set;
                nativeInputValueSetter.call(chatInput, text);
                
                // Dispatch input event so React state updates
                const event = new Event('input', { bubbles: true});
                chatInput.dispatchEvent(event);
                
                // Focus the input
                chatInput.focus();
                
                // Optional UI subtle animation on the chat input container
                const chatBox = window.parent.document.querySelector('[data-testid="stChatInput"]');
                if (chatBox) {
                    chatBox.style.transform = 'scale(1.02)';
                    chatBox.style.boxShadow = '0 0 20px rgba(59, 130, 246, 0.6)';
                    setTimeout(() => {
                        chatBox.style.transform = 'scale(1)';
                        chatBox.style.boxShadow = '0 -10px 30px rgba(0,0,0,0.5)';
                    }, 300);
                }
            }
        }
    });
}
</script>
""", height=0)
