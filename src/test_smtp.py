import smtplib

EMAIL_HOST="mail.your-server.de"
EMAIL_PORT= 587  
EMAIL_USERNAME="finance.check@omni-intelligence.de"
EMAIL_PASSWORD="dubsoj-xujzym-9Tuddu"

try:
    print("🔄 Versuche Verbindung zum SMTP-Server aufzubauen...")
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT, timeout=10)
    server.set_debuglevel(1)  # SMTP-Debugging aktivieren
    server.starttls()  # TLS starten
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
    print("✅ SMTP-Login erfolgreich!")
    server.quit()
except Exception as e:
    print("❌ Fehler beim SMTP-Login:", e)
