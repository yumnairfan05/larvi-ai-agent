# 🤖 LARVI — Autonomous Personal AI Agent

> **An intelligent AI-powered personal assistant that understands natural-language commands and autonomously manages Gmail, Google Calendar, and Google Drive.**

LARVI is a modular **AI personal assistant** designed to interact with Google services through natural-language instructions.

Instead of manually opening Gmail or Google Calendar and performing repetitive actions, users can simply tell LARVI what they want.

For example:

```text
"Show my unread emails"

"Send an email to Sarah saying I'll join the meeting at 5 PM"

"Find my Team Meeting"

"Move my Team Meeting to tomorrow at 6 PM"

"Delete my appointment with Ahmed"

"Find my project report in Google Drive"
```

LARVI interprets the user's request, determines which service is required, extracts the intended action, executes the operation through the appropriate Google API, and returns the result to the user.

---

## ✨ Key Features

### 📧 Intelligent Gmail Management

LARVI can interact with Gmail using natural-language commands.

Supported operations include:

* View unread emails
* View recent emails
* Search emails
* Open specific emails
* Read full email content
* Summarize emails
* Send emails
* Delete/trash emails
* Extract sender, recipient, subject, date, and body
* Decode plain-text and HTML email content

Example:

```text
User:
Show my unread emails
```

LARVI:

```text
1. From: Sarah
   Subject: Project Meeting
   Date: ...

2. From: Ahmed
   Subject: Internship Update
   Date: ...
```

---

### 📅 Google Calendar Management

LARVI can manage calendar events using natural-language instructions.

Supported operations include:

* View upcoming events
* Find events
* Create events
* Update events
* Reschedule events
* Delete events
* Check calendar availability
* Handle event locations
* Handle event descriptions
* Automatically interpret relative dates
* Use Pakistan Standard Time (`Asia/Karachi`)

Example:

```text
Create a Team Meeting tomorrow at 5 PM for one hour.
```

LARVI converts the request into a structured calendar operation and creates the event through Google Calendar.

---

### 📁 Google Drive Integration

LARVI is designed to support Google Drive operations through the same agent architecture.

Planned/implemented Drive capabilities include:

* Search files
* Find documents
* Read files
* Create files
* Update files
* Delete files
* Manage Drive content through natural-language commands

Example:

```text
Find my project report in Drive.
```

---

### 🧠 Natural-Language Understanding

Users do not need to learn commands or syntax.

LARVI understands natural language such as:

```text
Check my inbox.

Read my latest emails.

Find emails from Sarah.

Send an email to Ahmed saying I'll call him tomorrow.

Show my upcoming meetings.

Find my Team Meeting.

Move my Team Meeting to Friday at 5 PM.

Delete my appointment tomorrow.
```

The system converts natural-language requests into structured actions before executing them.

---

### 🔀 Intelligent Request Routing

LARVI contains a Master Agent that determines which service should handle a request.

```text
                User
                  │
                  ▼
          ┌───────────────┐
          │     LARVI     │
          │  Master Agent │
          └───────┬───────┘
                  │
          Request Classification
                  │
       ┌──────────┼──────────┬──────────┐
       ▼          ▼          ▼          ▼
    EMAIL      CALENDAR     DRIVE     GENERAL
       │          │          │          │
       ▼          ▼          ▼          ▼
 Gmail Agent  Calendar     Drive      Ollama
              Agent        Agent       LLM
       │          │          │
       ▼          ▼          ▼
    Gmail API  Calendar API Drive API
```

This modular architecture makes LARVI easier to maintain, extend, and scale.

---

## 🏗️ System Architecture

LARVI follows a multi-agent architecture.

```text
┌──────────────────────────────┐
│            USER              │
│     Natural Language Input   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       FastAPI Backend        │
│          /chat API           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       LARVI Master Agent     │
│                              │
│    Request Classification    │
└──────────────┬───────────────┘
               │
       ┌───────┼────────┐
       │       │        │
       ▼       ▼        ▼
    Email   Calendar   Drive
    Agent     Agent    Agent
       │       │        │
       ▼       ▼        ▼
     Gmail   Calendar  Google
      API      API     Drive API
       │       │        │
       └───────┼────────┘
               │
               ▼
        Structured Result
               │
               ▼
        LARVI Response
               │
               ▼
              USER
```

