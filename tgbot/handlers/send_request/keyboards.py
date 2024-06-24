from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from . import static_text


def language_button():
    button = [[InlineKeyboardButton('Uzbek', callback_data='uz'), InlineKeyboardButton('Русский', callback_data='ru')]]
    return InlineKeyboardMarkup(button)


def services_button(language, selected=[]):
    button = [
        [
            InlineKeyboardButton(f"{static_text.KEYBOARD['wash'][language]} ✅", callback_data='service_wash') if 'wash' in selected else InlineKeyboardButton(static_text.KEYBOARD['wash'][language], callback_data='service_wash'),
        ] ,
        [
            InlineKeyboardButton(f"{static_text.KEYBOARD['furniture'][language]} ✅", callback_data='service_furniture') if 'furniture' in selected else InlineKeyboardButton(static_text.KEYBOARD['furniture'][language], callback_data='service_furniture'),
        ] ,
        [
            InlineKeyboardButton(f"{static_text.KEYBOARD['window'][language]} ✅", callback_data='service_window') if 'window' in selected else InlineKeyboardButton(static_text.KEYBOARD['window'][language], callback_data='service_window'),
        ] ,
        [
            InlineKeyboardButton(f"{static_text.KEYBOARD['floor'][language]} ✅", callback_data='service_floor') if 'floor' in selected else InlineKeyboardButton(static_text.KEYBOARD['floor'][language], callback_data='service_floor'),
        ] ,
        [ 
            InlineKeyboardButton(f"{static_text.KEYBOARD['wall'][language]} ✅", callback_data='service_wall') if 'wall' in selected else InlineKeyboardButton(static_text.KEYBOARD['wall'][language], callback_data='service_wall'),
        ] ,
        [
            InlineKeyboardButton(f"{static_text.KEYBOARD['marmar'][language]} ✅", callback_data='service_marmar') if 'marmar' in selected else InlineKeyboardButton(static_text.KEYBOARD['marmar'][language], callback_data='service_marmar'),
        ],
        [
            InlineKeyboardButton(static_text.KEYBOARD['done'][language], callback_data='service_done'),
        ],
        [
            InlineKeyboardButton(static_text.KEYBOARD['no'][language], callback_data='service_no'),
        ],
    ]
    return InlineKeyboardMarkup(button)


def back_button(language):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    static_text.KEYBOARD['back'][language]),
            ],
            [
                KeyboardButton(
                    static_text.KEYBOARD['main_menu'][language]),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard


def no_keyboard(language):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    static_text.KEYBOARD['not'][language]),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard

def address_choice_button(language):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    static_text.KEYBOARD['rent'][language]),
                KeyboardButton(
                    static_text.KEYBOARD['house'][language]),
                KeyboardButton(
                    static_text.KEYBOARD['office'][language]),
            ],
            [
                KeyboardButton(
                    static_text.KEYBOARD['back'][language]),
                KeyboardButton(
                    static_text.KEYBOARD['main_menu'][language]),
            ],
        ],
        resize_keyboard=True,
    )
    return keyboard