# Personalized Networking Assistant

AI-powered web app that generates tailored conversation starters for networking events,
fact-checks topics against Wikipedia, and logs your interaction history with feedback.

**Stack:** FastAPI + SQLAlchemy (SQLite) backend · Google Gemini for theme extraction &
starter generation · Wikipedia REST API for fact-checking · Vanilla HTML/CSS/JS multi-page
frontend (served directly by FastAPI — no separate frontend server needed).

---

## 1. Prerequisites

- Python 3.10 or 3.11 (**recommended: 3.11** — some ML-adjacent packages have issues on 3.14)
- VS Code
- A free Google Gemini API key: https://aistudio.google.com/apikey
- Internet connection (for Gemini + Wikipedia calls)

---

## 2. Project structure

```
networking-assistant/
├── backend/
│   ├── main.py                  # FastAPI app + all routes + serves frontend
│   ├── database.py              # SQLAlchemy engine/session setup
│   ├── models.py                # DB tables: UserProfile, Interaction, Feedback, FactCheckLog
│   ├── schemas.py                # Pydantic request/response models
│   ├── services/
│   │   ├── gemini_service.py    # Calls Gemini for themes + starters
│   │   └── wikipedia_service.py # Wikipedia search + summary lookup
│   ├── requirements.txt
│   └── .env.example             # Copy to .env and add your Gemini key
└── frontend/
    ├── index.html                # Landing page
    ├── generate.html             # Generate starters form + results
    ├── verify.html                # Wikipedia fact-check tool
    ├── history.html               # Past interactions + feedback
    ├── css/style.css
    └── js/ (api.js, generate.js, verify.js, history.js, network-graph.js)
```

---

## 3. Setup — step by step (VS Code terminal)

### Step 1 — Open the project
Open the `networking-assistant` folder in VS Code (`File → Open Folder…`).

