
import streamlit as st
import openai

# # Get OpenAI API key from "Secrets" in Streamlit Community Cloud / Streamlit Community Cloudの「Secrets」からOpenAI API keyを取得
openai.api_key = st.secrets.OpenAIAPI.openai_api_key

# Save message interactions using st.session_state / st.session_stateを使いメッセージのやりとりを保存
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": st.secrets.AppSettings.chatbot_setting}
        ]

# Functions to interact with chatbots / チャットボットとやりとりする関数
def communicate():
    messages = st.session_state["messages"]

    user_message = {"role": "user", "content": st.session_state["user_input"]}
    messages.append(user_message)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    bot_message = response["choices"][0]["message"]
    messages.append(bot_message)

    st.session_state["user_input"] = ""  # 入力欄を消去


# Building user interfaces / ユーザーインターフェイスの構築
st.title("Chatbots to Help You Raise Your Child/子育てを助けるチャットボット")
st.image("life advice.png")
st.write("Do you have any problems raising your child? / 子育てについて、なにかお悩みですか？")

user_input = st.text_input("Enter your message / メッセージを入力してください。", key="user_input", on_change=communicate)

if st.session_state["messages"]:
    messages = st.session_state["messages"]

    for message in reversed(messages[1:]):  # Most recent message on top / 直近のメッセージを上に
        speaker = "🙂"
        if message["role"]=="assistant":
            speaker="🤖"

        st.write(speaker + ": " + message["content"])
