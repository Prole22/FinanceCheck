import sys
import os
import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
from fastapi.responses import HTMLResponse
from openai import OpenAI
from dotenv import load_dotenv

# Lade die .env Datei explizit aus dem src-Ordner (wegen Problemen mit dem korrekten Pfad)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))


# API-Schlüssel abrufen
openai_api_key = os.getenv("OPENAI_API_KEY")

# E-Mail Konfiguration aus .env (Sicherheitsrelevante Daten übernehmen)
EMAIL_HOST = os.getenv("EMAIL_HOST")  # z. B. smtp.gmail.com
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))  # Standardmäßig 587 für TLS
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Logging konfigurieren
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Test-Ausgabe (zur besseren Übersicht in der Konsole)
logger.info(f"API-Schlüssel erfolgreich geladen: {openai_api_key is not None}")
logger.info(f"E-Mail-Server konfiguriert: {EMAIL_HOST is not None}")

# Erstelle eine FastAPI-App-Instanz
app = FastAPI()

# Statische Dateien im frontend-Ordner bereitstellen
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# HTML-Template mit Jinja2
templates = Jinja2Templates(directory="frontend")

# Root-Endpunkt, um die HTML-Seite zu rendern
@app.get("/", response_class=HTMLResponse)
async def get_homepage():
    logger.debug("Aufruf der Startseite")
    return templates.TemplateResponse("index.html", {"request": {}})

# Datenmodell für User-Eingaben
class FinanceInput(BaseModel):
    username: str
    email: str
    beruf: str
    familie: str
    erfahrung: str
    alter: int
    budget: float
    risiko: int
    ausschluss: str
    horizont: str
    investitionsweise: str
    startkapital: float
    ai_response: str = None  # !Optional, wird beim E-Mail-Versand benötigt

# Endpunkt für den Finanz-Check mit Logging
@app.post("/finance-check/")
def get_finance_check(data: FinanceInput):
    logger.debug(f"Empfangene Daten: {data}")  # Loggt die empfangenen Daten
    try:
        # OpenAI API Client
        client = OpenAI()

        # Anfrage an OpenAI API mit o3-mini
        logger.debug("Sende Anfrage an OpenAI API mit GPT-4o...")
        openai_response = client.chat.completions.create(
            model="o3-mini",  
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher Finanzplaner."},
                {"role": "user", "content": f"""
                Erstelle bitte einen detaillierten Finance Check für einen Nutzer anhand folgender Angaben und der aktuell verfügbaren Marktdaten. 
                Der Bericht soll in einem strukturierten Format erfolgen und für jeden der folgenden fünf Bereiche – 
                1. Bankprodukte, 2. ETFs, 3. Anleihen, 4. Aktien, 5. Kryptowährungen – folgende Punkte beinhalten:
                
                • **Risikobewertung:** Wie hoch ist das Risiko in diesem Bereich?
                • **Pro und Contra:** Welche Vorteile und Nachteile bietet diese Investitionsmethode?
                • **Mögliche Rendite:** Welche Rendite könnte der Nutzer aktuell erwarten?
                
                Zusätzlich soll für jede Anlageform eine persönliche Eignungsbewertung anhand der folgenden vier Kriterien erfolgen 
                (jeweils auf einer Skala von 1 bis 5, wobei 5 den bestmöglichen Wert darstellt):
                
                1. **Investitionssicherheit:** Bewertung, wie robust und stabil das Investment ist (unter Berücksichtigung von Ausfallrisiko, Marktschwankungen und Kapitalerhalt).
                2. **Zeithorizont:** Bewertung, wie gut der empfohlene Anlagehorizont zur gewünschten Investitionsdauer des Nutzers passt.
                3. **Renditeerwartung:** Bewertung der zu erwartenden Rendite im Verhältnis zu den Erwartungen des Nutzers.
                4. **Komplexität:** Bewertung, wie einfach oder komplex die Anlageform ist, insbesondere in Bezug auf die Investitionserfahrung des Nutzers.
                
                Abschließend soll ein **Personal-Match-Score (PMS)** benannt werden (1-5), der angibt, wie gut die jeweilige Anlageform zur aktuellen Situation und den Präferenzen des Nutzers passt.

                Gib für jeden **Personal-Match-Score (PMS)** auch Begründungen an, warum ein bestimmtes Asset nicht zur persönlichen Situation des Users passt, 
                oder warum es zur persönlichen Situation des Users passt. 

                (Beispiel: Der Nutzer möchte kurzfristig investieren, während Festgeld eine langfristige Investitionsmethode ist →  
                "Beim Festgeld wird ein bestimmter Zeitrahmen festgelegt, der meist mehrere Jahre beträgt. Da du eher kurzfristig investieren möchtest, ist diese Methode nicht perfekt für dich geeignet.")

                **Marktdaten berücksichtigen:** 
                Bitte berücksichtige auch, dass du im Web die aktuellen Informationen suchst (z. B. Tagesgeldzinsen, Festgeldzinssätze, aktuelle Trends am Aktienmarkt, ETF-Renditen etc.).

                **Nutzerangaben für die Analyse:**
                - **Persönliche Situation:**
                  - Berufliche Situation: {data.beruf}
                  - Familiäre Situation: {data.familie}
                  - Investitionserfahrung: {data.erfahrung}
                  - Alter: {data.alter}
                  - Monatliches Investitionsbudget: {data.budget}€
                  - Risikobereitschaft: {data.risiko} (1 = sehr risikoavers, 10 = sehr risikofreudig)

                - **Investment-Präferenzen:**
                  - Ausschlusskriterien: {data.ausschluss}
                  - Anlagehorizont: {data.horizont}
                  - Investitionsweise: {data.investitionsweise}
                  - Startkapital: {data.startkapital}€

                Nutze diese Informationen, um den aktuellen Markt zu analysieren und dem Nutzer einen umfassenden Finance Check zu erstellen, 
                der alle oben genannten Punkte für jeden der fünf Bereiche abdeckt sowie eine abschließende Personal-Match-Score-Bewertung (PMS).
                """}
            ],
            max_completion_tokens=4000,
        )

        ai_response = openai_response.choices[0].message.content.strip()
        logger.debug(f"Antwort von OpenAI: {ai_response}")
    except Exception as e:
        logger.error(f"Fehler bei der OpenAI-Anfrage: {e}")
        ai_response = "Es gab ein Problem bei der Anfrage an die KI."

    return {
        "message": f"Hallo {data.username}, deine Daten wurden empfangen!",
        "email": data.email,
        "beruf": data.beruf,
        "familie": data.familie,
        "erfahrung": data.erfahrung,
        "alter": data.alter,
        "budget": data.budget,
        "startkapital":data.startkapital,
        "risiko": data.risiko,
        "ausschluss": data.ausschluss,
        "horizont": data.horizont,
        "investitionsweise": data.investitionsweise,
        "ai_response": ai_response
    }


