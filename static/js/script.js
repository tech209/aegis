document.addEventListener("DOMContentLoaded", function () {
    const uploadForm = document.getElementById("uploadForm");

    if (uploadForm) {
        uploadForm.addEventListener("submit", async (event) => {
            event.preventDefault();

            const phrase1 = document.getElementById("phrase1").value;
            const phrase2 = document.getElementById("phrase2").value;
            const biometric_proof = document.getElementById("biometric_proof").value;
            const credit_score = document.getElementById("credit_score").value;

            if (!phrase1 || !phrase2 || !biometric_proof || !credit_score) {
                document.getElementById("result").innerText = "❌ Please fill in all fields.";
                return;
            }

            try {
                const response = await fetch("/upload_credit_report", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ phrase1, phrase2, biometric_proof, credit_score })
                });

                const result = await response.json();

                if (result.redirect_url) {
                    window.location.href = result.redirect_url;  // ✅ Redirect to success or verify page
                } else {
                    document.getElementById("result").innerText = "✅ Submission Successful! But no redirect URL.";
                }
            } catch (error) {
                console.error("Error submitting credit snapshot:", error);
                document.getElementById("result").innerText = "❌ Submission failed.";
            }
        });
    }
});
