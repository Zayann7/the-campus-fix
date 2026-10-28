const express = require("express");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

const FLASK_BACKEND_URL = (
    process.env.FLASK_BACKEND_URL || "http://127.0.0.1:5000"
).replace(/\/$/, "");

app.use(express.json({ limit: "1mb" }));
app.use(express.urlencoded({ extended: true }));

// Serve frontend files
app.use(express.static(path.join(__dirname, "public")));

// Forward form submissions to Flask
app.post("/api/submit", async (req, res) => {
    try {
        const flaskResponse = await fetch(
            `${FLASK_BACKEND_URL}/submit`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(req.body)
            }
        );

        const data = await flaskResponse.json().catch(() => ({
            success: false,
            message: "Invalid response from Flask backend"
        }));

        return res.status(flaskResponse.status).json(data);

    } catch (error) {
        console.error("Flask connection error:", error.message);

        return res.status(502).json({
            success: false,
            message: "Unable to connect to Flask. Check whether the backend is running."
        });
    }
});

// Check whether Express and Flask are connected
app.get("/api/health", async (req, res) => {
    try {
        const response = await fetch(`${FLASK_BACKEND_URL}/health`);
        const data = await response.json();

        res.status(response.status).json({
            frontend: "OK",
            backend: data
        });
    } catch (error) {
        res.status(502).json({
            frontend: "OK",
            backend: "Unavailable"
        });
    }
});

app.listen(PORT, "0.0.0.0", () => {
    console.log(`Frontend running at http://localhost:${PORT}`);
    console.log(`Flask backend URL: ${FLASK_BACKEND_URL}`);
});