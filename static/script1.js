document.addEventListener('DOMContentLoaded', function() {
    const speakNameButton = document.getElementById('speakNameButton');
    const nameInput = document.getElementById('nameInput');

    const speakNumberButton = document.getElementById('speakNumberButton');
    const numberInput = document.getElementById('numberInput');

    function startSpeechRecognition(inputElement) {
        const recognition = new webkitSpeechRecognition() || new SpeechRecognition();

        recognition.onresult = function(event) {
            const result = event.results[0][0].transcript;
            inputElement.value = result;
        };

        recognition.onerror = function(event) {
            console.error('Speech recognition error:', event.error);
            recognition.stop();
        };

        recognition.onend = function() {
            console.log('Speech recognition ended.');
        };

        recognition.start();
    }

    speakNameButton.addEventListener('click', function() {
        startSpeechRecognition(nameInput);
    });

    speakNumberButton.addEventListener('click', function() {
        startSpeechRecognition(numberInput);
    });

    speakNameButton.addEventListener('mouseover', function() {
        speakButtonText(speakNameButton);
    });

    speakNumberButton.addEventListener('mouseover', function() {
        speakButtonText(speakNumberButton);
    });

    function speakButtonText(buttonElement) {
        const buttonText = buttonElement.innerText;
        const speech = new SpeechSynthesisUtterance(buttonText);
        speechSynthesis.speak(speech);
    }
});
