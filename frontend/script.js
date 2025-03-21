// Wenn das DOM vollständig geladen ist - warten bis alles geladen hat bevor es zur Ausführung kommt
document.addEventListener('DOMContentLoaded', function () {
    hideLoadingScreen(); // Ladebildschirm direkt verstecken

    const startButton = document.querySelector('.btn-start');
    if (startButton) {
        startButton.addEventListener('click', function () {
            showForm();
        });
    }

    const financeForm = document.getElementById('finance-form');
    if (financeForm) {
        financeForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            showLoadingScreen(); // Ladebildschirm aktivieren
            console.log("🟢 Formular abgeschickt, Ladebildschirm sollte jetzt erscheinen.");

            const formData = new FormData(financeForm);
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
                startkapital: parseFloat(formData.get('startkapital'))
            };

            try {
                const response = await fetch('/finance-check/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                
                // Künstliche Verzögerung einfügen (z.B. 1500 ms) - damit der Ladebildschirm auch sicher kurz angezeigt wird
                await delay(1500);

                if (!response.ok) {
                    throw new Error("Serverantwort war nicht erfolgreich.");
                }

                const result = await response.json();
                document.getElementById('ai-response').innerText = result.ai_response || 'Keine Antwort von der KI erhalten.';
                document.getElementById('form-section').style.display = 'none';
                document.getElementById('result-section').style.display = 'block';
            } catch (error) {
                console.error('Fehler:', error);
                document.getElementById('ai-response').innerText = 'Ein Fehler ist aufgetreten.';
            }

            console.log("🔴 Ladebildschirm wird deaktiviert!");
            hideLoadingScreen(); // Ladebildschirm deaktivieren
        });
    }

    const sendEmailBtn = document.getElementById('send-email-btn');
    if (sendEmailBtn) {
        sendEmailBtn.addEventListener('click', async function () {
            showLoadingScreen(); // Ladebildschirm aktivieren
            console.log("🟢 E-Mail-Versand gestartet, Ladebildschirm sollte jetzt erscheinen.");

            try {
                await sendEmail();
            } catch (error) {
                console.error('Fehler beim Senden der E-Mail:', error);
            }

            console.log("🔴 Ladebildschirm wird deaktiviert!");
            hideLoadingScreen(); // Ladebildschirm deaktivieren
        });
    }
});

// Funktion, um das Formular anzuzeigen
function showForm() {
    document.getElementById('form-section').style.display = 'block';
    document.querySelector('.btn-start').style.display = 'none';
    document.getElementById('why-finance-check').style.display = 'none';
    document.getElementById('roadmap-section').style.display = 'none';
    document.getElementById('form-section').scrollIntoView({ behavior: 'smooth' });
}

// Funktion zum Versenden der E-Mail
async function sendEmail() {
    const financeCheckResult = document.getElementById('ai-response').innerText;
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
        startkapital: parseFloat(formData.get('startkapital')),
        ai_response: financeCheckResult
    };

    if (!data.email) {
        alert("Bitte geben Sie eine gültige E-Mail-Adresse ein.");
        hideLoadingScreen(); // Ladebildschirm deaktivieren, falls keine E-Mail eingegeben wurde
        return;
    }

    try {
        const response = await fetch('/send-email/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error("E-Mail konnte nicht gesendet werden.");
        }

        const result = await response.json();
        alert(result.message);
    } catch (error) {
        console.error('Fehler beim Senden der E-Mail:', error);
        alert('E-Mail konnte nicht gesendet werden.');
    }
}

// Künstliche Verzögerungsfunktion
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// Funktion zum Anzeigen des Ladebildschirms
function showLoadingScreen() {
    console.log("🟢 Ladebildschirm wird aktiviert!");
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
        loadingOverlay.style.setProperty('display', 'flex', 'important');
    }
}

// Funktion zum Verstecken des Ladebildschirms
function hideLoadingScreen() {
    console.log("🔴 Ladebildschirm wird deaktiviert!");
    const loadingOverlay = document.getElementById('loading-overlay');
    if (loadingOverlay) {
        loadingOverlay.style.display = 'none';
        loadingOverlay.style.setProperty('display', 'none', 'important');
    }
}
