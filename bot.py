import logging

from telegram.ext import ApplicationBuilder, CommandHandler, ConversationHandler, MessageHandler, filters

import database.db_manager as db_manager
from handlers import start, roll_dice_command, handle_error, CHOOSING, TYPING_BET, cancel
from settings import BOT_TOKEN

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def main():
    with db_manager.get_conn() as conn:
        db_manager.create_tables(conn)
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_error_handler(handle_error)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [CommandHandler('start', start), roll_dice_command],
            TYPING_BET: [MessageHandler(filters.TEXT & ~filters.COMMAND, roll_dice_command)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == '__main__':
    main()
