// Dark Mode Toggle
document.getElementById("dark-mode-toggle").addEventListener("click", () => {
    document.body.classList.toggle("dark-mode");
});

// Download Video Function
async function downloadVideo() {
    let url = document.getElementById('videoUrl').value.trim();
    let platform = document.getElementById('platform').value;
    let message = document.getElementById('message');

    if (!url) {
        message.innerText = "⚠️ Please enter a valid video URL.";
        return;
    }

    try {
        // Show loading state
        message.innerText = "⏳ Fetching download link...";

        let response = await fetch('/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url, platform: platform })
        });

        let data = await response.json();

        if (response.ok && data.download_link) {
            // Redirect to download link
            window.location.href = data.download_link;
        } else {
            message.innerText = "❌ Failed to fetch video. Please try again.";
        }
    } catch (error) {
        console.error("Download Error:", error);
        message.innerText = "🚨 Error downloading video. Please check your internet connection.";
    }
}

// PWA Install Prompt
let installPrompt;

window.addEventListener("beforeinstallprompt", (event) => {
    event.preventDefault();
    installPrompt = event;
    document.getElementById("installBtn").style.display = "block";
});

document.getElementById("installBtn").addEventListener("click", () => {
    if (installPrompt) {
        installPrompt.prompt();
        installPrompt.userChoice.then((choice) => {
            if (choice.outcome === "accepted") {
                console.log("User installed the app!");
            }
        });
    }
});

// Register Service Worker for PWA
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/service_worker.js')
        .then(reg => console.log("✅ Service Worker registered!", reg))
        .catch(err => console.error("❌ Service Worker registration failed:", err));
}
