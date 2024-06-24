from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from tgbot.handlers.onboarding import static_text


# def make_keyboard_for_start_command() -> InlineKeyboardMarkup:
#     buttons = [[
#         InlineKeyboardButton(github_button_text, url="https://github.com/ohld/django-telegram-bot"),
#         InlineKeyboardButton(secret_level_button_text, callback_data=f'{SECRET_LEVEL_BUTTON}')
#     ]]

#     return InlineKeyboardMarkup(buttons)



def language_button():
    button = [[InlineKeyboardButton('Uzbek 🇺🇿', callback_data='uz'), InlineKeyboardButton('Русский 🇷🇺', callback_data='ru')]]
    return InlineKeyboardMarkup(button)

def main_menu_keyboard(language):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    static_text.KEYBOARD['request'][language]),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard