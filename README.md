# Campus Fix — Express + Flask + Docker

Campus Fix is a simple campus issue-reporting application built with a **Node.js and Express frontend** and a **Python Flask backend**. Users can submit an issue through a web form; Express forwards the request to Flask, which validates the input and stores submissions as JSON.

Repository: https://github.com/Zayann7/the-campus-fix

## Features

- Form for reporting campus issues
- Express serves the frontend and forwards submissions to Flask
- Flask validates form fields and generates a submission reference ID
- Submissions are stored in a JSON file
- Dockerfiles for both services
- Docker Compose configuration to build and run the full application
- Named Docker volume to persist submission data across container recreations
- Health-check endpoint for the Flask backend

## Tech stack

- HTML, CSS, JavaScript
- Node.js and Express
- Python and Flask
- Docker and Docker Compose

## Project structure

```text
Campus-fix/
├── .gitignore
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   ├── server.js
│   └── public/
│       ├── index.html
│       ├── style.css
│       └── script.js
└── backend/
    ├── Dockerfile
    ├── app.py
    └── requirements.txt
```

The Flask application creates `submissions.json` when a form is submitted. In Docker Compose, the file is stored at `/data/submissions.json` inside the backend container and backed by the `backend_data` named volume.

## Run with Docker Compose (recommended)

Make sure Docker Desktop (or Docker Engine with the Compose plugin) is running. From the project root—the directory containing `docker-compose.yml`—run:

```bash
docker compose up -d --build
```

Check the containers:

```bash
docker compose ps
```

Follow the logs:

```bash
docker compose logs -f
```

Open the application:

- **Frontend:** http://localhost:3000
- **Frontend-to-backend health check:** http://localhost:3000/api/health
- **Flask health endpoint:** http://localhost:5000/health
- **Saved submissions (development/testing):** http://localhost:5000/submissions

To stop the containers:

```bash
docker compose down
```

The named volume preserves submission data when containers are stopped or recreated. To remove the containers **and delete the stored submission data**, run:

```bash
docker compose down -v
```

## Run locally without Docker

Run the backend and frontend in separate terminals.

### 1. Start the Flask backend

From the project root:

**Windows PowerShell**

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

**Linux / macOS / Git Bash**

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

The Flask backend listens on http://localhost:5000.

### 2. Start the Express frontend

In a second terminal, from the project root:

```bash
cd frontend
npm install
npm start
```

Use **Node.js 18 or newer**, since the Express server uses the built-in `fetch` API. Open http://localhost:3000 in your browser.

When running both services directly on your computer, Express uses `http://127.0.0.1:5000` as the default Flask backend URL. You can override it with the `FLASK_BACKEND_URL` environment variable if needed.

## Request flow

1. The user fills out the form in the browser.
2. `frontend/public/script.js` sends a JSON request to Express at `POST /api/submit`.
3. Express forwards the JSON payload to the Flask service at `POST /submit`.
4. Flask validates the fields, generates a reference ID and timestamp, and saves the submission.
5. Flask returns a JSON response to Express, and the frontend displays the result.

In Docker Compose, Express reaches Flask using the Compose service name `backend` at `http://backend:5000`. The browser only sends requests to Express, so a browser-side CORS configuration is not required for this flow.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/health` | Express checks the Flask health endpoint |
| `POST` | `/api/submit` | Express receives the form submission and forwards it to Flask |
| `GET` | `/health` | Flask health check |
| `POST` | `/submit` | Flask validates and stores a submission |
| `GET` | `/submissions` | Returns all stored submissions for development/testing |

### Example submission payload

```json
{
  "name": "Example Student",
  "email": "student@example.com",
  "category": "Electrical",
  "location": "Building A, Room 12",
  "description": "The lights are not working."
}
```

A successful submission returns a JSON response containing `success`, a message, and the generated submission details, including an ID and timestamp.

## Configuration

The Compose configuration sets these environment variables:

| Variable | Purpose | Compose value |
|---|---|---|
| `FLASK_BACKEND_URL` | URL Express uses to reach Flask | `http://backend:5000` |
| `PORT` | Express listening port | `3000` |
| `DATA_FILE` | File path Flask uses for submission storage | `/data/submissions.json` |

## Important security note

This is an assignment/demo project. The `/submissions` endpoint returns stored form submissions without authentication. Do not expose it publicly or use it with real personal information in production without adding authentication, authorization, stronger validation, and appropriate data protection.
