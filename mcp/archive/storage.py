import sqlite3
import streamlit as st
from datetime import datetime
from typing import List, Tuple

# ---------- SQLite helpers ----------
@st.cache_resource
def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect("chat_history.db", check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            role TEXT NOT NULL,             -- 'user' | 'assistant' | 'system'
            content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(chat_id) REFERENCES chats(id) ON DELETE CASCADE
        )
        """
    )
    conn.commit()
    return conn

def create_chat(conn: sqlite3.Connection, title: str) -> int:
    ts = datetime.utcnow().isoformat()
    cur = conn.execute("INSERT INTO chats (title, created_at) VALUES (?, ?)", (title, ts))
    conn.commit()
    return cur.lastrowid

def list_chats(conn: sqlite3.Connection) -> List[Tuple[int, str, str]]:
    cur = conn.execute("SELECT id, title, created_at FROM chats ORDER BY id DESC")
    return cur.fetchall()

def get_chat_messages(conn: sqlite3.Connection, chat_id: int) -> List[Tuple[str, str, str]]:
    cur = conn.execute(
        "SELECT role, content, created_at FROM messages WHERE chat_id = ? ORDER BY id ASC",
        (chat_id,),
    )
    return cur.fetchall()

def add_message(conn: sqlite3.Connection, chat_id: int, role: str, content: str) -> None:
    ts = datetime.utcnow().isoformat()
    conn.execute(
        "INSERT INTO messages (chat_id, role, content, created_at) VALUES (?, ?, ?, ?)",
        (chat_id, role, content, ts),
    )
    conn.commit()