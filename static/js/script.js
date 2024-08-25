let mediaRecorder;
let audioChunks = [];

document.getElementById('record-btn').addEventListener('click', async function() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        mediaRecorder.ondataavailable = function(event) {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = async function() {
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' }); // Use 'audio/wav' if your backend expects this format
            const formData = new FormData();
            formData.append('audio', audioBlob, 'recording.wav'); // Adjust extension based on MIME type

            try {
                const response = await fetch('/process_audio', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }

                const data = await response.json();
                document.getElementById('response').value = data.text;

                // Decode Base64 if needed
                const audioUrl = URL.createObjectURL(new Blob([new Uint8Array(atob(data.audio).split('').map(c => c.charCodeAt(0)))], { type: 'audio/mp3' }));
                const audioPlayback = document.getElementById('audio-playback');
                audioPlayback.src = audioUrl;
                audioPlayback.play();

                const downloadBtn = document.getElementById('download-btn');
                downloadBtn.href = audioUrl;
                downloadBtn.download = 'response.mp3';
                downloadBtn.disabled = false;

            } catch (error) {
                console.error('Error processing audio:', error);
            }
        };

        setTimeout(() => {
            mediaRecorder.stop();
        }, 5000); // Stop recording after 5 seconds

    } catch (error) {
        console.error('Error accessing media devices:', error);
    }
});
