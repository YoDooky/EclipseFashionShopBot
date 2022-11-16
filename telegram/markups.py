from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def get_user_menu():
    user_menu = InlineKeyboardMarkup(row_width=3)
    order_button = InlineKeyboardButton(text='🤑 Сделать заказ', callback_data='make_order')
    faq_button = InlineKeyboardButton(text='ℹ F.A.Q', callback_data='faq')
    ask_button = InlineKeyboardButton(text='❓ Задать вопрос', callback_data='ask_question')
    user_menu.insert(order_button)
    user_menu.insert(faq_button)
    user_menu.insert(ask_button)
    return user_menu


def get_start_menu():
    user_menu = InlineKeyboardMarkup(row_width=1)
    start_button = InlineKeyboardButton(text='🤖Начать работу с ботом🤖', callback_data='start_app')
    user_menu.insert(start_button)
    return user_menu


def get_approve_menu(text: str, button_type: str = 'order'):
    user_menu = InlineKeyboardMarkup(row_width=2)
    if button_type == 'order':
        callback_text = 'order_approve'
    else:
        callback_text = 'ask_approve'
    order_button_approve = InlineKeyboardButton(text=f'{text}', callback_data=callback_text)
    back_button = InlineKeyboardButton(text='👈 Назад', callback_data='back_menu')
    user_menu.insert(order_button_approve)
    user_menu.insert(back_button)
    return user_menu


def get_back_button():
    user_menu = InlineKeyboardMarkup(row_width=1)
    back_button = InlineKeyboardButton(text='👈 Назад', callback_data='back_menu')
    user_menu.insert(back_button)
    return user_menu


def get_finish_order_button():
    finish_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    finish_button = KeyboardButton('🏁 Завершить выбор')
    finish_menu.add(finish_button)
    return finish_menu
