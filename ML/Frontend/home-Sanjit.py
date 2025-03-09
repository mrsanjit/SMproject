import streamlit as st
import numpy as np

def show_home():
    st.html("<p><span style='text-decoration: line-through double red;'>Oops</span>!</p>")

# Function to show voice message (not used directly in your current code, but can be added if needed)
def show_voice():
    audio_value = st.audio_input("Record a voice message")

    if audio_value:
        st.audio(audio_value)

# Function to show a chat message and a chart (used in your main app)
def show_message():
    # Show a message
    with st.chat_message("user"):
        # st.write("Hello 👋")
        # st.balloons()
        st.snow()
        # st.success('This is a success message!', icon="✅")
       
    # Show a chart after the message
        st.line_chart(np.random.randn(30, 3))  # This is just an example; replace with relevant data
        # st.image("https://d2jx2rerrg6sh3.cloudfront.net/image-handler/picture/2017/4/Parkinson%27s_disease_brain_680x_-_Designua.jpg", caption="Sunrise by the mountains")

