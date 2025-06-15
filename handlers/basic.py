import re, os

from telegram import Update, InputFile
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from utils.excel import save_to_excel, export_data
from config import logger


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Handler untuk command /help
    help_text = """
        🛠 *Panduan Penggunaan Bot Budgeting* 🛠
        
        /start - Start Bot
        /help - Show guide

        📝 *Format Input*:
        `<nama> <harga>`
        Contoh: `Buku 10000`
        """

    await update.message.reply_text(help_text, parse_mode="Markdown")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text.strip()

    # Pisahkan nama dan harga menggunakan regex
    match = re.match(r"^(.+?)\s+([\d,.+]+)$", text)

    if not match:
        await update.message.reply_text(
            "⚠ Format salah. Gunakan:\n"
            "<nama_item> <harga>\n"
            "Contoh: `Mie Sedap Ayam 15,000` atau `Kopi Susu 10.500`",
            parse_mode="Markdown",
        )
        return

    nama = match.group(1).strip()  # Ambil bagian nama (boleh ada spasi/koma/+)
    harga_str = match.group(2)  # Ambil bagian harga

    # Normalisasi harga (hilangkan tanda baca selain digit)
    try:
        harga = float(re.sub(r"[^\d]", "", harga_str))
    except ValueError:
        await update.message.reply_text("❌ Harga harus angka!")
        return

    # Simpan ke Excel (gunakan fungsi yang sudah ada)
    save_to_excel(nama, harga)
    await update.message.reply_text(f"✅ Disimpan: {nama} - Rp{harga:,}")


async def export_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        export_path = export_data()

        with open(export_path, "rb") as file:
            await update.message.reply_document(
                document=InputFile(file, filename=os.path.basename(export_path)),
                caption="📊 Export data budget",
            )
    except Exception as e:
        logger.error(f"Export error: {e}")
        await update.message.reply_text("❌ Gagal mengekspor data")


# Export handlers
handlers = [
    CommandHandler("help", help),
    CommandHandler("export", export_command),
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
]
