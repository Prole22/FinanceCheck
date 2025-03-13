// Wenn das DOM vollständig geladen ist
document.addEventListener('DOMContentLoaded', function() {
    // Button holen, der das Formular anzeigt
    const startButton = document.querySelector('.btn-start');

    // Event Listener hinzufügen, der das Formular anzeigt
    if (startButton) {
        startButton.addEventListener('click', function() {
            showForm();  // ruft die Funktion auf, die das Formular anzeigt
        });
    }
});

// Funktion, um das Formular anzuzeigen
function showForm() {
    // Formular sichtbar machen
    document.getElementById('form-section').style.display = 'block';
    // Startbutton ausblenden
    document.querySelector('.btn-start').style.display = 'none';

    // Die Sektionen ausblenden
    document.getElementById('why-finance-check').style.display = 'none';
    document.getElementById('roadmap-section').style.display = 'none';

    // Optional: Nach oben scrollen, damit die Felder direkt sichtbar sind
    document.getElementById('form-section').scrollIntoView({ behavior: 'smooth' });
}

document.getElementById('finance-form').addEventListener('submit', function(event) {
    event.preventDefault();


    // Formulardaten sammeln
    const formData = new FormData(this);
    const data = {
        username: formData.get('username'),
        email: formData.get('email'),
        beruf: formData.get('beruf'),
        familie: formData.get('familie'),
        erfahrung: formData.get('erfahrung'),
        alter: parseInt(formData.get('alter')),
        budget: parseFloat(formData.get('budget')),
        risiko: parseInt(formData.get('risiko')),
        ausschluss: formData.get('ausschluss'),
        horizont: formData.get('horizont'),
        investitionsweise: formData.get('investitionsweise')
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
        // Formularbereich ausblenden, wenn das Ergebnis angezeigt wird
        document.getElementById('form-section').style.display = 'none';
        // KI-Antwortbereich anzeigen
        document.getElementById('result-section').style.display = 'block';
    })
    .catch(error => {

        console.error('Error:', error);
        // Fehlerausgabe in der Konsole, wenn etwas schief geht
        document.getElementById('ai-response').innerText = 'Ein Fehler ist aufgetreten.';
    });
});


document.addEventListener('DOMContentLoaded', function () {
    const sendEmailBtn = document.getElementById('send-email-btn');

    if (sendEmailBtn) {
        sendEmailBtn.addEventListener('click', function () {
            sendEmail();
        });
    }
});

function sendEmail() {
    // Finanzstrategie abrufen
    const financeCheckResult = document.getElementById('ai-response').innerText;

    // Formulardaten aus den Eingabefeldern holen
    const formData = new FormData(document.getElementById('finance-form'));
    const data = {
        username: formData.get('username'),
        email: formData.get('email'),
        beruf: formData.get('beruf'),
        familie: formData.get('familie'),
        erfahrung: formData.get('erfahrung'),
        alter: parseInt(formData.get('alter')),
        budget: parseFloat(formData.get('budget')),
        risiko: parseInt(formData.get('risiko')),
        ausschluss: formData.get('ausschluss'),
        horizont: formData.get('horizont'),
        investitionsweise: formData.get('investitionsweise'),
        ai_response: financeCheckResult // KI-Antwort hinzufügen
    };

    if (!data.email) {
        alert("Bitte geben Sie eine gültige E-Mail-Adresse ein.");
        return;
    }

    fetch('/send-email/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    })
    .catch(error => {
        console.error('Fehler beim Senden der E-Mail:', error);
        alert('E-Mail konnte nicht gesendet werden.');
    });
}

