# 🎫 TrackIT – Ticket Management System (Issue Tracker)

A **full-stack web application** built for software teams and production support teams to **create, track, assign, and resolve** support tickets efficiently.

> Built with Python Flask, SQLite, HTML/CSS/JS — beginner-friendly and interview-ready.

---

## 📌 What This Project Does

Imagine you work in a software company. Users report bugs like:
- "Login page is broken"
- "Payment is failing"
- "App crashes on mobile"

Your team needs a system to **track all these problems**. That's exactly what TrackIT does!

With TrackIT you can:
- ✅ **Create** a new ticket when a problem is reported
- ✅ **View** all tickets in a clean table
- ✅ **Edit** a ticket to update its status or assign it to someone
- ✅ **Delete** a ticket when it's no longer needed
- ✅ **Search** tickets by title or keyword
- ✅ **Filter** tickets by status (Open, In Progress, etc.) or priority (High, Medium, Low)
- ✅ **Dashboard** to see a quick summary of all tickets at a glance

---

## 🛠️ Tech Stack (What Tools Are Used)

| Tool | What It Does |
|------|-------------|
| **Python** | The programming language used for backend logic |
| **Flask** | A lightweight Python web framework that handles routes and pages |
| **SQLite** | A simple file-based database (no setup needed!) |
| **Jinja2** | Template engine that lets us mix Python with HTML |
| **HTML** | Creates the structure of web pages |
| **CSS** | Makes the pages look beautiful (colors, layout, fonts) |
| **JavaScript** | Adds interactivity (animations, form validation) |

---

## 📁 Project Structure (What Each File Does)

```
Ticket Management System (Issue Tracker)/
│
├── app.py                  ← 🧠 The BRAIN of the project (all backend logic)
├── requirements.txt        ← 📦 Lists the Python packages needed
├── database.db             ← 💾 The database file (auto-created when you run the app)
├── README.md               ← 📖 This file you're reading right now
│
├── templates/              ← 🎨 HTML pages (what the user sees)
│   ├── base.html           ← The main layout (sidebar, header) — every page uses this
│   ├── login.html          ← Login page
│   ├── dashboard.html      ← Dashboard with stats and recent tickets
│   ├── tickets.html        ← Shows all tickets in a table with filters
│   ├── create_ticket.html  ← Form to create a new ticket
│   ├── edit_ticket.html    ← Form to edit an existing ticket
│   └── ticket_detail.html  ← Shows full details of one ticket
│
└── static/                 ← 🎨 CSS and JavaScript files
    ├── style.css           ← All the styling (dark theme, colors, layout)
    └── script.js           ← Client-side logic (sidebar toggle, form validation)
```

---

## 🏗️ How The App Works (Architecture – Simple Explanation)

```
   👤 User (Browser)
       │
       │  Clicks a link or submits a form
       ▼
   🌐 Flask (app.py)
       │
       │  Receives the request → Decides what to do
       │  Example: User visits /tickets → Flask runs the tickets() function
       ▼
   💾 SQLite (database.db)
       │
       │  Flask asks the database for data
       │  Example: "Give me all tickets where status = Open"
       ▼
   🧠 Flask gets the data back
       │
       │  Puts the data into an HTML template using Jinja2
       │  Example: Fills tickets.html with ticket rows
       ▼
   📄 HTML Page is sent back to the browser
       │
       │  Browser displays the beautiful page
       ▼
   👤 User sees the result!
```

### In Even Simpler Words:

1. **User clicks something** → Browser sends a request to Flask
2. **Flask handles it** → Reads/writes data from the database
3. **Flask fills an HTML template** → Puts real data into the page
4. **Page is sent back** → User sees the updated page

---

## 🗄️ Database Tables (Where Data Is Stored)

### Users Table
Stores login information for all users.

| Column | What It Stores | Example |
|--------|---------------|---------|
| id | Unique number for each user | 1 |
| username | Login username | admin |
| password | Encrypted password | (hashed value) |
| full_name | Display name | Admin User |
| role | User's role | admin, developer, support |
| created_at | When the account was created | 2026-04-23 |

### Tickets Table
Stores all the support tickets.

| Column | What It Stores | Example |
|--------|---------------|---------|
| id | Unique ticket number | 1 |
| title | Short summary of the issue | "Login Page Returns 500 Error" |
| description | Detailed explanation | "Users report a 500 error when..." |
| priority | How urgent it is | Low, Medium, High |
| status | Current state | Open, In Progress, Resolved, Closed |
| assigned_to | Who is working on it | John Smith |
| created_by | Who reported it | Admin User |
| created_at | When it was created | 2026-04-23 04:21 PM |
| updated_at | When it was last modified | 2026-04-23 05:30 PM |

---

## 🚀 How to Run This Project

### Step 1: Make sure Python is installed
```bash
python --version
```
You should see something like `Python 3.10.x` or higher.

### Step 2: Install required packages
```bash
pip install -r requirements.txt
```
This installs Flask (the web framework).

### Step 3: Run the application
```bash
python app.py
```
You'll see:
```
 * Running on http://127.0.0.1:5000
```

### Step 4: Open in browser
Go to: **http://127.0.0.1:5000**

### Step 5: Login
```
Username: admin
Password: admin
```

That's it! You're now inside the TrackIT dashboard. 🎉

---

## 👥 Demo Users Available

| Username | Password | Role |
|----------|----------|------|
| admin | admin | Admin |
| john | john123 | Developer |
| sarah | sarah123 | Support |
| mike | mike123 | Developer |
| lisa | lisa123 | Tester |

---

## 📋 Sample Tickets (Pre-loaded)

The app comes with **8 realistic tickets** already loaded:

1. 🔴 Login Page Returns 500 Error on Invalid Credentials
2. 🔴 REST API Timeout on /api/v2/reports Endpoint
3. 🔴 Database Connection Pool Exhaustion Under Load
4. 🟡 Dashboard Chart Tooltip Overlaps on Mobile Devices
5. 🔴 Payment Gateway Returns Duplicate Transaction IDs
6. 🔵 User Profile Avatar Upload Fails for PNG Files > 2 MB
7. 🟡 Notification Emails Sent in Wrong Timezone
8. 🔵 CSV Export Missing Header Row for Custom Fields

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔐 Login/Logout | Session-based authentication with password hashing |
| 📊 Dashboard | Stats cards showing ticket counts by status and priority |
| ➕ Create Ticket | Form with title, description, priority, status, assignee |
| 👁️ View Ticket | Detailed view with all metadata |
| ✏️ Edit Ticket | Update any ticket field |
| 🗑️ Delete Ticket | Remove tickets with confirmation prompt |
| 🔍 Search | Search tickets by title or keyword |
| 🎛️ Filters | Filter by status and priority |
| 📄 Pagination | 8 tickets per page |
| 🌙 Dark Theme | Modern professional dark UI |
| 📱 Responsive | Works on mobile, tablet, and desktop |

---

## 🎯 Interview Talking Points

If you present this project in an interview, here's what you can say:

1. **"I built a full-stack ticket management system using Flask and SQLite"**
2. **"It has complete CRUD operations"** — Create, Read, Update, Delete
3. **"I implemented session-based authentication with password hashing"**
4. **"The frontend uses a responsive dark theme with CSS Grid and Flexbox"**
5. **"I used Jinja2 templates for server-side rendering"**
6. **"It has search, filtering, and pagination for handling large datasets"**
7. **"The database auto-seeds with sample data on first run"**
8. **"I focused on clean code with comments and proper project structure"**

---

## 📝 License

This project is for educational and interview purposes.

---

**Made with ❤️ using Python Flask**
