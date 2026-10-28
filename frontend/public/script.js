const form = document.getElementById("issueForm");
const submitButton = document.getElementById("submitButton");
const statusMessage = document.getElementById("statusMessage");

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    statusMessage.className = "status";
    statusMessage.textContent = "";

    submitButton.disabled = true;
    submitButton.textContent = "Submitting...";

    try {
        const formData = Object.fromEntries(
            new FormData(form).entries()
        );

        const response = await fetch("/api/submit", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        if (!response.ok || !result.success) {
            throw new Error(result.message || "Submission failed.");
        }

        statusMessage.textContent =
            `${result.message} Reference ID: ${result.submission.id}`;

        statusMessage.className = "status success";

        form.reset();

    } catch (error) {
        statusMessage.textContent = error.message;
        statusMessage.className = "status error";

    } finally {
        submitButton.disabled = false;
        submitButton.textContent = "Submit Request";
    }
});