document.getElementById('submit-btn').addEventListener('click', function() {
    const userInput = document.getElementById('user-input').value;
    if (userInput) {
        // Handle the input value (e.g., send it to the server or process it)
        console.log('User input:', userInput);
        
        // Send input to the server
        fetch('/process_text', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({ text: userInput })
        })
        .then(response => response.json())
        .then(data => {
            // Display response in the response textarea
            document.getElementById('response').value = data.text;
            console.log('Response from server:', data);

            // Handle audio playback if needed
            if (data.audio) {
                const audio = document.getElementById('audio-playback');
                audio.src = `data:audio/mp3;base64,${data.audio}`;
                document.getElementById('download-btn').disabled = false;
            }
        })
        .catch(error => console.error('Error:', error));
    } else {
        alert('Please enter some text before submitting.');
    }
});
