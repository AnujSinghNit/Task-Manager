import streamlit as st
import sqlite3
import os
import math
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

# ---------------------------------------------------------------------------
# App Configuration
# ---------------------------------------------------------------------------
st.set_page_config(page_title="TrackIT - Issue Tracker", page_icon="🎫", layout="wide")

DB_PATH = os.path.join(os.getcwd(), "database.db")

# ---------------------------------------------------------------------------
# Database Helpers
# ---------------------------------------------------------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    fresh = not os.path.exists(DB_PATH)
    conn = get_db_connection()
    conn.execute("PRAGMA foreign_keys = ON")

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            username    TEXT    NOT NULL UNIQUE,
            password    TEXT    NOT NULL,
            full_name   TEXT    NOT NULL,
            role        TEXT    NOT NULL DEFAULT 'user',
            created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS tickets (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT    NOT NULL,
            description TEXT    NOT NULL,
            priority    TEXT    NOT NULL DEFAULT 'Medium',
            status      TEXT    NOT NULL DEFAULT 'Open',
            assigned_to TEXT,
            created_by  TEXT    NOT NULL,
            created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
            updated_at  TEXT    NOT NULL DEFAULT (datetime('now'))
        );
    """)

    if fresh:
        # Seed Data
        users = [
            ("admin", generate_password_hash("admin"), "Admin User", "admin"),
            ("john",  generate_password_hash("john123"), "John Smith", "developer"),
            ("sarah", generate_password_hash("sarah123"), "Sarah Connor", "support"),
        ]
        conn.executemany("INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)", users)
        conn.commit()
    conn.close()

# Initialize DB on first run
init_db()

# ---------------------------------------------------------------------------
# Session State Management
# ---------------------------------------------------------------------------
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "full_name" not in st.session_state:
    st.session_state.full_name = None

def login_user(username, password):
    conn = get_db_connection()
    user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    conn.close()
    
    if user and check_password_hash(user["password"], password):
        st.session_state.user_id = user["id"]
        st.session_state.username = user["username"]
        st.session_state.full_name = user["full_name"]
        return True
    return False

def signup_user(username, password, full_name):
    conn = get_db_connection()
    existing_user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
    
    if existing_user:
        conn.close()
        return False
        
    conn.execute(
        "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
        (username, generate_password_hash(password), full_name)
    )
    conn.commit()
    conn.close()
    return True

def logout_user():
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.full_name = None
    st.rerun()

# ---------------------------------------------------------------------------
# Authentication UI
# ---------------------------------------------------------------------------
if st.session_state.user_id is None:
    st.title("🎫 TrackIT System")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        with st.form("login_form"):
            login_username = st.text_input("Username")
            login_password = st.text_input("Password", type="password")
            submit_login = st.form_submit_button("Log In")
            
            if submit_login:
                if login_user(login_username, login_password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
                    
    with tab2:
        with st.form("signup_form"):
            signup_fullname = st.text_input("Full Name")
            signup_username = st.text_input("Username")
            signup_password = st.text_input("Password", type="password")
            submit_signup = st.form_submit_button("Sign Up")
            
            if submit_signup:
                if signup_user(signup_username, signup_password, signup_fullname):
                    st.success("Account created! Please log in.")
                else:
                    st.error("Username already exists.")
                    
    st.stop() # Stop execution until logged in

# ---------------------------------------------------------------------------
# Main App UI
# ---------------------------------------------------------------------------
st.sidebar.title(f"Welcome, {st.session_state.full_name}")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Tickets", "Create Ticket"])

if st.sidebar.button("Logout"):
    logout_user()

def get_user_names():
    conn = get_db_connection()
    rows = conn.execute("SELECT full_name FROM users ORDER BY full_name").fetchall()
    conn.close()
    return [r["full_name"] for r in rows]

if menu == "Dashboard":
    st.title("📊 Dashboard")
    conn = get_db_connection()
    
    total = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    open_c = conn.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Open'").fetchone()[0]
    progress = conn.execute("SELECT COUNT(*) FROM tickets WHERE status = 'In Progress'").fetchone()[0]
    resolved = conn.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Resolved'").fetchone()[0]
    closed = conn.execute("SELECT COUNT(*) FROM tickets WHERE status = 'Closed'").fetchone()[0]
    high = conn.execute("SELECT COUNT(*) FROM tickets WHERE priority = 'High'").fetchone()[0]
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tickets", total)
    col2.metric("Open", open_c)
    col3.metric("In Progress", progress)
    col4.metric("High Priority", high)
    
    st.subheader("Recent Tickets")
    recent = pd.read_sql_query("SELECT id, title, priority, status, assigned_to, created_at FROM tickets ORDER BY created_at DESC LIMIT 5", conn)
    st.dataframe(recent, use_container_width=True, hide_index=True)
    conn.close()

elif menu == "Tickets":
    st.title("🎫 Manage Tickets")
    conn = get_db_connection()
    
    col1, col2, col3 = st.columns(3)
    search = col1.text_input("Search by title/description")
    status_filter = col2.selectbox("Filter by Status", ["All", "Open", "In Progress", "Resolved", "Closed"])
    priority_filter = col3.selectbox("Filter by Priority", ["All", "Low", "Medium", "High"])
    
    query = "SELECT * FROM tickets WHERE 1=1"
    params = []
    
    if search:
        query += " AND (title LIKE ? OR description LIKE ?)"
        params.extend([f"%{search}%", f"%{search}%"])
    if status_filter != "All":
        query += " AND status = ?"
        params.append(status_filter)
    if priority_filter != "All":
        query += " AND priority = ?"
        params.append(priority_filter)
        
    query += " ORDER BY created_at DESC"
    
    tickets_df = pd.read_sql_query(query, conn, params=params)
    
    if not tickets_df.empty:
        # Display tickets as expanders to allow editing
        for index, row in tickets_df.iterrows():
            with st.expander(f"[{row['id']}] {row['title']} - {row['status']} ({row['priority']})"):
                st.write("**Description:**", row['description'])
                st.write(f"**Assigned To:** {row['assigned_to']} | **Created By:** {row['created_by']}")
                st.write(f"**Created At:** {row['created_at']}")
                
                # Edit functionality
                with st.form(f"edit_form_{row['id']}"):
                    st.write("Edit Ticket")
                    new_status = st.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], index=["Open", "In Progress", "Resolved", "Closed"].index(row['status']))
                    new_priority = st.selectbox("Priority", ["Low", "Medium", "High"], index=["Low", "Medium", "High"].index(row['priority']))
                    new_assigned = st.selectbox("Assign To", [""] + get_user_names(), index=([""] + get_user_names()).index(row['assigned_to']) if row['assigned_to'] in get_user_names() else 0)
                    
                    if st.form_submit_button("Update Ticket"):
                        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                        conn.execute(
                            "UPDATE tickets SET status=?, priority=?, assigned_to=?, updated_at=? WHERE id=?",
                            (new_status, new_priority, new_assigned, now, row['id'])
                        )
                        conn.commit()
                        st.success("Ticket updated!")
                        st.rerun()
                        
                if st.button("Delete Ticket", key=f"del_{row['id']}", type="primary"):
                    conn.execute("DELETE FROM tickets WHERE id=?", (row['id'],))
                    conn.commit()
                    st.warning("Ticket deleted!")
                    st.rerun()
    else:
        st.info("No tickets found.")
        
    conn.close()

elif menu == "Create Ticket":
    st.title("➕ Create New Ticket")
    
    with st.form("create_ticket_form"):
        title = st.text_input("Title")
        description = st.text_area("Description")
        col1, col2 = st.columns(2)
        priority = col1.selectbox("Priority", ["Low", "Medium", "High"], index=1)
        status = col2.selectbox("Status", ["Open", "In Progress", "Resolved", "Closed"], index=0)
        assigned_to = st.selectbox("Assign To", [""] + get_user_names())
        
        if st.form_submit_button("Create Ticket"):
            if title and description:
                conn = get_db_connection()
                now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                conn.execute(
                    """INSERT INTO tickets (title, description, priority, status, assigned_to, created_by, created_at, updated_at)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (title, description, priority, status, assigned_to, st.session_state.full_name, now, now)
                )
                conn.commit()
                conn.close()
                st.success("Ticket created successfully!")
            else:
                st.error("Title and Description are required.")
