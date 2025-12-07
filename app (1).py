
# Import semuanya dulu
import streamlit as st
from bot import build_agent

# Custom CSS for football field theme
st.markdown(
    """
    <style>
    .stApp {
        background-color: #4CAF50; /* A common green for football fields */
        background-image:
            linear-gradient(rgba(255, 255, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.1) 1px, transparent 1px);
        background-size: 50px 50px; /* Adjust grid size as needed */
        background-position: -2px -2px; /* Adjust for line thickness */
    }
    /* Optional: Make header/toolbar transparent if they overlay the background */
    [data-testid="stHeader"], [data-testid="stToolbar"] {
        background-color: rgba(0,0,0,0);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Judul
st.title("BOT FUTBOL")

# Session state
if "agent" not in st.session_state:
  st.session_state.agent = build_agent()

if "messages" not in st.session_state:
  st.session_state.messages = []

agent = st.session_state.agent

# Tombol-tombol dan UI
reset_chat_button = st.button("reset chat")
if reset_chat_button:
  st.session_state.messages = []
  st.session_state.agent = build_agent()
  # user_input = None
  # ai_output = None


user_input = st.chat_input()


for m in st.session_state.messages:
  with st.chat_message(m["role"]):
    st.markdown(m["content"], unsafe_allow_html=True)


if user_input is not None:
  # with st.chat_message("human"):
  st.session_state.messages.append({
    "role": "human",
    "content": user_input,
  })

  with st.chat_message("user"):
    st.markdown(user_input)


  with st.spinner("Thinking.."):
    ai_output = ""

    for step in agent.stream({"input": user_input}):
      if "actions" in step.keys():
        for action in step["actions"]:
          with st.chat_message("assistant"):
            tool_name = action.tool
            tool_input = action.tool_input

            tool_message = f"""
              <div style="border-left: 5px solid #4CAF50; padding:6px 10px; background-color: #f9f9f9; border-radius:4px; font-size:14px;">
                🛠️ <b>{tool_name}</b> <code>{tool_input}</code>
              </div>
            """
            st.session_state.messages.append({
              "role": "🛠️",
              "content": tool_message,
            })


            st.markdown(tool_message, unsafe_allow_html=True)


      if "output" in step.keys():
        ai_output = step["output"]


  with st.chat_message("assistant"):
    # with st.chat_message("assistant"):
    st.session_state.messages.append({
      "role": "assistant",
      "content": ai_output,
    })



    st.markdown(ai_output, unsafe_allow_html=True)


    # st.text(agent.memory.chat_memory.messages)