### Step 2 — Create a virtual environment (Python 3.11)
Open a VS Code terminal (`` Ctrl+` ``) and run:

```bash
cd backend
python3.11 -m venv venv
```

Activate it:
- **macOS/Linux:** `source venv/bin/activate`
- **Windows (PowerShell):** `venv\Scripts\Activate.ps1`
- **Windows (cmd):** `venv\Scripts\activate.bat`

You should see `(venv)` at the start of your terminal prompt.

> If `python3.11` isn't found, install Python 3.11 first, or use whatever 3.10/3.11 command
> is available on your system (e.g. `py -3.11` on Windows).

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Add your Gemini API key

```bash
cp .env.example .env        # macOS/Linux
copy .env.example .env      # Windows
```

Open `.env` and paste your key:

```
GEMINI_API_KEY=AIza...your_real_key_here
GEMINI_MODEL=gemini-2.0-flash
DATABASE_URL=sqlite:///./networking_assistant.db
```

> If `gemini-2.0-flash` isn't available on your key/account, check
> https://ai.google.dev/gemini-api/docs/models for the current model name and
> update `GEMINI_MODEL` accordingly — the code doesn't need to change.

### Step 5 — Run the app

Still inside `backend/` with the venv active:

```bash
uvicorn main:app --reload
```

You should see:
```
Uvicorn running on http://127.0.0.1:8000
```

### Step 6 — Open it in your browser

Go to **http://127.0.0.1:8000/** — that's it. The FastAPI backend serves the entire
frontend directly, so there's nothing else to start.

- `/` — Home
- `/generate.html` — Generate conversation starters
- `/verify.html` — Wikipedia fact check
- `/history.html` — Past sessions + feedback
- `/docs` — Auto-generated interactive API docs (Swagger UI)

The SQLite database file (`networking_assistant.db`) is created automatically in `backend/`
on first run — no manual database setup needed.

---

## 4. API endpoints (for reference / grading)

| Method | Path | Purpose |
|---|---|---|
| POST | `/api/v1/generate` | Takes bio + event description + interests → returns themes & 3 conversation starters, logs the interaction |
| GET | `/api/v1/verify?query=...` | Looks up a topic on Wikipedia, returns a summary + source link |
| POST | `/api/v1/feedback` | Marks an interaction's starters as useful / not useful |
| GET | `/api/v1/history` | Returns the 50 most recent interactions with themes, starters, and feedback |
| GET | `/api/health` | Health check |

Example request body for `/api/v1/generate`:
```json
{
  "name": "Sowji",
  "bio": "Final-year CS student focused on NLP and applied AI.",
  "event_description": "AI for Sustainable Cities — a panel on AI in urban planning and climate resilience.",
  "interests": "climate change, urban planning"
}
```

---

## 5. Mapping to the architecture diagram

The original architecture (Streamlit + local DistilBERT/GPT-2 + separate frontend) was
simplified into a leaner, equally real-world stack for faster, more reliable delivery:

| Diagram component | This build |
|---|---|
| Streamlit Web Application | Multi-page HTML/CSS/JS, served by FastAPI |
| FastAPI Backend Service (API Endpoints, Orchestration) | `backend/main.py` |
| DistilBERT (theme classification) + GPT-2 (text generation) | Single Gemini API call doing both theme extraction and starter generation (`services/gemini_service.py`) — avoids heavy local model downloads while keeping the same functional role |
| Fact Verification Module + Wikipedia Search API | `services/wikipedia_service.py` |
| Local Data Store (User Profiles, Interaction Logs) | SQLite via SQLAlchemy (`models.py`) |

This keeps every functional block from the diagram (input → generation → fact-check →
storage → history/feedback) while being something you can actually run and demo today.

---

## 6. Troubleshooting

- **`ModuleNotFoundError`** → make sure the venv is activated and you ran `pip install -r requirements.txt` from inside `backend/`.
- **`GEMINI_API_KEY is not set`** → check `.env` exists in `backend/` (not `.env.example`) and has a real key, then restart `uvicorn`.
- **Wikipedia fact check returns "not found" for everything** → check your internet connection; some sandboxed/restricted networks block `en.wikipedia.org`.
- **Port 8000 already in use** → run `uvicorn main:app --reload --port 8001` and open `http://127.0.0.1:8001/` instead.
- **Python 3.14 dependency errors** → this is a known issue with several ML-adjacent packages; use Python 3.10 or 3.11 for the venv as shown in Step 2.

---

## 7. Demo Video

Watch the complete project demonstration here:

▶️ **[Click here to watch the demo video](https://drive.google.com/file/d/14L1BGqLOZ3P0-5h9RcTzTCjckrctV8TZ/view?usp=drivesdk)**

## 8. Screenshots

### Home Page
![Home](outputs/home.png)

### Generate Conversation Starters
![Generate](outputs/generate.png)

### Fact Verification
![Verify](outputs/verify.png)

### Interaction History
![History](outputs/history.png)

## 9. Features

- AI-powered conversation starter generation
- Personalized networking recommendations
- Wikipedia-based fact verification
- Interaction history tracking
- User feedback logging
- FastAPI REST APIs
- Responsive multi-page frontend

## 10. Technologies Used

### Frontend
- HTML5
- CSS3
- JavaScript

### Backend
- Python
- FastAPI
- SQLAlchemy
- SQLite

### AI & APIs
- Google Gemini API
- Wikipedia REST API

## 11. For your submission / demo

- **GitHub:** push this whole `networking-assistant/` folder as your repo root.
- **Demo:** run Step 5 and record/demo `http://127.0.0.1:8000/` locally, walking through
  Scenario 1 (Generate), Scenario 2 (Fact check), Scenario 3 (History).
- Do **not** commit your real `.env` file — only `.env.example` should go to GitHub. Add
  `.env` and `venv/` to a `.gitignore` (see below).

`.gitignore` suggestion:
```
venv/
__pycache__/
*.db
.env
```
##  Author

**Patchara Devi Venkata Sowjanya**

##  License

This project is developed for academic and educational purposes.

