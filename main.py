import streamlit as st
from api_v1 import get_access_token, send_message

st.title("Помощник")

# Исправлено: ключ должен быть "access_token"
if "access_token" not in st.session_state:
    try:
        st.session_state.access_token = get_access_token()
    except Exception as e:
        st.toast(f"Ошибка: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "bot",
            "content": "Я буду рад вам помочь, не стесняйтесь задавать мне вопросы!",
        }
    ]

for message in st.session_state.messages:
    if message.get("is_image"):
        st.chat_message(message["role"]).image(message["content"])
    else:
        st.chat_message(message["role"]).write(message["content"])

if user_message := st.chat_input():
    st.chat_message("user").write(user_message)
    st.session_state.messages.append({"role": "user", "content": user_message})

    with st.spinner("В процессе..."):
        response, is_image = send_message(user_message, st.session_state.access_token)
        if is_image:
            st.chat_message("bot").image(response)
            st.session_state.messages.append(
                {"role": "bot", "content": response, "is_image": True}
            )
        else:
            st.chat_message("bot").write(response)
            st.session_state.messages.append({"role": "bot", "content": response})