---

# 🧩 Project Architecture

LARVI is organized into separate layers so that each component has a clear responsibility.

```text
LARVI/
│
├── frontend/
│   │
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── ...
│   │
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
├── backend/
│   │
│   ├── agents/
│   │   ├── master_agent.py
│   │   ├── email_agent.py
│   │   ├── calendar_agent.py
│   │   └── drive_agent.py
│   │
│   ├── services/
│   │   └── google_service.py
│   │
│   ├── tools/
│   │   ├── gmail_tools.py
│   │   ├── calendar_tools.py
│   │   └── drive_tools.py
│   │
│   ├── workflows/
│   │   ├── larvi_graph.py
│   │   └── conversation_state.py
│   │
│   ├── agent.py
│   ├── config.py
│   ├── google_auth.py
│   ├── main.py
│   ├── .env
│   ├── .env.example
│   ├── credentials.json
│   └── token.json
│
├── .gitignore
├── README.md
└── ...
```

---

# 🧠 Core Components

## Master Agent

The Master Agent acts as the central controller of LARVI.

Its responsibilities include:

* Receiving user requests
* Classifying requests
* Routing requests
* Coordinating specialized agents
* Returning structured responses

Supported categories:

```text
GENERAL
EMAIL
CALENDAR
DRIVE
```

---

## Email Agent

The Email Agent handles Gmail-specific operations.

It works with:

```text
Gmail Agent
      │
      ▼
Gmail Tools
      │
      ▼
Google Gmail API
```

The agent can determine whether the user wants to:

```text
read
recent
search
open
summarize
send
delete
```

---

## Calendar Agent

The Calendar Agent handles Google Calendar operations.

Supported actions:

```text
view
find
create
update
delete
```

Calendar operations use:

```text
Asia/Karachi
```

as the application's default timezone.

---

## Drive Agent

The Drive Agent handles Google Drive operations.

The architecture allows additional Drive capabilities to be added without modifying the Gmail or Calendar agents.

---

# 🧠 Conversation State

LARVI includes a conversation-state layer for maintaining short-term context.

This allows follow-up instructions such as:

```text
User:
Find my Team Meeting.

LARVI:
I found your Team Meeting.

User:
Move it to 7 PM.
```

Instead of treating the second message as a completely new request, LARVI can use the previously identified event information.

The conversation state can contain:

```text
Last category
Last action
Last user message
Last response
Email information
Calendar event information
Last search query
Additional context
```

---

# 🕒 Timezone Awareness

LARVI uses:

```text
Asia/Karachi
```

as its default timezone.

This allows natural-language expressions such as:

```text
today
tomorrow
Friday
5 PM
tomorrow at 6 PM
```

to be interpreted using Pakistan's local date and time.

---

# 🔐 Google OAuth Authentication

LARVI uses Google OAuth 2.0 to securely connect to Google services.

The application requests access for:

```text
Gmail
Google Calendar
Google Drive
```

The authentication flow is:

```text
User
 │
 ▼
/auth/google
 │
 ▼
Google OAuth
 │
 ▼
User grants permission
 │
 ▼
/auth/google/callback
 │
 ▼
OAuth credentials
 │
 ▼
token.json
```

Once authenticated, LARVI can use the stored credentials for subsequent Google API operations.

---

# 🔑 Environment Variables

Create a `.env` file inside the backend directory.

Example:

```env
OLLAMA_API_KEY=your_ollama_api_key
OLLAMA_MODEL=gpt-oss:20b
OLLAMA_URL=https://ollama.com/api/chat

GOOGLE_CLIENT_SECRET_FILE=credentials.json
GOOGLE_TOKEN_FILE=token.json

GOOGLE_CALENDAR_ID=primary
GMAIL_USER_ID=me

BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

FRONTEND_URL=http://localhost:5173

MAX_EMAIL_RESULTS=10
MAX_CALENDAR_RESULTS=10
MAX_DRIVE_RESULTS=10
```

