import logging, os
from pathlib import Path
from dotenv import load_dotenv

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Excel File
EXPORT_DIR = Path("export")
EXPORT_DIR.mkdir(exist_ok=True)
EXCEL_FILE = EXPORT_DIR / "budget_data.xlsx"

if not BOT_TOKEN:
    raise ValueError("Token bot tidak ditemukan! Pastikan file .env sudah dibuat")
