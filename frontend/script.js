document.getElementById('finance-form').addEventListener('submit', function(event) {
    event.preventDefault();

    // Formulardaten sammeln
    const formData = new FormData(this);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        investment_amount: parseFloat(formData.get('investment_amount')),
        risk_level: formData.get('risk_level'),
        duration: parseInt(formData.get('duration'))
    };

    // Anfrage an den Backend-Endpunkt senden
    fetch('/finance-check/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)  // Formulardaten als JSON senden
    })
    .then(response => response.json())  // Die Antwort vom Server im JSON-Format lesen
    .then(data => {
        // Ausgabe der Antwort auf der Webseite im 'ai-response' Bereich
        document.getElementById('ai-response').innerText = data.ai_response || 'Keine Antwort von der KI erhalten.';
    })
    .catch(error => {
        console.error('Error:', error);
        // Fehlerausgabe in der Konsole, wenn etwas schief geht
        document.getElementById('ai-response').innerText = 'Ein Fehler ist aufgetreten.';
    });
});

