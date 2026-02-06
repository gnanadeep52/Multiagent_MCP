
import time
import streamlit as st
import asyncio
from agents.note_taker_agent import note_taker_agent
from agents.doc_writer_agent import doc_writer_agent

# ────────────────────────────────────────────────
# Page configuration
# ────────────────────────────────────────────────
st.set_page_config(
    page_title="DeepDraft",
    layout="wide"
)

st.title("DeepDraft 📝")
st.caption(
    "Type your topic or question → get outline → full document → summary points\n"
    "Type 'quit', 'exit' or 'q' to stop."
)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Your topic or question...")

if user_input:
    # Add and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Quit / exit detection
    if user_input.strip().lower() in ["quit", "exit", "q", "bye", "stop"]:
        goodbye = "Goodbye! Come back anytime."
        st.session_state.messages.append({"role": "assistant", "content": goodbye})
        with st.chat_message("assistant"):
            st.markdown(goodbye)
        st.rerun()

    else:
        # Assistant response block
        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                try:
                    # ── 1. Outline first
                    outline_result = asyncio.run(note_taker_agent(user_input.strip()))
                    outline_points = outline_result.get("outline_points", [])

                    outline_text = "**Outline**\n\n"
                    if outline_points:
                        for i, point in enumerate(outline_points, 1):
                            outline_text += f"{point}\n\n"
                    else:
                        outline_text += "(no outline points generated)\n\n"

                    st.markdown(outline_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": outline_text}
                    )

                    # Small pause so user can read the outline
                    time.sleep(0.8)

                    # ── 2. Full document 
                    write_result = asyncio.run(
                        doc_writer_agent(
                            topic=user_input.strip(),
                            outline=outline_points
                        )
                    )

                    full_content = write_result.get("final_content", "")

                    doc_text = "**Full Document**\n\n" + (
                        full_content or "(no document content generated)"
                    )

                    st.markdown(doc_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": doc_text}
                    )

                    # Small pause before summary
                    time.sleep(0.6)

                    # ── 3. Summary points last 
                    summary_points = write_result.get("final_summary_points", [])

                    summary_text = "**Key Summary Points**\n\n"
                    if summary_points:
                        for point in summary_points:
                            summary_text += f"• {point}\n"
                    else:
                        summary_text += "(no summary points generated)\n"

                    st.markdown(summary_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": summary_text}
                    )

                except Exception as e:
                    error_text = f"**Error occurred**\n\n{str(e)}"
                    st.error(error_text)
                    st.session_state.messages.append(
                        {"role": "assistant", "content": error_text}
                    )

    
    st.rerun()