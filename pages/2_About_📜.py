import streamlit as st

st.set_page_config(
    page_title="BibleBuddy About",
    page_icon="https://raw.githubusercontent.com/Lars-Ostervold/bible-project-chatbot/main/resources/images/favicon.ico",
    layout="centered"
)
st.title("About BibleBuddy 📜")

st.header("What is BibleBuddy?")
st.write("This is a conversational chatbot designed to help you understand the Bible and the story of Jesus by using content from The Bible Project. When you submit a question, the chatbot searches for relevant information in a database containing most of BibleProject's content. Then, your question and any relevant content are sent to ChatGPT to generate an answer. None of your data is saved in any way. If you have any questions or feedback, please reach out to me at [my email](mailto:lars.ostervold.3@gmail.com).👨🏼‍🍳")

st.write("We'll add a more detailed about page in the future. For now, enjoy the chatbot! 🚀")