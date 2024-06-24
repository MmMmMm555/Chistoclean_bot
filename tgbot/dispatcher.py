"""
    Telegram event handlers
"""
from telegram.ext import (
    Dispatcher, Filters,
    CommandHandler, MessageHandler,
    CallbackQueryHandler,
    ConversationHandler,
)

from dtb.settings import DEBUG
from tgbot.handlers.broadcast_message.manage_data import CONFIRM_DECLINE_BROADCAST
from tgbot.handlers.broadcast_message.static_text import broadcast_command
from tgbot.handlers.onboarding.manage_data import SECRET_LEVEL_BUTTON

from tgbot.handlers.utils import files, error
from tgbot.handlers.admin import handlers as admin_handlers
from tgbot.handlers.location import handlers as location_handlers
from tgbot.handlers.onboarding import handlers as onboarding_handlers
from tgbot.handlers.broadcast_message import handlers as broadcast_handlers
from tgbot.handlers.send_request import handlers as send_request_handlers
from tgbot.main import bot
from tgbot import states

def setup_dispatcher(dp):
    """
    Adding handlers for events from Telegram
    """
    conv = ConversationHandler(
        entry_points=[
            CommandHandler("start", onboarding_handlers.command_start),
            MessageHandler(
                Filters.regex("(^Ariza yuborish 📤$|^Отправить запрос 📤$)"),
                send_request_handlers.send_request),
        ],
        states={
            states.SELECT_LANGUAGE: [
                CallbackQueryHandler(onboarding_handlers.select_language, pattern="^(uz|ru)$"),
            ],

            states.NAME: [
                MessageHandler(
                Filters.regex("(^Asosiy sahifa 🏠$|^Главное меню 🏠$)"),
                onboarding_handlers.redirect_to_main_menu),

                MessageHandler(Filters.text,
                send_request_handlers.name),
            ],

            states.PHONE: [
                MessageHandler(
                Filters.regex("(^Asosiy sahifa 🏠$|^Главное меню 🏠$)"),
                onboarding_handlers.redirect_to_main_menu),

                MessageHandler(Filters.regex('(^998)|^Ortga 🔙$|^Назад 🔙'),
                send_request_handlers.phone),
            ],

            states.ADDRESS: [
                MessageHandler(
                Filters.regex("(^Asosiy sahifa 🏠$|^Главное меню 🏠$)"),
                onboarding_handlers.redirect_to_main_menu),

                MessageHandler(Filters.text,
                send_request_handlers.address),
            ],

            states.SERVICES: [
                MessageHandler(
                Filters.regex("(^Asosiy sahifa 🏠$|^Главное меню 🏠$)"),
                onboarding_handlers.redirect_to_main_menu),

                MessageHandler(Filters.regex('^Ortga 🔙$|^Назад 🔙'),
                send_request_handlers.services),

                CallbackQueryHandler(
                    send_request_handlers.services, pattern="^service"),
            ],

            states.AREA: [
                MessageHandler(
                Filters.regex("(^Asosiy sahifa 🏠$|^Главное меню 🏠$)"),
                onboarding_handlers.redirect_to_main_menu),

                MessageHandler(Filters.text,
                send_request_handlers.area),
            ],

            states.DATE: [
                MessageHandler(
                Filters.regex("(^Asosiy sahifa 🏠$|^Главное меню 🏠$)"),
                onboarding_handlers.redirect_to_main_menu),

                MessageHandler(Filters.text,
                send_request_handlers.date),
            ],

            states.TIME: [
                MessageHandler(
                Filters.regex("(^Asosiy sahifa 🏠$|^Главное меню 🏠$)"),
                onboarding_handlers.redirect_to_main_menu),

                MessageHandler(Filters.text,
                send_request_handlers.time),
            ],

            states.LOCATION: [
                MessageHandler(
                Filters.regex("(^Asosiy sahifa 🏠$|^Главное меню 🏠$)"),
                onboarding_handlers.redirect_to_main_menu),

                MessageHandler(Filters.location,
                send_request_handlers.location),
            ],

            states.COMMENT: [
                MessageHandler(Filters.text,
                send_request_handlers.comment),
            ],
        },
        fallbacks=[],
    )

    dp.add_handler(conv)

    # onboarding
    # dp.add_handler(CommandHandler("start", onboarding_handlers.command_start))

    # admin commands
    dp.add_handler(CommandHandler("admin", admin_handlers.admin))
    dp.add_handler(CommandHandler("stats", admin_handlers.stats))
    dp.add_handler(CommandHandler('export_users', admin_handlers.export_users))

    # location
    dp.add_handler(CommandHandler("ask_location", location_handlers.ask_for_location))
    dp.add_handler(MessageHandler(Filters.location, location_handlers.location_handler))

    # secret level
    dp.add_handler(CallbackQueryHandler(onboarding_handlers.secret_level, pattern=f"^{SECRET_LEVEL_BUTTON}"))

    # broadcast message
    dp.add_handler(
        MessageHandler(Filters.regex(rf'^{broadcast_command}(/s)?.*'), broadcast_handlers.broadcast_command_with_message)
    )
    dp.add_handler(
        CallbackQueryHandler(broadcast_handlers.broadcast_decision_handler, pattern=f"^{CONFIRM_DECLINE_BROADCAST}")
    )

    # files
    dp.add_handler(MessageHandler(
        Filters.animation, files.show_file_id,
    ))

    # handling errors
    dp.add_error_handler(error.send_stacktrace_to_tg_chat)

    # EXAMPLES FOR HANDLERS
    # dp.add_handler(MessageHandler(Filters.text, <function_handler>))
    # dp.add_handler(MessageHandler(
    #     Filters.document, <function_handler>,
    # ))
    # dp.add_handler(CallbackQueryHandler(<function_handler>, pattern="^r\d+_\d+"))
    # dp.add_handler(MessageHandler(
    #     Filters.chat(chat_id=int(TELEGRAM_FILESTORAGE_ID)),
    #     # & Filters.forwarded & (Filters.photo | Filters.video | Filters.animation),
    #     <function_handler>,
    # ))

    return dp


n_workers = 0 if DEBUG else 4
dispatcher = setup_dispatcher(Dispatcher(bot, update_queue=None, workers=n_workers, use_context=True))
