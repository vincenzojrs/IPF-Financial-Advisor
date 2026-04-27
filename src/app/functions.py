import streamlit as st


def render_assistant_response(response):
    if response is None:
        return

    if "__interrupt__" in response:
        return

    if "answer" in response:
        with st.chat_message("assistant"):
            st.markdown(response["answer"])

            st.session_state.messages.append(
                {"role": "assistant", "content": response["answer"]}
            )


def render_user_message(label, values):
    if isinstance(values, dict):
        lines = []
        for key, value in values.items():
            lines.append(f"  - {key}: {value}")
        content = f"{label.title()}\n" + "\n".join(lines)
    else:
        content = f"{label.title()}\n  - {values}"

    with st.chat_message("user"):
        st.markdown(content)

    st.session_state.messages.append({"role": "user", "content": content})
