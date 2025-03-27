import streamlit as st
from transformers import pipeline
import speech_recognition as sr

# Initialize transformer-based chatbot model (using GPT-2)
generator = pipeline('text-generation', model='gpt2')

def get_chatbot_response(user_input):
    """
    Generate a chatbot response given the user input.
    """
    prompt = f"User: {user_input}\nChatbot:"
    generated = generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
    answer = generated.split("Chatbot:")[-1].strip()
    return answer

def recognize_speech_from_mic():
    """
    Capture audio from the microphone and convert it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Please speak for up to 5 seconds.")
        audio = recognizer.listen(source, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, could not understand the audio."
    except sr.RequestError as e:
        return f"Error: {e}"

# Initialize conversation history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize user input in session state
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

def display_conversation():
    """
    Display the conversation history.
    """
    for message, is_user in st.session_state.messages:
        if is_user:
            st.markdown(f"**User:** {message}")
        else:
            st.markdown(f"**Chatbot:** {message}")

# App Title and Description
st.set_page_config(page_title="AI ChatBot")
st.title("Chatbot Assistant")
st.write("Interact with the chatbot using text or speech input.")
styling=f"""
<style>
p{{font-size: 1.2rem;}}
.st-emotion-cache-jkfxgf p{{font-size: 1.2rem;}}
</style>"""
st.markdown(styling,unsafe_allow_html=True)

# Input Method Selection
input_method = st.radio("Select Input Method:", ("📃 Text Input", "🎤 Speech Input"),horizontal=True)

# Process input based on the chosen method
if input_method == "📃 Text Input":
    st.session_state.user_input = st.text_input("Your Message:", value=st.session_state.user_input)
else:
    if st.button("Record Speech"):
        # Save recognized speech to session state
        st.session_state.user_input = recognize_speech_from_mic()
        st.write(f"You said: {st.session_state.user_input}")

# Process and send the message when "Send" is clicked
if st.session_state.user_input and st.button("Send"):
    # Append user message to conversation history
    st.session_state.messages.append((st.session_state.user_input, True))
    # Get chatbot response and update conversation history
    response = get_chatbot_response(st.session_state.user_input)
    st.session_state.messages.append((response, False))
    # Clear the input for the next message
    st.session_state.user_input = ""

# Display the conversation history
st.header("Conversation")
display_conversation()

# Option to clear the conversation history
if st.button("Clear Conversation"):
    st.session_state.messages = []
    st.experimental_rerun()


