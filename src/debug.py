# debug.py
import logging
from fastapi import APIRouter
from pydantic import BaseModel

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)

# Erstelle einen neuen Router für Debug-Endpunkte
debug_router = APIRouter()

# Datenmodell für User-Eingaben - genutzt für Debuging
class FinanceInput(BaseModel):
    name: str
    email: str
    investment_amount: float
    risk_level: str
    duration: int

# Debug-Endpunkt
@debug_router.post("/debug-finance-check/")
def debug_finance_check(data: FinanceInput):
    # Logge die empfangenen Daten
    logging.info(f"Empfangene Debug-Daten: {data}")
    return {
        "message": f"Debug: Hallo {data.name}, deine Daten wurden empfangen!",
        "investment": data.investment_amount,
        "risk": data.risk_level,
        "duration": data.duration
    }


