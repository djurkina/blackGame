import logging

from telebot.types import ReplyKeyboardRemove
from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler, ApplicationErrorCallback, ConversationHandler
from games.dice import roll_dice
from database import db_manager
import settings

CHOOSING, TYPING_BET = range(2)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    with db_manager.get_conn() as conn:
        db_manager.add_user(conn, user_id)
    balance = get_user_balance(update, context)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Welcome to the game! Your balance: {balance}")
    return CHOOSING

async def roll_dice_command(update: Update, context: CallbackContext):
    try:
        bet = int(update.message.text)
        if bet <= 0:
            raise ValueError("The rate must be positive.")

        with db_manager.get_conn() as conn:
            balance = db_manager.get_user_balance(conn, update.effective_user.id)
            if bet > balance:
                raise ValueError("Insufficient funds.")

        results, total = roll_dice()
        winnings = bet * 2 if total > 7 else -bet

        with db_manager.get_conn() as conn:
            db_manager.update_user_balance(conn, update.effective_user.id, winnings)
            balance = db_manager.get_user_balance(conn, update.effective_user.id)

        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Dropped out: {results[0]} и {results[1]}, sum: {total}\n{'You won!' if winnings > 0 else 'You lost!'}\n Your balance: {balance}")
        return CHOOSING

    except (ValueError, TypeError) as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {e}. Enter another amount.")
        return TYPING_BET
    except Exception as e:
        await handle_error(update, context, e)
        return ConversationHandler.END

async def handle_error(update: object, context: CallbackContext, error: Exception):
    logger = logging.getLogger(__name__)
    logger.error(f"Error: {error}, Update: {update}")
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Error: {error}")

def get_user_balance(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    with db_manager.get_conn() as conn:
        return db_manager.get_user_balance(conn, user_id)

async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Cancellation.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END
