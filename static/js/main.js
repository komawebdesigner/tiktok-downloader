async function downloadVideo() {
    let url = document.getElementById('videoUrl').value;

    if (!url) {
        document.getElementById('message').innerText = "Please enter a TikTok video URL.";
        return;
    }

    try {
        let response = await fetch('/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url: url })
        });

        let data = await response.json();
        
        if (data.download_link) {
            window.location.href = data.download_link;
        } else {
            document.getElementById('message').innerText = "Failed to fetch video.";
        }
    } catch (error) {
        document.getElementById('message').innerText = "Error downloading video.";
    }
}
