import smtplib

EMAIL_HOST = "smtp.office365.com"  # oder smtp-mail.outlook.com testen
EMAIL_PORT = 587
EMAIL_USERNAME = "deine_email@outlook.com"
EMAIL_PASSWORD = "DEIN_APP_PASSWORT"

try:
    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.starttls()  # TLS starten
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)  # Login testen
    print("✅ SMTP-Login erfolgreich!")
    server.quit()
except Exception as e:
    print("❌ Fehler beim SMTP-Login:", e)
