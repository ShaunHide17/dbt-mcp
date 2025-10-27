import streamlit as st
from agent import build_agent, agent_ask
from storage import get_conn, create_chat, list_chats, get_chat_messages, add_message

if "chat_id" not in st.session_state:
    st.session_state.chat_id = None
if "agent" not in st.session_state:
    st.session_state.agent = build_agent()

conn = get_conn()

# ---------- Sidebar ----------
with st.sidebar:
    st.header("🧱 dbt MCP Chat")
    st.caption("Local dbt Core + MCP over stdio.")

    # Quick-start prompts
    st.subheader("Suggested prompts")
    suggested = [
        "List all models in my project",
        "Show me sources and their downstream models",
        "What tests are failing and why?",
        "Generate a model stub for a new incremental table",
        "Which models depend on {{ ref('my_model') }}?",
        "Run a dry-run build for the staging layer",
    ]
    for p in suggested:
        if st.button(p, use_container_width=True):
            # Start (or reuse) the current chat and inject the prompt into input box
            if not st.session_state.chat_id:
                st.session_state.chat_id = create_chat(conn, title="New chat")
            if "pending_input" not in st.session_state:
                st.session_state.pending_input = p
            else:
                st.session_state.pending_input = p

    st.divider()
    if st.button("➕ New chat", type="primary", use_container_width=True):
        st.session_state.chat_id = create_chat(conn, title="New chat")

    # st.subheader("Chat history")
    # for cid, title, created in list_chats(conn):
    #     label = f"#{cid} — {title or 'Untitled'}"
    #     if st.button(label, key=f"chat_{cid}", use_container_width=True):
    #         st.session_state.chat_id = cid

# ---------- Main Area ----------
st.title("dbt MCP Chat")

# New chat banner
if not st.session_state.chat_id:
    st.info("Start a new chat from the sidebar, or pick one from history.")
else:
    # Rename chat (first assistant reply often suggests a topic; allow user to set title)
    chat_row = conn.execute("SELECT title FROM chats WHERE id = ?", (st.session_state.chat_id,)).fetchone()
    if chat_row:
        new_title = st.text_input("Chat title", value=chat_row[0] or "New chat")
        if st.button("Save title"):
            conn.execute("UPDATE chats SET title = ? WHERE id = ?", (new_title, st.session_state.chat_id))
            conn.commit()
            st.success("Title saved")

    st.divider()
    # Render history
    for role, content, ts in get_chat_messages(conn, st.session_state.chat_id):
        with st.chat_message("user" if role == "user" else "assistant"):
            st.markdown(content)

# Chat input
user_text = st.chat_input(placeholder="Ask about your dbt project…", key="chat_input")

# Handle pending input from suggested prompts
if "pending_input" in st.session_state and not user_text:
    user_text = st.session_state.pop("pending_input")

if user_text:
    # Ensure a chat exists
    if not st.session_state.chat_id:
        st.session_state.chat_id = create_chat(conn, title="New chat")

    # Store user message & echo
    add_message(conn, st.session_state.chat_id, "user", user_text)
    with st.chat_message("user"):
        st.markdown(user_text)

    # Get assistant reply
    try:
        reply = agent_ask(st.session_state.agent, user_text)
    except Exception as e:
        reply = f"Sorry, I hit an error while calling dbt MCP:\n\n```\n{e}\n```"

    add_message(conn, st.session_state.chat_id, "assistant", reply)
    with st.chat_message("assistant"):
        st.markdown(reply)