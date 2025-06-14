import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import pandas as pd
from datetime import datetime

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

EXCEL_FILE = 'budget_data.xlsx'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(f'Hai {user.first_name}! Kirimkan transaksi dalam format:\nNama Harga\nContoh: Buku 15000')

def save_to_excel(nama, harga):
    try:
        df = pd.read_excel(EXCEL_FILE)
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Tanggal', 'Nama', 'Harga'])
    
    new_row = {
        'Tanggal': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Nama': nama,
        'Harga': harga
    }
    
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(EXCEL_FILE, index=False)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        text = update.message.text
        parts = text.split(maxsplit=1)
        
        if len(parts) != 2:
            await update.message.reply_text('Format salah. Gunakan: Nama Harga')
            return
            
        nama = parts[0]
        try:
            harga = float(parts[1])
        except ValueError:
            await update.message.reply_text('Harga harus angka')
            return
        
        save_to_excel(nama, harga)
        await update.message.reply_text(f'✅ Tersimpan: {nama} - Rp{harga:,}')
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text('⚠️ Gagal menyimpan')

def main() -> None:
    application = Application.builder().token("8086600951:AAEMGPG_LLqxVW5rJ1p9eZJb6uOC3K03STA").build()  # Ganti dengan token bot Anda
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()
