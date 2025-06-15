from telegram.ext import Application
from config import BOT_TOKEN
from handlers.basic import handlers


def main() -> None:
    # Running Bot
    application = Application.builder().token(BOT_TOKEN).build()

    for handler in handlers:
        application.add_handler(handler)

    application.run_polling()


if __name__ == "__main__":
    main()
