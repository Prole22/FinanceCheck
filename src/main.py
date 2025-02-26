import sys
import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pathlib import Path
from fastapi.responses import HTMLResponse
from openai import OpenAI
from dotenv import load_dotenv

# Lade die .env Datei explizit aus dem src-Ordner
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# API-Schlüssel abrufen
openai_api_key = os.getenv("OPENAI_API_KEY")

# Logging konfigurieren
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Test-Ausgabe (nur zur Kontrolle, später entfernen!)
logger.info(f"API-Schlüssel erfolgreich geladen: {openai_api_key is not None}")

# Fügt den Pfad zu `sys.path` hinzu
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Erstelle eine FastAPI-App-Instanz
app = FastAPI()

# Statische Dateien (CSS, JS, Bilder) im frontend-Ordner bereitstellen
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

# Endpunkt für den Finanz-Check mit Logging
@app.post("/finance-check/")
def get_finance_check(data: FinanceInput):
    logger.debug(f"Empfangene Daten: {data}")  # Loggt die empfangenen Daten
    try:
        # OpenAI API Client
        client = OpenAI()

        # Anfrage an OpenAI API mit GPT-4o
        logger.debug("Sende Anfrage an OpenAI API mit GPT-4o...")
        openai_response = client.chat.completions.create(
            model="gpt-4o",  # Verwendet das leistungsstärkere GPT-4o
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher Finanzplaner."},
                {"role": "user", "content": f"Berechne eine Investitionsstrategie für {data.username}, der {data.alter} Jahre alt ist. Berufliche Situation: {data.beruf}, familiäre Situation: {data.familie}. Risikobereitschaft: {data.risiko} (Skala 1-10), monatliches Budget: {data.budget}€, Ausschlusskriterien: {data.ausschluss}. Anlagehorizont: {data.horizont}, Investitionsweise: {data.investitionsweise}."}
            ],
            max_tokens=150,
            temperature=0.7  # Optional: Erhöht Kreativität, Standard wäre 1.0
        )

        ai_response = openai_response.choices[0].message.content.strip()
        logger.debug(f"Antwort von OpenAI: {ai_response}")
    except Exception as e:
        logger.error(f"Fehler bei der OpenAI-Anfrage: {e}")
        ai_response = "Es gab ein Problem bei der Anfrage an die KI."

    return {
    "message": f"Hallo {data.username}, deine Daten wurden empfangen!",
    "email": data.email,  # Beispiel: E-Mail
    "beruf": data.beruf,  # Beispiel: Beruf
    "familie": data.familie,  # Beispiel: Familiäre Situation
    "erfahrung": data.erfahrung,  # Beispiel: Erfahrung
    "alter": data.alter,  # Beispiel: Alter
    "budget": data.budget,  # Beispiel: Budget
    "risiko": data.risiko,  # Beispiel: Risikolevel
    "ausschluss": data.ausschluss,  # Beispiel: Ausschlusskriterien
    "horizont": data.horizont,  # Beispiel: Horizont
    "investitionsweise": data.investitionsweise,  # Beispiel: Investitionsweise
    "ai_response": ai_response  # Antwort von der KI
}


