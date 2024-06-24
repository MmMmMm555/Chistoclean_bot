from telegram import Update, ParseMode
from telegram.ext import CallbackContext, ConversationHandler
from tgbot.handlers.onboarding.keyboards import main_menu_keyboard

from tgbot.handlers.send_request import static_text
from tgbot.handlers.onboarding.static_text import main_menu
from users.models import User
from tgbot.handlers.send_request import keyboards
from tgbot import states


def send_request(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    text = static_text.TEXT['name'][u.language]
    update.message.delete()
    update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
    return states.NAME


def name(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    if update.message.text in ('Ortga 🔙', 'Назад 🔙'):
        text = main_menu[u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=main_menu_keyboard(u.language))
        return ConversationHandler.END
    else:
        name = update.message.text
        context.user_data['name'] = name
        text = static_text.TEXT['phone'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
        return states.PHONE


def phone(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    if update.message.text in ('Ortga 🔙', 'Назад 🔙'):
        update.message.delete()
        text = static_text.TEXT['name'][u.language]
        update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
        return states.NAME
    else:
        phone = update.message.text
        if len(phone) != 12:
            text = static_text.TEXT['phone_error'][u.language]
            update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
            return states.PHONE
        else:
            context.user_data['phone'] = phone
            text = static_text.TEXT['address'][u.language]
            update.message.delete()
            update.message.reply_text(text=text, reply_markup=keyboards.address_choice_button(u.language))
            return states.ADDRESS


def address(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    if update.message.text in ('Ortga 🔙', 'Назад 🔙'):
        text = static_text.TEXT['phone'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
        return states.PHONE
    else:
        address = update.message.text

        if address in ('Kvartira 🏢', 'Квартира 🏢', 'Uy/honadon 🏡', 'Дом 🏡', 'Ofis 👩‍💻', 'Офис 👩‍💻'):

            context.user_data['address'] = address

            text = static_text.TEXT['services'][u.language]

            update.message.reply_text(text=text, reply_markup=keyboards.services_button(u.language))

            return states.SERVICES
        else:
            update.message.delete()
            text = static_text.TEXT['address_error'][u.language]
            update.message.reply_text(text=text, reply_markup=keyboards.address_choice_button(u.language))
            return states.ADDRESS


def services(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    back = None
    try:
        back = update.message.text
    except:
        pass

    if back in ('Ortga 🔙', 'Назад 🔙'):
        text = static_text.TEXT['address'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.address_choice_button(u.language))
        return states.ADDRESS
    else:
        service = update.callback_query.data.split('_')[1]
        if service not in ('done', 'no'):
            if context.user_data.get('service', None) == None:
                context.user_data['service'] = [service]
            elif service in context.user_data['service']:
                context.user_data['service'].remove(service)
            else:
                context.user_data['service'].append(service)
            selected = context.user_data['service']
            text = static_text.TEXT['services'][u.language]
            update.callback_query.message.edit_text(text=text, reply_markup=keyboards.services_button(u.language, selected=selected))
            return states.SERVICES
        elif service in ['no', 'done']:
            if service == 'no':
                context.user_data['service'] = ["no"]
            if service == 'done' and len(context.user_data.get('service', '')) == 0:
                context.user_data['service'] = ["no"]
            text = static_text.TEXT['area'][u.language]
            update.callback_query.message.delete()
            update.callback_query.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
            return states.AREA


def area(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    if update.message.text in ('Ortga 🔙', 'Назад 🔙'):
        text = static_text.TEXT['services'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.services_button(u.language))
        return states.SERVICES
    else:
        area = update.message.text
        context.user_data['area'] = area
        text = static_text.TEXT['date'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
        return states.DATE


def date(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    if update.message.text in ('Ortga 🔙', 'Назад 🔙'):
        text = static_text.TEXT['area'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
        return states.AREA
    else:
        date = update.message.text
        context.user_data['date'] = date
        text = static_text.TEXT['time'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
        return states.TIME


def time(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    if update.message.text in ('Ortga 🔙', 'Назад 🔙'):
        text = static_text.TEXT['date'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
        return states.DATE
    else:
        time = update.message.text
        context.user_data['time'] = time
        text = static_text.TEXT['location'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
        return states.LOCATION


def location(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)

    if update.message.text in ('Ortga 🔙', 'Назад 🔙'):
        text = static_text.TEXT['time'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.back_button(u.language))
        return states.TIME
    else:
        location = update.message.location
        context.user_data['location'] = location
        text = static_text.TEXT['contact'][u.language]
        update.message.delete()
        update.message.reply_text(text=text, reply_markup=keyboards.no_keyboard(u.language))
        return states.COMMENT


def comment(update: Update, context: CallbackContext) -> None:
    u = User.get_user(update, context)
    comment = update.message.text

    update.message.delete()
    user_link = f"@{update.message.from_user.username}"
    services = []
    for service in context.user_data.get('service', None):
        services.append(static_text.KEYBOARD[service][u.language])
    data = data = f"Mijoz: {user_link}\nism: {context.user_data['name']}\ntel: +{context.user_data['phone']}\njoy turi: {context.user_data['address']}\nxizmatlar: {services}\nmaydon: {context.user_data['area']}\nsana: {context.user_data['date']}\nvaqt: {context.user_data['time']}\nlokatsiya: {context.user_data['location']}\ncomment: {comment}"

    update.message.bot.send_message(chat_id=1295037439, text=data)

    text = static_text.TEXT['successful'][u.language]
    update.message.reply_text(text=text, reply_markup=main_menu_keyboard(u.language))
    return ConversationHandler.END
