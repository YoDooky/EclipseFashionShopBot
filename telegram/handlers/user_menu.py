from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot
from config.bot_config import ORDERS_CHAT_ID, QA_CHAT_ID

from telegram import markups


class OrderItem(StatesGroup):
    waiting_for_photo = State()
    waiting_for_question = State()


class UserMenu:
    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    async def user_choice(call: types.CallbackQuery, state: FSMContext):
        await state.finish()
        keyboard = markups.get_user_menu()
        await call.message.edit_text(text='Что Вы хотите сделать? Оформить заказ, показать памятку по работе или '
                                          'задать вопрос нашим специалистам? 🧐',
                                     reply_markup=keyboard)

    @staticmethod
    async def make_order(call: types.CallbackQuery, state: FSMContext):
        keyboard = markups.get_back_button()
        await call.message.edit_text(text='Приложите скриншот с товаром и введите необходимый размер. '
                                          'После этого отправьте сообщение...',
                                     reply_markup=keyboard)
        await state.set_state(OrderItem.waiting_for_photo.state)

    #  send user choice to 'ORDER' chat
    async def send_order(self, message: types.Message, state: FSMContext):
        photo_id = message.photo[-1].file_id
        if not message.caption:
            await message.answer("Фотография должна содержать прикрепленный текст с размерами, "
                                 "пожалуйста повторите попытку")
            return
        caption_text = f'имя: {message.from_user.first_name}\n' \
                       f'имя пользователя: {message.from_user.mention}\n' \
                       f'детали заказа: {message.caption}'
        await self.bot.send_photo(ORDERS_CHAT_ID, photo_id, caption=caption_text)
        keyboard = markups.get_finish_order_button()
        await message.answer(text='Нажмите "Завершить", когда закончите выбор',
                             reply_markup=keyboard)

    #  send user choice to 'QA' chat
    async def send_ask(self, message: types.Message, state: FSMContext):
        try:
            photo_id = message.photo[-1].file_id
        except Exception as ex:
            photo_id = None
            pass
        if not message.text and not message.caption:
            await message.answer("Текст вопроса не должен быть пустым. Если во вложении фотография, "
                                 "пожалуйста приложите к ней описание своего вопроса")
            return
        question_text = message.text if not message.caption else message.caption
        caption_text = f'имя: {message.from_user.first_name}\n' \
                       f'имя пользователя: {message.from_user.mention}\n' \
                       f'вопрос: {question_text}'
        if message.caption:
            await self.bot.send_photo(QA_CHAT_ID, photo_id, caption=caption_text)
        else:
            await self.bot.send_message(QA_CHAT_ID, caption_text)
        keyboard = markups.get_user_menu()
        await message.answer(text='Ваш вопрос успешно отправлен нашим специалистам. С Вами скоро свяжутся',
                             reply_markup=keyboard)
        await state.finish()

    @staticmethod
    async def finish_order(message: types.Message, state: FSMContext):
        await state.finish()
        await message.answer(text='Заказ отправлен для оформления нашим специалистам 😎',
                             reply_markup=ReplyKeyboardRemove())
        keyboard = markups.get_user_menu()
        await message.answer(text='С Вами скоро свяжутся для дальнейшего оформления заказа',
                             reply_markup=keyboard)

    @staticmethod
    async def ask_question(call: types.CallbackQuery, state: FSMContext):
        keyboard = markups.get_back_button()
        await call.message.edit_text(text='Введите вопрос нашим специалистам и нажмите "Отправить вопрос"',
                                     reply_markup=keyboard)
        await state.set_state(OrderItem.waiting_for_question.state)

    @staticmethod
    async def send_faq(call: types.CallbackQuery):
        keyboard = markups.get_back_button()
        await call.message.edit_text(text='🌗FAQ🌗\n\n'
                                          '1) Как мы работаем?\n'
                                          'Вы выбираете в приложении Dewu любой товар, который вам понравился и '
                                          'заказываете этот товар через нашего телеграмм бота @bot (скидывая ему '
                                          'скриншот, указав размер)\n\n'
                                          '2) Оплата\n'
                                          'После того как вы оставили заказ нашему боту втечении суток с вами '
                                          'свяжется наш администратор который выставит вам счет.\n'
                                          'Цена формируется из цена товара * внутренний курс + наша наценка\n'
                                          'Наценка :\n до 1000RMB фиксированная наценка 200 RMB\n'
                                          'с 1000 до 10 000 RMB наценка 15%\n'
                                          'более 10 000 RMB наценка 10%\n'
                                          'Так же доставка будет зависеть от того куда будет отправлена посылка '
                                          'обычно цена не превышает 800р.\n\n'
                                          '3) Доставка\n'
                                          'Обычно доставка производится в течении 20-30 дней в зависимости от вашего '
                                          'местоположения.',
                                     reply_markup=keyboard)

    def register_handlers(self, dp: Dispatcher):
        """Register message handlers"""
        dp.register_callback_query_handler(self.user_choice, text='start_app')
        dp.register_callback_query_handler(self.make_order, text='make_order')
        dp.register_callback_query_handler(self.send_faq, text='faq')
        dp.register_callback_query_handler(self.ask_question, text='ask_question')
        dp.register_message_handler(self.send_order, content_types=['photo'], state=OrderItem.waiting_for_photo)
        dp.register_message_handler(self.send_ask, content_types=['photo', 'text'],
                                    state=OrderItem.waiting_for_question)
        dp.register_message_handler(self.finish_order, text='🏁 Завершить выбор', state='*')
        dp.register_callback_query_handler(self.user_choice, text='back_menu', state='*')