@app.post("/send-email/")
def send_email(data: FinanceInput):
    try:
        # ließt das E-Mail-Template aus der Datei
        template_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'email_template.html')
        with open(template_path, "r", encoding="utf-8") as f:
            email_template = f.read()
        
        # Sende einen zweiten Prompt an o3-mini, der das Template mit den Finanzdaten füllt
        client = OpenAI()
        logger.debug("Sende zweiten Prompt an GPT-4o für HTML-Template-Füllung...")
        
        openai_response = client.chat.completions.create(
            model="o3-mini",
            messages=[
                {"role": "system", "content": "Du bist ein Finanzexperte, der ein HTML-Email-Template anhand übergebener Finanzdaten ausfüllt. Ändere dabei nur die Platzhalter im HTML, ohne den Rest des Codes zu verändern."},
                {"role": "user", "content": f"""
Fülle die folgende HTML-E-Mail-Vorlage aus, indem du die Informationen aus der folgenden Finance Analyse einsetzt. Ersetze alle Platzhalter (z.B. {{Name}}, {{Budget}}, etc.) mit den entsprechenden Werten. 
                 Achte darauf die Platzhalter unterhalb des PMS auszufüllen ([Platzhalter Grund 1]).

**Finance Analyse:**
Name: {data.username}
Alter: {data.alter}
Beruf: {data.beruf}
Familiensituation: {data.familie}
Investitionserfahrung: {data.erfahrung}
Budget: {data.budget}€
startkapital:{data.startkapital}
Risikobereitschaft: {data.risiko} (auf einer Skala von 1 bis 10)
Ausschlusskriterien: {data.ausschluss}
Anlagehorizont: {data.horizont}
Investitionsweise: {data.investitionsweise}

KI-generierte Finanzstrategie:
{data.ai_response}

**HTML-Vorlage:**
{email_template}
                """}
            ],
            max_completion_tokens=15000,
            
        )

        # Extrahiere den generierten HTML-Code
        html_body = openai_response.choices[0].message.content.strip()

        # Entferne Markdown-Formatierung (```html ... ```) falls vorhanden - zur Fehlerbehandlung
        if html_body.startswith("```html") and html_body.endswith("```"):
            html_body = html_body[7:-3].strip()

       # Debug: HTML-Output in den Logs anzeigen
        logger.debug(f"Generierter HTML-Code:\n{html_body}")

        # Erstelle und versende die HTML-E-Mail
        subject = "Ihr persönlicher Finanzplan"

        msg = MIMEMultipart()
        msg['From'] = EMAIL_USERNAME
        msg['To'] = data.email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, 'html'))  # HTML-Inhalt anhängen

        # Verbindung zum SMTP-Server herstellen und Mail versenden
        server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
        server.starttls()
        server.login(EMAIL_USERNAME, EMAIL_PASSWORD)
        server.sendmail(EMAIL_USERNAME, data.email, msg.as_string())
        server.quit()

        logger.info(f"E-Mail erfolgreich an {data.email} gesendet.")
        return {"message": "E-Mail erfolgreich gesendet."}

    except Exception as e:
        logger.error(f"Fehler beim Senden der E-Mail: {e}")
        return {"error": "Fehler beim Senden der E-Mail."}
