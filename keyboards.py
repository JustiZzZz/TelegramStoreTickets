from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


main_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📚 Посмотреть примеры', callback_data='example')],
    [InlineKeyboardButton(text='💳 Купить доступ', callback_data='choice_buy')],
    [InlineKeyboardButton(text='❓ Как это работает?', callback_data='payment_guide')],
    [InlineKeyboardButton(text='✍️ Задать вопрос', url='https://catsgenerator.ru/')]
] )

back_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='↩️ Вернуться назад', callback_data='example')],
    [InlineKeyboardButton(text='↩️↩️ Вернуться в начало', callback_data='back_start')]
])

back_menu_close = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='↩️ Вернуться назад', callback_data='back_start')],
])

example_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='⚡️ Математика', callback_data='math'),
        InlineKeyboardButton(text='🚀 Физика', callback_data='physics')
     ],
    [InlineKeyboardButton(text='↩️ Вернуться назад', callback_data='back_start')],
])

user_agreement = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📄 Пользовательское соглашение', callback_data='user_agreement')],
    [InlineKeyboardButton(text='↩️ Вернуться назад', callback_data='back_start')]
])

user_agreement_next_stage = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Ознакомлен(а)', callback_data='product_selection')],
    [InlineKeyboardButton(text='🥱 А можно вкратце?', callback_data='short_agreement')],
    [InlineKeyboardButton(text='↩️ Вернуться назад', callback_data='back_start')]
])

product_selection = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="⚡️ Купить 'Математика'", callback_data='math_payment')],
    [InlineKeyboardButton(text="🚀 Купить 'Физика'", callback_data='physics_payment')],
    [InlineKeyboardButton(text="💎 Купить 'Математика + Физика'", callback_data='combo_payment')],
    [InlineKeyboardButton(text='↩️ Вернуться в начало', callback_data='back_start')]

])

short_agreement = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Теперь всё понятно!', callback_data='product_selection')],
])

payment_for_the_product = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Я оплатил(а)', callback_data='payment_trigger')],
    [InlineKeyboardButton(text='↩️ Вернуться назад', callback_data='product_selection')],
])