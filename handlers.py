from aiogram import F, Router
from aiogram.filters import CommandStart, Command, StateFilter
import keyboards as kb
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaAudio
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from files.config import MEDIA_MATH, VOICE_MATH

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(
        text=(
            "<b>Здравствуйте! Добро пожаловать в официальный бот проекта <u>«Гайды по билетам»</u></b> 🎓\n\n"
            "Этот бот – ваш проводник к закрытому Telegram-каналу, где собраны подробные разборы всех экзаменационных билетов по <b>устной математике и физике</b> \n\n"
            "<b>О нас:</b>\n"
            "Нас зовут Таня и Кирилл. Мы сами недавно были на вашем месте, успешно сдали эти экзамены и поступили. "
            "Мы создали эти материалы, чтобы систематизировать знания и помочь вам подготовиться <b>уверенно и без стресса</b>, "
            "опираясь на свежий и релевантный опыт ☝️\n\n"
            "<b>Что вы найдете в закрытом канале:</b>\n"
            "🔹 Фотографии красиво и понятно оформленных конспектов по каждому билету\n"
            "🔹 Профессиональные аудиоверсии разборов для удобного прослушивания\n"
            "🔹 Удобную навигацию по темам и номерам билетов\n\n"
            "Воспользуйтесь меню ниже, чтобы узнать больше, посмотреть примеры или сразу получить доступ ⬇️"
        ),
        reply_markup=kb.main_menu,
        parse_mode="HTML"
    )



@router.callback_query(F.data == 'payment_guide')
async def payment_guide(callback: CallbackQuery):
    await callback.message.answer(
        'ТЕКСТ ПРИМЕРА',
        reply_markup=kb.back_menu_close
    )
    await callback.answer()

@router.callback_query(F.data == 'choice_buy')
async def choice_buy(callback: CallbackQuery):
    await callback.message.answer(
        text=(
            "Пожалуйста, выберите подходящий вам тариф:\n\n"
            "<b><u>⚡️ Тариф «Гайд | Математика»</u></b>\n"
            "<b>Содержание:</b>  полный разбор всех <b>100 билетов</b>\n"
            "<b>Стоимость: <u>29 BYN</u></b>\n\n"
            "<i>Идеально подходит для абитуриентов, поступающих по целевому направлению и сдающих устный экзамен по математике</i>\n\n"
            "<b><u>🚀 Тариф «Гайд | Физика»</u></b>\n"
            "<b>Содержание:</b> полный разбор всех 94 билетов\n"
            "<b>Стоимость: <u>29 BYN</u></b>\n\n"
            "<i>Идеально подходит для абитуриентов, поступающих по целевому направлению и сдающих устный экзамен по физике</i>\n\n"
            "<b><u>💎 Тариф «Гайд | Математика + Физика»</u></b>\n"
            "<b>Содержание:</b> все <b>100 билетов</b> по математике и <b>94 билета</b> по физике\n"
            "<b>Стоимость: <u>45 BYN</u></b> (выгода – 13 BYN)\n\n"
            "<i>Комплексное решение для абитуриентов после Национального детского технопарка (НДТП), проходящих собеседование по двум предметам</i>\n\n"
            "Перед покупкой, пожалуйста, ознакомьтесь с условиями предоставления услуг (кнопка «Пользовательское соглашение»)"
        ),
        reply_markup=kb.user_agreement,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == 'user_agreement')
async def user_agreement(callback: CallbackQuery):
    await callback.message.answer(
        text=(
            "<b>Пользовательское соглашение</b>\n\n"
            "В этом документе изложены условия и правила использования материалов, порядок оплаты, а также права и обязанности сторон.\n\n"
            "Ознакомление с ним – важный шаг перед покупкой. Совершая оплату, вы автоматически подтверждаете свое полное согласие со всеми пунктами соглашения.\n\n"
            "Полный текст публичной оферты доступен по ссылке: [тут ссылка на статью Телеграф]"
        ),
        reply_markup=kb.user_agreement_next_stage,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == 'product_selection')
async def products(callback: CallbackQuery):
    await callback.message.answer(
        text=(
            "Пожалуйста, выберите ваш тариф"
        ),
        reply_markup=kb.product_selection,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == 'math_payment')
async def math_payment(callback: CallbackQuery):
    await callback.message.answer(
        text=(
            "Отлично! Вы выбрали тариф «Гайд | Математика»\n\n"
            "К оплате: <b>29 белорусских рублей</b>\n"
            "Доступ: бессрочный, предоставляется к одному закрытому каналу «Гайд по билетам | Математика»\n\n"
            "<b>Инструкция по оплате:</b>\n\n"
            "1️⃣ Переведите указанную сумму по реквизитам: [здесь будут реквизиты]\n\n"
            "2️⃣ <b>ВАЖНО</b> сделайте скриншот или фото чека об оплате\n\n"
            "3️⃣ Нажмите кнопку ниже, как только будете готовы отправить чек\n\n"
            "Нажимая кнопку «Я оплатил(а)», вы подтверждаете, что ознакомились и согласны с условиями Пользовательского соглашения"
        ),
        reply_markup=kb.payment_for_the_product,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == 'short_agreement')
async def short_agreement(callback: CallbackQuery):
    await callback.message.answer(
        text=(
            "Конечно! Вот выжимка самых важных пунктов из Пользовательского соглашения, чтобы вы четко понимали основные условия. Это не заменяет полного документа, но поможет быстро сориентироваться.\n\n"
            "<b>Кратко о главном из Пользовательского соглашения:</b>\n\n"
            "<b>1. Что вы покупаете?</b>\n\n"
            "Вы приобретаете личный, бессрочный доступ к закрытому Telegram-каналу (или каналам) для собственного обучения. Вы не покупаете сами файлы, а право пользоваться базой знаний\n\n"
            "<b>2. Что категорически запрещено? (Самое важное!)</b>\n\n"
            "Все материалы являются авторской интеллектуальной собственностью. Поэтому <b>строго запрещается</b>: Все материалы являются авторской интеллектуальной собственностью. Поэтому строго запрещается: делать скриншоты, сканы, копировать или записывать материалы. Делиться материалами или доступом с кем-либо еще (друзьями, одноклассниками). Перепродавать или публиковать гайды в открытом доступе. Передавать кому-либо полученную ссылку-приглашение\n\n"
            "❗ <b>Нарушение этих правил ведет к немедленной и безвозвратной блокировке доступа без возврата средств.</b>\n\n"
            "<b>3. Можно ли вернуть деньги?</b>\n\n"
            "Поскольку услуга заключается в предоставлении доступа к цифровым материалам и считается оказанной в момент отправки вам ссылки, возврат средств после получения доступа невозможен\n\n"
            "<b>4. Гарантирует ли гайд сдачу экзамена?</b>\n\n"
            "Наши гайды – это мощный и эффективный инструмент для подготовки, но они не гарантируют успешную сдачу экзамена. Ваш итоговый результат зависит только от вашего усердия и личной подготовки. Мы даем удочку – а рыбачите вы 🙃\n\n"
            "Это ключевые моменты. Полный текст соглашения, который вы принимаете при оплате, находится здесь: [опять ссылка на Телеграф]\n\n"  # Заменить на реальную ссылку
            "Пожалуйста, ознакомьтесь с ним перед совершением покупки."
        ),
        reply_markup=kb.short_agreement,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == 'example')
async def example(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        'Выберите предмет, по которому хотите увидеть пример',
        reply_markup=kb.example_menu
    )



@router.callback_query(F.data == 'math')
async def math_media(callback: CallbackQuery):
    await callback.message.answer(
        "<b>Математика | Билет №1</b>\n"
        "<b>Тема:</b> Определение угла. Равные углы. Биссектриса угла. Градусная мера угла",
        parse_mode="HTML"
    )
    media_group_photo = [InputMediaPhoto(media=file_id) for file_id in MEDIA_MATH]
    await callback.message.answer_media_group(media=media_group_photo)
    media_group_audio = [
        InputMediaAudio(
            media=file_id,
            caption="🎙️ <i>Пример аудиобилета по математике</i>" if i == 0 else None,
            parse_mode="HTML"
        )
        for i, file_id in enumerate(VOICE_MATH)
    ]
    await callback.message.answer_media_group(media=media_group_audio)
    await callback.message.answer(
        'Уже определились с выбором?',
        reply_markup=kb.back_menu
    )
    await callback.answer()



@router.callback_query(F.data == 'back_start')
async def back_to_start(callback: CallbackQuery):
    await callback.message.answer(
        '↩️Возвращаемся назад↩️',
        reply_markup=kb.main_menu
    )
    await callback.answer()


@router.callback_query(F.data == 'payment_trigger')
async def back_to_start(callback: CallbackQuery):
    await callback.message.answer(
        'Пожалуйста, пришлите чек оплаты!',
    )
    await callback.answer()




# @router.message(F.photo)
# async def get_photo(message: Message):
#     await message.answer(f'ID фото: {message.photo[-1].file_id}')
#
#
# @router.message(F.voice)
# async def handle_voice(message: Message):
#     await message.answer(f"🎤 file_id голосового сообщения:\n`{message.voice.file_id}`")
