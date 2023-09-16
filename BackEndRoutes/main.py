import BackEndRoutes.streamlit as st
import google.generativeai as palm

# Configure API key
palm.configure(api_key='AIzaSyA1fu-ob27CzsJozdr6pHd96t5ziaD87wM')

# Set page title
st.set_page_config(page_title="🌴🤖 Palm Chatbot")

# Initialize chat
response = palm.chat(messages=["Hi!"])
chat_history = [{"role": "Bot", "content": response.last}]

# Display chat messages
for message in chat_history:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function for generating bot response
def generate_bot_response(user_input):
    return palm.chat(messages=[user_input]).last

# User input box
user_input = st.text_input("You:", key="user_input")

if st.button("Send"):
    if user_input:
        if user_input.upper() == "Q":
            st.stop()
        else:
            response = generate_bot_response(user_input)
            message = {"role": "User", "content": user_input}
            chat_history.append(message)
            message = {"role": "Bot", "content": response}
            chat_history.append(message)

            # Display chat messages
            with st.spinner("Thinking..."):
                for message in chat_history[-2:]:
                    with st.chat_message(message["role"]):
                        st.write(message["content"])
