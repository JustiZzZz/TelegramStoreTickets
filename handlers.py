# handlers.py
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaAudio, InputMediaDocument
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage # You can define storage here or in run.py

import keyboards as kb
from files.config import ADMIN_ID, MEDIA_MATH, VOICE_MATH, PAYMENT_REQUISITES, FULL_AGREEMENT_LINK

router = Router()

class PaymentStates(StatesGroup):
    waiting_for_payment_proof = State()
    admin_replying = State()

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
            f"Полный текст публичной оферты доступен по ссылке: <a href='{FULL_AGREEMENT_LINK}'>здесь</a>"
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
            f"1️⃣ Переведите указанную сумму по реквизитам: {PAYMENT_REQUISITES}\n\n"
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
            "<b>1. Что вы покупаете?</b>\n"
            "Вы приобретаете личный, бессрочный доступ к закрытому Telegram-каналу (или каналам) для собственного обучения. Вы не покупаете сами файлы, а право пользоваться базой знаний.\n\n"
            "<b>2. Что категорически запрещено? (Самое важное!)</b>\n"
            "Все материалы являются авторской интеллектуальной собственностью. Поэтому <b>строго запрещается</b>:\n"
            "— делать скриншоты, сканы, копировать или записывать материалы.\n"
            "— Делиться материалами или доступом с кем-либо еще (друзьями, одноклассниками).\n"
            "— Перепродавать или публиковать гайды в открытом доступе.\n"
            "— Передавать кому-либо полученную ссылку-приглашение.\n\n"
            "❗️ <b>Нарушение этих правил ведет к немедленной и безвозвратной блокировке доступа без возврата средств.</b>\n\n"
            "<b>3. Можно ли вернуть деньги?</b>\n"
            "Поскольку услуга заключается в предоставлении доступа к цифровым материалам и считается оказанной в момент отправки вам ссылки, возврат средств после получения доступа невозможен.\n\n"
            "<b>4. Гарантирует ли гайд сдачу экзамена?</b>\n"
            "Наши гайды – это мощный и эффективный инструмент для подготовки, но они не гарантируют успешную сдачу экзамена. Ваш итоговый результат зависит только от вашего усердия и личной подготовки. Мы даем удочку – а рыбачите вы 🙃\n\n"
            f"Это ключевые моменты. Полный текст соглашения, который вы принимаете при оплате, находится здесь: <a href='{FULL_AGREEMENT_LINK}'>здесь</a>\n\n"
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
async def start_payment_proof_collection(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        'Пожалуйста, пришлите скриншот или фото чека об оплате. Если вы хотите отправить текстовое сообщение, также отправьте его сейчас.',
    )
    await state.set_state(PaymentStates.waiting_for_payment_proof)
    await callback.answer()

@router.message(StateFilter(PaymentStates.waiting_for_payment_proof), F.photo)
async def process_payment_photo(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name
    caption_from_user = message.caption or 'Без подписи'
    caption_for_admin = (
        f"Новый чек от пользователя @{username} (ID: <code>{user_id}</code>).\n\n"
        f"<b>Сообщение от пользователя:</b>\n{caption_from_user}"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="Ответить пользователю", callback_data=f"reply_to_user:{user_id}")

    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=caption_for_admin,
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )
    await message.answer("Спасибо! Ваш чек отправлен на проверку. Мы свяжемся с вами в ближайшее время.")
    await state.clear()

@router.message(StateFilter(PaymentStates.waiting_for_payment_proof), F.text)
async def process_payment_text(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name
    text_content = message.text

    builder = InlineKeyboardBuilder()
    builder.button(text="Ответить пользователю", callback_data=f"reply_to_user:{user_id}")

    await bot.send_message(
        chat_id=ADMIN_ID,
        text=(
            f"Новое текстовое сообщение от пользователя @{username} (ID: <code>{user_id}</code>) по поводу оплаты:\n\n"
            f"<b>Содержание:</b>\n{text_content}"
        ),
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )
    await message.answer("Спасибо! Ваше сообщение отправлено на проверку. Мы свяжемся с вами в ближайшее время.")
    await state.clear()

@router.message(StateFilter(PaymentStates.waiting_for_payment_proof), F.voice)
async def process_payment_voice(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name

    builder = InlineKeyboardBuilder()
    builder.button(text="Ответить пользователю", callback_data=f"reply_to_user:{user_id}")

    await bot.send_voice(
        chat_id=ADMIN_ID,
        voice=message.voice.file_id,
        caption=(
            f"Новое голосовое сообщение от пользователя @{username} (ID: <code>{user_id}</code>) по поводу оплаты."
        ),
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )
    await message.answer("Спасибо! Ваше голосовое сообщение отправлено на проверку. Мы свяжемся с вами в ближайшее время.")
    await state.clear()

@router.message(StateFilter(PaymentStates.waiting_for_payment_proof), F.document)
async def process_payment_document(message: Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.full_name
    caption_from_user = message.caption or 'Без подписи'
    caption_for_admin = (
        f"Новый документ от пользователя @{username} (ID: <code>{user_id}</code>).\n\n"
        f"<b>Сообщение от пользователя:</b>\n{caption_from_user}"
    )

    builder = InlineKeyboardBuilder()
    builder.button(text="Ответить пользователю", callback_data=f"reply_to_user:{user_id}")

    await bot.send_document(
        chat_id=ADMIN_ID,
        document=message.document.file_id,
        caption=caption_for_admin,
        parse_mode="HTML",
        reply_markup=builder.as_markup()
    )
    await message.answer("Спасибо! Ваш документ отправлен на проверку. Мы свяжемся с вами в ближайшее время.")
    await state.clear()

@router.message(StateFilter(PaymentStates.waiting_for_payment_proof))
async def process_unsupported_payment_proof(message: Message, state: FSMContext):
    await message.answer("Извините, я могу принять только фото, текст, голосовое сообщение или документ для подтверждения оплаты. Пожалуйста, отправьте один из этих форматов.")

@router.callback_query(F.data.startswith('reply_to_user:'))
async def start_admin_reply(callback: CallbackQuery, state: FSMContext):
    if callback.from_user.id != ADMIN_ID:
        await callback.answer("У вас нет прав на эту операцию.", show_alert=True)
        return

    target_user_id = int(callback.data.split(':')[1])
    await state.update_data(target_user_id=target_user_id)
    await state.set_state(PaymentStates.admin_replying)
    await callback.message.answer(f"Вы отвечаете пользователю с ID: <code>{target_user_id}</code>. Введите ваше сообщение:", parse_mode="HTML")
    await callback.answer()

@router.message(StateFilter(PaymentStates.admin_replying), F.text)
async def send_admin_reply(message: Message, state: FSMContext, bot: Bot):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Извините, у вас нет прав на эту операцию.")
        await state.clear()
        return

    data = await state.get_data()
    target_user_id = data.get('target_user_id')
    admin_message = message.text

    if target_user_id:
        try:
            await bot.send_message(
                chat_id=target_user_id,
                text=f"✉️ <b>Сообщение от администратора:</b>\n\n{admin_message}",
                parse_mode="HTML"
            )
            await message.answer(f"Сообщение успешно отправлено пользователю <code>{target_user_id}</code>.")
        except Exception as e:
            await message.answer(f"Не удалось отправить сообщение пользователю <code>{target_user_id}</code>. Ошибка: {e}")
    else:
        await message.answer("Ошибка: не найден ID пользователя для ответа.")

    await state.clear()

@router.message(StateFilter(PaymentStates.admin_replying), F.photo | F.voice | F.document | F.sticker)
async def handle_admin_non_text_reply(message: Message, state: FSMContext):
    if message.from_user.id not in ADMIN_ID:
        await message.answer("Извините, у вас нет прав на эту операцию.")
        await state.clear()
        return
    await message.answer("Извините, для ответа пользователю отправьте, пожалуйста, текстовое сообщение.")
