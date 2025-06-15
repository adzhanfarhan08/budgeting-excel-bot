import pandas as pd
from datetime import datetime
from config import EXCEL_FILE, EXPORT_DIR


def save_to_excel(nama: str, harga: float) -> None:
    # Saving File to Excel
    try:
        df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Tanggal", "Nama", "Harga"])

    new_row = {
        "Tanggal": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Nama": nama,
        "Harga": harga,
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)


def export_data() -> str:
    # Mengembalikan path file Excel yang sudah di-export
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_path = EXPORT_DIR / f"budget_export_{timestamp}.xlsx"

    df = pd.read_excel(EXCEL_FILE)
    df.to_excel(export_path, index=False)

    return str(export_path)