### ⚠️ Never commit secrets

Do **not** upload the following files to GitHub:

```text
.env
credentials.json
token.json
```

Make sure they are included in `.gitignore`.

---

# 🛠️ Technology Stack

## Frontend

* React
* Vite
* JavaScript
* HTML
* CSS

## Backend

* Python
* FastAPI
* Uvicorn
* Requests

## AI

* Ollama Cloud API
* `gpt-oss:20b`

## Google Services

* Gmail API
* Google Calendar API
* Google Drive API
* Google OAuth 2.0

## Architecture

* Multi-Agent Architecture
* Modular Agent Design
* Natural-Language Command Parsing
* Conversation State
* API-based Tool Execution

---

# 🚀 Installation

## 1. Clone the repository

```bash
git clone https://github.com/your-username/larvi.git
```

Move into the project:

```bash
cd larvi
```

---

# ⚙️ Backend Setup

Move into the backend:

```bash
cd backend
```

Create a virtual environment:

### Windows

```bash
py -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Configure Google OAuth

Create a Google Cloud project and enable:

```text
Gmail API
Google Calendar API
Google Drive API
```

Create OAuth credentials and download:

```text
credentials.json
```

Place it inside:

```text
backend/
```

---

# 🤖 Configure Ollama

Add your Ollama API key to `.env`:

```env
OLLAMA_API_KEY=your_api_key
```

Set the model:

```env
OLLAMA_MODEL=gpt-oss:20b
```

---

# ▶️ Run the Backend

From the backend directory:

```bash
py -m uvicorn main:app --reload --port 8000
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

Test the root endpoint:

```text
http://127.0.0.1:8000/
```

Expected response:

```json
{
  "message": "LARVI AI Agent backend is running"
}
```

---

# 🎨 Run the Frontend

Open another terminal.

Move into the frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm.cmd run dev
```

The frontend will normally run at:

```text
http://localhost:5173
```

---

# 🔗 API

## POST `/chat`

Send a natural-language command to LARVI.

### Request

```json
{
  "message": "Show my unread emails"
}
```

### Response

```json
{
  "category": "EMAIL",
  "response": "Here are your unread emails..."
}
```

---

# 🔐 Authentication Endpoints

## Start Google Authentication

```text
GET /auth/google
```

## OAuth Callback

```text
GET /auth/google/callback
```

After successful authentication, the application stores the OAuth token locally.

---

# 🧪 Example Commands

### Gmail

```text
Show my unread emails
```

```text
Show my latest emails
```

```text
Find emails from Sarah
```

```text
Open the email from Ahmed
```

```text
Summarize my latest email
```

```text
Send an email to Sarah saying I'll join the meeting at 5 PM
```

```text
Delete the email about the project
```

---

### Calendar

```text
Show my upcoming events
```

```text
Find my Team Meeting
```

```text
Create a meeting tomorrow at 5 PM
```

```text
Schedule a project meeting on Friday at 4 PM
```

```text
Move my Team Meeting to 7 PM
```

```text
Delete my Team Meeting
```

---

### Google Drive

```text
Find my project report in Drive
```

```text
Search Drive for LARVI
```

```text
Find my internship document
```

---

### General AI

```text
Explain machine learning.
```

```text
What is Python?
```

```text
Help me understand APIs.
```

```text
Write a professional email.
```

---

# 🛡️ Reliability & Safety

LARVI is designed to avoid falsely claiming that an external action was completed.

For example, if Google Calendar fails to create an event, LARVI should return an appropriate failure response instead of saying:

```text
Event created successfully.
```

This principle is applied throughout the architecture:

```text
User Request
     │
     ▼
Interpret Request
     │
     ▼
Execute Real Tool
     │
     ├──── Success ────► Confirm action
     │
     └──── Failure ────► Report failure
