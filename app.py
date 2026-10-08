import streamlit as st
from chatbot import FAQChatbot


# ---------------------------------------
# Page Configuration
# ---------------------------------------

st.set_page_config(
    page_title="AI FAQ Assistant",
    page_icon="🤖",
    layout="centered"
)


# ---------------------------------------
# Custom CSS
# ---------------------------------------

st.markdown(
    """
    <style>

    .title {
        text-align: center;
        font-size: 40px;
        font-weight: bold;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: gray;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .info {
        padding: 15px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin-bottom: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------
# Load Chatbot
# ---------------------------------------

@st.cache_resource
def load_chatbot():

    return FAQChatbot("faqs.json")


chatbot = load_chatbot()


# ---------------------------------------
# Header
# ---------------------------------------

st.markdown(
    '<div class="title">🤖 AI FAQ Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Natural Language Processing Based FAQ Chatbot'
    '</div>',
    unsafe_allow_html=True
)


# ---------------------------------------
# Information Box
# ---------------------------------------

st.markdown(
    """
    <div class="info">
    💡 Ask me anything about accounts, payments,
    security, support, or technical problems.
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------
# Initialize Chat History
# ---------------------------------------

if "messages" not in st.session_state:

    st.session_state.messages = []


# ---------------------------------------
# Display Previous Messages
# ---------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.write(message["content"])


# ---------------------------------------
# User Input
# ---------------------------------------

user_question = st.chat_input(
    "Type your question here..."
)


# ---------------------------------------
# Process Question
# ---------------------------------------

if user_question:

    # Display user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_question
        }
    )

    with st.chat_message("user"):

        st.write(user_question)


    # Get chatbot response

    result = chatbot.get_response(
        user_question
    )

    response = result["answer"]
    confidence = result["confidence"]
    category = result["category"]


    # Display chatbot response

    with st.chat_message("assistant"):

        st.write(response)

        if category != "Unknown":

            st.caption(
                f"Category: {category} | "
                f"Confidence: {confidence:.2%}"
            )


    # Save response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )


# ---------------------------------------
# Sidebar
# ---------------------------------------

with st.sidebar:

    st.header("🤖 About")

    st.write(
        """
        This application is an AI-powered FAQ chatbot
        that uses Natural Language Processing to find
        the most relevant answer to a user's question.
        """
    )

    st.divider()

    st.subheader("🛠 Technologies")

    st.write("Python")
    st.write("NLTK")
    st.write("Scikit-learn")
    st.write("TF-IDF")
    st.write("Cosine Similarity")
    st.write("Streamlit")

    st.divider()

    st.subheader("📌 Example Questions")

    st.write("• How do I create an account?")
    st.write("• I forgot my password")
    st.write("• Do you accept UPI?")
    st.write("• Can I get a refund?")
    st.write("• Is my data secure?")

    st.divider()

    if st.button(
        "🗑️ Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()