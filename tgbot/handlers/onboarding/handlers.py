import datetime

from django.utils import timezone
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, ConversationHandler

from tgbot.handlers.onboarding import static_text
from tgbot.handlers.utils.info import extract_user_data_from_update
from users.models import User
from tgbot.handlers.onboarding.keyboards import language_button, main_menu_keyboard
from tgbot.states import SELECT_LANGUAGE


def command_start(update: Update, context: CallbackContext) -> None:
    u, created = User.get_user_and_created(update, context)

    text =  """Добро пожаловать в ChistoClean!
Мы предлагаем профессиональные клининговые
услуги для вашего дома и офиса.
Чистота и порядок - наша профессия!
Сделаем всё в лучшем виде!
___________________________
ChistoClean-ga xush kelibsiz!
Uyingiz va ofisingiz uchun professional klining
xizmatlarini taklif etamiz.
Tozalik va tartib bizning kasbimiz!
Biz hamma narsani eng yaxshi tarzda qilamiz!"""
    if update.message.from_user.id == 1295037439:
        text = "Salom boss!"
    update.message.reply_text(text=text)
    update.message.reply_text(text="Tilni tanlang/Выберете язык 🌐", reply_markup=language_button())
    return SELECT_LANGUAGE


def select_language(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    if update.callback_query.data == 'uz':
        u.language = 'uz'
    elif update.callback_query.data == 'ru':
        u.language = 'ru'
    u.save()
    text = static_text.main_menu[u.language]
    update.callback_query.message.reply_text(text=text, reply_markup=main_menu_keyboard(u.language))
    return ConversationHandler.END



def redirect_to_main_menu(update: Update, context: CallbackContext) -> None:
    """ Redirect to main menu """
    u = User.get_user(update, context)
    text = static_text.main_menu[u.language]
    update.message.reply_text(text=text, reply_markup=main_menu_keyboard(u.language))
    return ConversationHandler.END



def secret_level(update: Update, context: CallbackContext) -> None:
    # callback_data: SECRET_LEVEL_BUTTON variable from manage_data.py
    """ Pressed 'secret_level_button_text' after /start command"""
    user_id = extract_user_data_from_update(update)['user_id']
    text = static_text.unlock_secret_room.format(
        user_count=User.objects.count(),
        active_24=User.objects.filter(updated_at__gte=timezone.now() - datetime.timedelta(hours=24)).count()
    )

    context.bot.edit_message_text(
        text=text,
        chat_id=user_id,
        message_id=update.callback_query.message.message_id,
        parse_mode=ParseMode.HTML
    )