```

LARVI does not intentionally invent:

* Email addresses
* Message IDs
* Calendar event IDs
* Google Drive file IDs
* Successful external actions

---

# 📂 Modular Design

One of LARVI's main design goals is extensibility.

New capabilities can be added as independent agents and tools.

For example:

```text
agents/
│
├── master_agent.py
├── email_agent.py
├── calendar_agent.py
├── drive_agent.py
├── task_agent.py
└── web_agent.py
```

The same architecture can later support:

* Task management
* WhatsApp
* Slack
* Notion
* Weather
* News
* Web search
* Reminders
* Productivity automation

without rewriting the entire application.

---

# 🔄 Request Processing Pipeline

Every request follows a structured pipeline.

```text
1. User enters command
          ↓
2. FastAPI receives request
          ↓
3. Master Agent receives message
          ↓
4. Request is classified
          ↓
5. Appropriate agent selected
          ↓
6. Natural language converted
   into structured command
          ↓
7. Tool executes API operation
          ↓
8. Result returned
          ↓
9. LARVI generates response
          ↓
10. Response displayed to user
```

---

# 📈 Future Improvements

Planned improvements include:

* [ ] Full Google Drive agent
* [ ] Persistent conversation memory
* [ ] Multi-user authentication
* [ ] Better intent classification
* [ ] Improved entity extraction
* [ ] Email reply support
* [ ] Email forwarding
* [ ] Email drafting
* [ ] Calendar conflict resolution
* [ ] Recurring event support
* [ ] File creation and editing
* [ ] Voice input
* [ ] Voice responses
* [ ] Mobile interface
* [ ] Long-term memory
* [ ] Advanced agent planning
* [ ] Background task automation
* [ ] Production deployment
* [ ] Improved authentication and authorization

---

# 🎯 Project Goals

LARVI is designed around four core principles:

### 1. Natural Interaction

Users should be able to communicate naturally instead of learning commands.

### 2. Autonomous Execution

LARVI should perform real actions through connected services rather than simply explaining how to perform them.

### 3. Modular Architecture

Each service should have its own agent and tool layer.

### 4. Honest Responses

LARVI should only report an action as successful when the underlying tool actually succeeds.

---

# 👩‍💻 Development

The project is designed to be easy to extend.

When adding a new Google service:

```text
1. Create service/tool functions
2. Create a specialized agent
3. Add request classification
4. Add workflow routing
5. Add conversation-state support
6. Test API integration
7. Connect the frontend
```

This keeps the system maintainable as the number of capabilities grows.

---

# 🧪 Testing

Before using LARVI in production, test each integration independently.

### Gmail

```text
Show my unread emails
```

```text
Find emails from test@example.com
```

```text
Send an email to test@example.com
```

### Calendar

```text
Show my upcoming events
```

```text
Create a test event tomorrow at 5 PM
```

```text
Find my test event
```

```text
Delete my test event
```

### General AI

```text
Explain artificial intelligence.
```

---

# ⚠️ Security Notice

This project uses OAuth credentials and API keys.

Never commit:

```text
.env
credentials.json
token.json
```

to a public repository.

If a secret is accidentally exposed:

1. Revoke the exposed credential.
2. Generate a new credential.
3. Update your `.env`.
4. Remove the secret from Git history if necessary.

---

# 📜 License

This project is intended for educational, portfolio, and development purposes.

A formal open-source license can be added depending on the project's distribution requirements.

---

# 🌟 Why LARVI?

Traditional productivity applications require users to manually navigate multiple interfaces.

LARVI aims to provide a unified natural-language interface:

```text
              ┌──────────────────────┐
              │        LARVI         │
              │                      │
              │  One AI Interface    │
              └──────────┬───────────┘
                         │
             ┌───────────┼───────────┐
             │           │           │
             ▼           ▼           ▼
           Gmail      Calendar     Drive
```

Instead of:

```text
Open Gmail
   ↓
Find email
   ↓
Read email
   ↓
Open Calendar
   ↓
Find meeting
   ↓
Change meeting
   ↓
Open Drive
   ↓
Find document
```

the goal is simply:

```text
"Handle this for me."
```

---

# 🚀 LARVI

**LARVI — Your AI-powered personal productivity assistant.**

> **Think it. Tell LARVI. Get it done.**

```
```