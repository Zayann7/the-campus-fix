from flask import Flask, request, jsonify
from datetime import datetime, timezone
import json
import os
import uuid

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.environ.get(
    "DATA_FILE",
    os.path.join(BASE_DIR, "submissions.json")
)

REQUIRED_FIELDS = [
    "name",
    "email",
    "category",
    "location",
    "description"
]


def load_submissions():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError("Stored submissions must be a JSON list.")

    return data


def save_submissions(submissions):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            submissions,
            file,
            indent=4,
            ensure_ascii=False
        )


@app.get("/health")
def health():
    return jsonify({
        "success": True,
        "message": "Flask backend is running."
    }), 200


@app.post("/submit")
def submit_form():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({
            "success": False,
            "message": "A valid JSON request body is required."
        }), 400

    # Extract and clean the input fields
    cleaned_data = {}

    for field in REQUIRED_FIELDS:
        value = payload.get(field, "")

        cleaned_data[field] = (
            str(value).strip() if value is not None else ""
        )

    # Validate required fields
    missing_fields = [
        field
        for field, value in cleaned_data.items()
        if not value
    ]

    if missing_fields:
        return jsonify({
            "success": False,
            "message": "Please fill in all required fields.",
            "missing_fields": missing_fields
        }), 400

    # Basic email validation
    email = cleaned_data["email"]

    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        return jsonify({
            "success": False,
            "message": "Please enter a valid email address."
        }), 400

    # Create the submission record
    submission = {
        "id": uuid.uuid4().hex[:8].upper(),
        **cleaned_data,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    try:
        submissions = load_submissions()
        submissions.append(submission)
        save_submissions(submissions)

    except (OSError, ValueError, json.JSONDecodeError) as error:
        app.logger.error("Could not save submission: %s", error)

        return jsonify({
            "success": False,
            "message": "The server could not save your submission."
        }), 500

    return jsonify({
        "success": True,
        "message": "Your request was submitted successfully.",
        "submission": submission
    }), 201


@app.get("/submissions")
def get_submissions():
    """Return all saved submissions for local assignment testing."""

    try:
        submissions = load_submissions()

    except (OSError, ValueError, json.JSONDecodeError) as error:
        app.logger.error("Could not read submissions: %s", error)

        return jsonify({
            "success": False,
            "message": "Could not read saved submissions."
        }), 500

    return jsonify({
        "success": True,
        "count": len(submissions),
        "submissions": submissions
    }), 200


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )