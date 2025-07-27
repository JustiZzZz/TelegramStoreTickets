from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📚 Тарифы и покупка", callback_data="choice_buy")],
    [InlineKeyboardButton(text="🔍 Посмотреть примеры", callback_data="example")],
    [InlineKeyboardButton(text="❓ Как это работает?", callback_data="how_it_works")],
    [InlineKeyboardButton(text="✍️ Задать вопрос", callback_data="ask_question")]
])

back_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="back_start")]
])

back_menu_close = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Закрыть", callback_data="close_message")]
])

choice_buy = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⚡️ Математика (29 BYN)", callback_data="buy_math")],
    [InlineKeyboardButton(text="🚀 Физика (29 BYN)", callback_data="buy_physics")],
    [InlineKeyboardButton(text="💎 Математика + Физика (45 BYN)", callback_data="buy_both")],
    [InlineKeyboardButton(text="📄 Пользовательское соглашение", callback_data="user_agreement")],
    [InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="back_start")]
])

user_agreement_next_stage = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🥱 А можно вкратце?", callback_data="short_agreement")],
    [InlineKeyboardButton(text="⬅️ Вернуться к тарифам", callback_data="choice_buy")]
])

short_agreement = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⬅️ Вернуться к тарифам", callback_data="choice_buy")]
])

payment_for_the_product = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Я оплатил(а), готов(а) отправить чек", callback_data="payment_trigger")],
    [InlineKeyboardButton(text="⬅️ Вернуться к тарифам", callback_data="choice_buy")]
])

example_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⚡️ Математика", callback_data="math")],
    [InlineKeyboardButton(text="🚀 Физика", callback_data="physics")],
    [InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="back_start")]
])

decline_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✍️ Задать вопрос администратору", callback_data="ask_question")],
    [InlineKeyboardButton(text="⬅️ Вернуться в меню", callback_data="back_start")]
])

def admin_decline_keyboard(user_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(
        text="❌ Отклонить оплату", callback_data=f"decline_{user_id}"
    )
    return builder.as_markup()
