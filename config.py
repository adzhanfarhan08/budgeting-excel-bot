import logging
from pathlib import Path

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Excel File
EXPORT_DIR = Path("export")
EXPORT_DIR.mkdir(exist_ok=True)
EXCEL_FILE = EXPORT_DIR / "budget_data.xlsx"

# TOKEN
BOT_TOKEN = "8086600951:AAEMGPG_LLqxVW5rJ1p9eZJb6uOC3K03STA"
