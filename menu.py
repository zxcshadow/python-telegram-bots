import logging

import telegram
from telegram import Update, ForceReply, ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaDocument, \
    InputMediaPhoto, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackContext, Defaults, CallbackQueryHandler
from typing import Union, List
from telegram import InlineKeyboardButton

# Enable logging

TOKEN = "5133967103:AAFLaXf1GIPO2HzZKEy_Qg1HWd_ASQdhqkQ"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)


def build_menu(
    buttons: List[InlineKeyboardButton],
    n_cols: int,
    header_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None,
    footer_buttons: Union[InlineKeyboardButton, List[InlineKeyboardButton]]=None
) -> List[List[InlineKeyboardButton]]:
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons if isinstance(header_buttons, list) else [header_buttons])
    if footer_buttons:
        menu.append(footer_buttons if isinstance(footer_buttons, list) else [footer_buttons])
    return menu


def inline_keyboard(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [
        [
            InlineKeyboardButton('Menu', callback_data='0'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(custom_keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Count: ", reply_markup=reply_markup)


def btn_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    count = int(query.data) + 1
    custom_keyboard = [
        InlineKeyboardButton('MenuItem1', callback_data=count),
        InlineKeyboardButton('MenuItem2', callback_data=count),
        InlineKeyboardButton('MenuItem3', callback_data=count),
        InlineKeyboardButton('MenuItem4', callback_data=count),
    ]
    header_keyboard = [
        InlineKeyboardButton('List1', callback_data=count),
        InlineKeyboardButton('List2', callback_data=count),
    ]

    reply_markup = InlineKeyboardMarkup(build_menu(buttons=custom_keyboard, n_cols=2, header_buttons=header_keyboard))
    query.edit_message_text(text=f"Count: {count}", reply_markup=reply_markup)


def main() -> None:
    """Start the bot."""

    defaults = Defaults(parse_mode=ParseMode.HTML)

    updater = Updater(TOKEN, defaults=defaults)

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("ibuttons", inline_keyboard))
    dispatcher.add_handler(CallbackQueryHandler(btn_handler))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()