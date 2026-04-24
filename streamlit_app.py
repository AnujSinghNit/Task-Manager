"""
TrackIT – Task Manager (Streamlit Cloud Edition)
=================================================
A Streamlit-based task management system for cloud deployment.
"""

import streamlit as st
import sqlite3
import os
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

# ---------------------------------------------------------------------------
st.set_page_config(page_title="TrackIT - Task Manager", page_icon="🎫", layout="wide")

DB_PATH = os.path.join(os.getcwd(), "database.db")


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
            ("john", generate_password_hash("john123"), "John Smith", "developer"),
            ("sarah", generate_password_hash("sarah123"), "Sarah Connor", "support"),
        ]
        conn.executemany(
            "INSERT INTO users (username, password, full_name, role) VALUES (?, ?, ?, ?)",
            users,
        )

        # Sample tickets
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        sample_tickets = [
            ("Login Page Returns 500 Error", "Users report a 500 error on invalid credentials.", "High", "Open", "John Smith", "Admin User", now, now),
            ("REST API Timeout on /api/v2/reports", "The reports endpoint times out after 30 seconds.", "High", "In Progress", "Sarah Connor", "Admin User", now, now),
            ("Database Connection Pool Exhaustion", "Connection pool exhausted during peak traffic.", "High", "Open", "John Smith", "Admin User", now, now),
            ("Dashboard Chart Tooltip Overlaps", "Tooltips overflow on mobile screens.", "Medium", "In Progress", "Admin User", "John Smith", now, now),
            ("Payment Gateway Duplicate IDs", "Stripe returns duplicate transaction IDs.", "High", "Open", "Sarah Connor", "Admin User", now, now),
            ("CSV Export Missing Headers", "Custom field headers missing in CSV export.", "Low", "Closed", "John Smith", "Sarah Connor", now, now),
        ]
        conn.executemany(
            """INSERT INTO tickets (title, description, priority, status, assigned_to, created_by, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            sample_tickets,
        )
        conn.commit()
    conn.close()


# Initialize DB on first run
init_db()


# ---------------------------------------------------------------------------
# Session State
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "full_name" not in st.session_state:
    st.session_state.full_name = None


def login_user(username, password):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user["password"], password):
        st.session_state.user_id = user["id"]
        st.session_state.username = user["username"]
        st.session_state.full_name = user["full_name"]
        return True
    return False


def signup_user(username, password, full_name):
    conn = get_db_connection()
    existing = conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()

    if existing:
        conn.close()
        return False

    conn.execute(
        "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
        (username, generate_password_hash(password), full_name),
    )
    conn.commit()
    conn.close()
    return True


def logout_user():
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.full_name = None
    st.rerun()


def get_user_names():
    conn = get_db_connection()
    rows = conn.execute("SELECT full_name FROM users ORDER BY full_name").fetchall()
    conn.close()
    return [r["full_name"] for r in rows]


# ---------------------------------------------------------------------------
# LOGIN / SIGNUP SCREEN
# ---------------------------------------------------------------------------
if st.session_state.user_id is None:
    st.title("🎫 TrackIT - Task Manager")
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

    st.stop()

# ---------------------------------------------------------------------------
# MAIN APP (after login)
# ---------------------------------------------------------------------------
st.sidebar.title(f"Welcome, {st.session_state.full_name}")
menu = st.sidebar.radio("Navigation", ["Dashboard", "Tickets", "Create Ticket"])

if st.sidebar.button("Logout"):
    logout_user()

# ---------------------------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------------------------
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
    recent = pd.read_sql_query(
        "SELECT id, title, priority, status, assigned_to, created_at FROM tickets ORDER BY created_at DESC LIMIT 5",
        conn,
    )
    st.dataframe(recent, width="stretch", hide_index=True)
    conn.close()

# ---------------------------------------------------------------------------
# TICKETS LIST
# ---------------------------------------------------------------------------
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
        for index, row in tickets_df.iterrows():
            with st.expander(f"[{row['id']}] {row['title']} - {row['status']} ({row['priority']})"):
                st.write("**Description:**", row["description"])
                st.write(f"**Assigned To:** {row['assigned_to']} | **Created By:** {row['created_by']}")
                st.write(f"**Created At:** {row['created_at']}")

                with st.form(f"edit_form_{row['id']}"):
                    st.write("Edit Ticket")
                    statuses = ["Open", "In Progress", "Resolved", "Closed"]
                    priorities = ["Low", "Medium", "High"]
                    user_names = get_user_names()

                    new_status = st.selectbox(
                        "Status", statuses,
                        index=statuses.index(row["status"]) if row["status"] in statuses else 0,
                    )
                    new_priority = st.selectbox(
                        "Priority", priorities,
                        index=priorities.index(row["priority"]) if row["priority"] in priorities else 1,
                    )
                    assign_options = [""] + user_names
                    new_assigned = st.selectbox(
                        "Assign To", assign_options,
                        index=assign_options.index(row["assigned_to"]) if row["assigned_to"] in assign_options else 0,
                    )

                    if st.form_submit_button("Update Ticket"):
                        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
                        conn.execute(
                            "UPDATE tickets SET status=?, priority=?, assigned_to=?, updated_at=? WHERE id=?",
                            (new_status, new_priority, new_assigned, now, row["id"]),
                        )
                        conn.commit()
                        st.success("Ticket updated!")
                        st.rerun()

                if st.button("Delete Ticket", key=f"del_{row['id']}", type="primary"):
                    conn.execute("DELETE FROM tickets WHERE id=?", (row["id"],))
                    conn.commit()
                    st.warning("Ticket deleted!")
                    st.rerun()
    else:
        st.info("No tickets found.")

    conn.close()

# ---------------------------------------------------------------------------
# CREATE TICKET  (FIX: this block was incorrectly indented in the original)
# ---------------------------------------------------------------------------
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
                    (title, description, priority, status, assigned_to, st.session_state.full_name, now, now),
                )
                conn.commit()
                conn.close()
                st.success("Ticket created successfully!")
            else:
                st.error("Title and Description are required.")
