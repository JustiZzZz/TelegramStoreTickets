import re
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, StateFilter
import keyboards as kb
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaAudio
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from files.config import (
    ADMIN_ID, MEDIA_MATH, VOICE_MATH, SUCCESS_PAYMENT_MESSAGE, VOICE_PHYSICS, MEDIA_PHYSICS
)

router = Router()

class AskQuestion(StatesGroup):
    waiting_for_question = State()

class Payment(StatesGroup):
    waiting_for_check = State()
    tariff_type = State()

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

@router.callback_query(F.data == 'how_it_works')
async def how_it_works(callback: CallbackQuery):
    await callback.message.answer(
        text=(
            "<b>⚙️ Все максимально просто и прозрачно. Вот как это работает:</b>\n\n"
            "1️⃣ <b>Выбираете тариф</b>, который подходит именно вам\n\n"
            "2️⃣ <b>Оплачиваете доступ</b> по реквизитам. Наша деятельность оформлена официально (самозанятость), что является гарантией честности\n\n"
            "3️⃣ <b>Присылаете скриншот чека</b> в этот бот\n\n"
            "4️⃣ <b>Получение доступа!</b> Мы лично проверяем оплату и высылаем вам уникальную ссылку-приглашение в закрытый канал с бессрочным доступом"
        ),
        reply_markup=kb.back_menu
    )
    await callback.answer()

@router.callback_query(F.data == 'ask_question')
async def ask_question(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AskQuestion.waiting_for_question)
    await callback.message.answer(
        "Мы с радостью ответим на любой ваш вопрос. Сформулируйте и отправьте его, пожалуйста, одним сообщением")
    await callback.answer()

@router.message(AskQuestion.waiting_for_question)
async def process_question(message: Message, state: FSMContext, bot: Bot):
    user_info = f"От пользователя @{message.from_user.username} (ID: `{message.from_user.id}`)"
    await bot.send_message(
        ADMIN_ID,
        f"❓ <b>Новый вопрос!</b>\n\n{user_info}\n\n<b>Текст вопроса:</b>\n«{message.text}»\n\n"
        "Чтобы ответить, просто используй функцию «Ответить» (Reply) на это сообщение (свайпни влево)"
    )
    await message.answer(
        "Спасибо! Ваш вопрос получен. Мы ответим вам в этот чат, как только сможем",
        reply_markup=kb.back_menu,
    )
    await state.clear()

@router.message(F.from_user.id == ADMIN_ID, F.reply_to_message, ~F.text.startswith('https://t.me/+'))
async def admin_reply_to_question(message: Message, bot: Bot):
    if "Текст вопроса:" in message.reply_to_message.text:
        match = re.search(r"\(ID: `(\d+)`\)", message.reply_to_message.text)
        if match:
            user_id = int(match.group(1))
            await bot.send_message(user_id, f"✉️ <b>Вам пришел ответ от администратора:</b>\n«{message.text}»")
            await message.answer("✅ Ответ на вопрос успешно отправлен пользователю")
    else:
        await message.answer(
            "Чтобы подтвердить оплату, ответьте на сообщение с чеком <b>ссылкой-приглашением</b>, а не текстом")

@router.message(F.from_user.id == ADMIN_ID, F.reply_to_message, F.text.startswith('https://t.me/+'))
async def admin_approve_with_link(message: Message, bot: Bot):
    if message.reply_to_message.caption:
        match = re.search(r"\(ID: `(\d+)`\)", message.reply_to_message.caption)
        if match:
            user_id = int(match.group(1))
            invite_link = message.text
            await bot.send_message(chat_id=user_id, text=SUCCESS_PAYMENT_MESSAGE.format(link=invite_link))
            await message.reply_to_message.edit_caption(
                caption=f"{message.reply_to_message.caption}\n\n✅ <b>ОПЛАТА ПОДТВЕРЖДЕНА</b>\nСсылка отправлена пользователю",
                reply_markup=None
            )
            await message.answer("✅ Ссылка-приглашение успешно отправлена пользователю")

@router.callback_query(F.data == 'choice_buy')
async def choice_buy(callback: CallbackQuery):
    await callback.message.edit_text(
        text=(
            "Пожалуйста, выберите подходящий вам тариф:\n\n"
            "⚡️ <b><u>Тариф «Гайд | Математика»</u></b>\n"
            "<b>Содержание:</b> полный разбор всех <b>100 билетов</b>\n\n"
            "<b>Стоимость: <u>29 BYN</u></b>\n\n"
            "<i>Идеально подходит для абитуриентов, поступающих по целевому направлению и сдающих устный экзамен по математике</i>\n\n"
            "🚀 <b><u>Тариф «Гайд | Физика»</u></b>\n"
            "<b>Содержание:</b> полный разбор всех <b>94 билетов</b>\n\n"
            "<b>Стоимость: <u>29 BYN</u></b>\n\n"
            "<i>Идеально подходит для абитуриентов, поступающих по целевому направлению и сдающих устный экзамен по физике</i>\n\n"
            "💎 <b><u>Тариф «Гайд | Математика + Физика»</u></b>\n"
            "<b>Содержание:</b> все <b>100 билетов</b> по математике и <b>94 билета</b> по физике\n\n"
            "<b>Стоимость: <u>45 BYN</u></b> (выгода – 13 BYN)\n\n"
            "<i>Комплексное решение для абитуриентов после Национального детского технопарка (НДТП), проходящих собеседование по двум предметам</i>\n\n"
            "Перед покупкой, пожалуйста, ознакомьтесь с условиями предоставления услуг (кнопка «Пользовательское соглашение»)"
        ),
        reply_markup=kb.choice_buy,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith('buy_'))
async def payment_start(callback: CallbackQuery, state: FSMContext):
    tariff_code = callback.data.split('_')[1]
    await state.update_data(tariff_type=tariff_code)

    if tariff_code == 'math':
        price, name, info = 29, "«Гайд | Математика»", "к одному закрытому каналу"
    elif tariff_code == 'physics':
        price, name, info = 29, "«Гайд | Физика»", "к одному закрытому каналу"
    else:
        price, name, info = 45, "«Гайд | Математика + Физика»", "к двум закрытым каналам"

    await callback.message.edit_text(
        text=(
            f"Отлично! Вы выбрали тариф <b>{name}</b>\n\n"
            f"<b>К оплате:</b> {price} белорусских рублей\n"
            f"<b>Доступ:</b> бессрочный, предоставляется {info}\n\n"
            "<b>Инструкция по оплате:</b>\n\n"
            "1️⃣ Переведите указанную сумму по реквизитам: [здесь будут реквизиты]\n\n"
            "2️⃣ <b>ВАЖНО</b> сделайте скриншот или фото чека об оплате\n\n"
            "3️⃣ Нажмите кнопку ниже, как только будете готовы отправить чек\n\n"
            "<i>Нажимая кнопку «Я оплатил(а)», вы подтверждаете, что ознакомились и согласны с условиями Пользовательского соглашения</i>"
        ),
        reply_markup=kb.payment_for_the_product,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == 'payment_guide')
async def payment_guide(callback: CallbackQuery):
    await callback.message.answer(
        'ТЕКСТ ПРИМЕРА',
        reply_markup=kb.back_menu_close
    )
    await callback.answer()

@router.callback_query(F.data == 'user_agreement')
async def user_agreement(callback: CallbackQuery):
    await callback.message.answer(
        text=(
            "<b>Пользовательское соглашение</b>\n\n"
            "В этом документе изложены условия и правила использования материалов, порядок оплаты, а также права и обязанности сторон\n\n"
            "Ознакомление с ним – важный шаг перед покупкой. Совершая оплату, вы автоматически подтверждаете свое полное согласие со всеми пунктами соглашения\n\n"
            "Полный текст публичной оферты доступен по <a href=\"https://graph.org/Publichnaya-oferta-Polzovatelskoe-soglashenie-na-predostavlenie-dostupa-k-informacionnym-materialam-07-26\">ссылке</a>"
        ),
        reply_markup=kb.user_agreement_next_stage,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == 'short_agreement')
async def short_agreement(callback: CallbackQuery):
    await callback.message.answer(
        text=(
            "Конечно! Вот выжимка самых важных пунктов из Пользовательского соглашения, чтобы вы четко понимали основные условия. Это не заменяет полного документа, но поможет быстро сориентироваться\n\n"
            "<b>Кратко о главном из Пользовательского соглашения:</b>\n\n"
            "<b>1. Что вы покупаете?</b>\n\n"
            "Вы приобретаете личный, бессрочный доступ к закрытому Telegram-каналу (или каналам) для собственного обучения. Вы не покупаете сами файлы, а право пользоваться базой знаний\n\n"
            "<b>2. Что категорически запрещено? <u>(Самое важное!)</u></b>\n\n"
            "Все материалы являются авторской интеллектуальной собственностью. Поэтому <b>строго запрещается</b>: делать скриншоты, сканы, копировать или записывать материалы. Делиться материалами или доступом с кем-либо еще (друзьями, одноклассниками). Перепродавать или публиковать гайды в открытом доступе. Передавать кому-либо полученную ссылку-приглашение\n\n"
            "❗ <b>Нарушение этих правил ведет к немедленной и безвозвратной блокировке доступа без возврата средств.</b>\n\n"
            "<b>3. Можно ли вернуть деньги?</b>\n\n"
            "Поскольку услуга заключается в предоставлении доступа к цифровым материалам и считается оказанной в момент отправки вам ссылки, возврат средств после получения доступа невозможен\n\n"
            "<b>4. Гарантирует ли гайд сдачу экзамена?</b>\n\n"
            "Наши гайды – это мощный и эффективный инструмент для подготовки, но они не гарантируют успешную сдачу экзамена. Ваш итоговый результат зависит только от вашего усердия и личной подготовки. Мы даем удочку – а рыбачите вы 🙃\n\n"
            "Это ключевые моменты. Полный текст соглашения, который вы принимаете при оплате, находится <a href=\"https://graph.org/Publichnaya-oferta-Polzovatelskoe-soglashenie-na-predostavlenie-dostupa-k-informacionnym-materialam-07-26\">здесь</a>\n\n"
            "Пожалуйста, ознакомьтесь с ним перед совершением покупки"
        ),
        reply_markup=kb.short_agreement,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == 'example')
async def example(callback: CallbackQuery):
    await callback.message.edit_text(
        'Выберите предмет, чтобы посмотреть, как выглядят материалы:',
        reply_markup=kb.example_menu
    )
    await callback.answer()

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
        InputMediaAudio(media=file_id, caption="🎙️ <i>Пример аудиобилета по математике</i>" if i == 0 else None,
                        parse_mode="HTML") for i, file_id in enumerate(VOICE_MATH)]
    await callback.message.answer_media_group(media=media_group_audio)
    await callback.message.answer(
        'Вот пример разбора одного из билетов по математике. В закрытом канале каждый билет разобран так же подробно, в формате «фото-конспект + аудио-версия»',
        reply_markup=kb.back_menu
    )
    await callback.answer()

@router.callback_query(F.data == 'physics')
async def math_media(callback: CallbackQuery):
    await callback.message.answer(
        "<b>Физика | Билет №1</b>\n"
        "<b>Тема:</b> Механическое движение. Относительность покоя и движения. Поступательное движение. Система отсчета. Характеристики механического движения: путь, перемещение, координата",
        parse_mode="HTML"
    )
    media_group_photo = [InputMediaPhoto(media=file_id) for file_id in MEDIA_PHYSICS]
    await callback.message.answer_media_group(media=media_group_photo)
    media_group_audio = [
        InputMediaAudio(media=file_id, caption="🎙️ <i>Пример аудиобилета по физике</i>" if i == 0 else None,
                        parse_mode="HTML") for i, file_id in enumerate(VOICE_PHYSICS)]
    await callback.message.answer_media_group(media=media_group_audio)
    await callback.message.answer(
        'Вот пример разбора одного из билетов по физике. В закрытом канале каждый билет разобран так же подробно, в формате «фото-конспект + аудио-версия»',
        reply_markup=kb.back_menu
    )
    await callback.answer()

@router.callback_query(F.data == 'back_start')
async def back_to_start(callback: CallbackQuery):
    await callback.message.edit_text(
        'Вы вернулись в главное меню. Воспользуйтесь кнопками ниже ⬇️',
        reply_markup=kb.main_menu
    )
    await callback.answer()

@router.callback_query(F.data == 'payment_trigger')
async def payment_trigger(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Payment.waiting_for_check)
    await callback.message.edit_text(
        "Замечательно! Остался последний шаг. Пожалуйста, отправьте скриншот чека об оплате в этот чат ⬇️",
        reply_markup=None
    )
    await callback.answer()

@router.message(Payment.waiting_for_check, F.photo)
async def process_check(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    tariff = user_data.get('tariff_type', 'unknown')
    user_info = f"от @{message.from_user.username} (ID: `{message.from_user.id}`)"
    caption = (
        f"🧾 Новая оплата {user_info}\n<b>Тариф: {tariff.upper()}</b>\n\n"
        "<i><b>Инструкция для админа:</b></i>\n"
        "<i>1. Создай уникальную ссылку-приглашение</i>\n"
        "<i>2. Ответь на ЭТО сообщение этой ссылкой, чтобы подтвердить оплату</i>"
    )
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=message.photo[-1].file_id,
        caption=caption,
        reply_markup=kb.admin_decline_keyboard(user_id=message.from_user.id)
    )
    await message.answer(
        "Благодарю. Ваш чек получен и передан на проверку. Обычно это занимает не больше часа. Хорошего дня! 😊")
    await state.clear()

@router.callback_query(F.data.startswith('decline_'))
async def decline_payment(callback: CallbackQuery, bot: Bot):
    user_id = int(callback.data.split('_')[1])
    await bot.send_message(
        user_id,
        "❌ К сожалению, ваша оплата была отклонена. Пожалуйста, свяжитесь с администратором для уточнения деталей, если считаете, что это ошибка",
        reply_markup=kb.decline_menu
    )
    await callback.message.edit_caption(
        caption=f"{callback.message.caption}\n\n❌ <b>ОПЛАТА ОТКЛОНЕНА</b>",
        reply_markup=None
    )
    await callback.answer("Оповещение об отклонении отправлено пользователю")

# @router.message(F.photo)
# async def get_photo(message: Message):
#     await message.answer(f'ID фото: {message.photo[-1].file_id}')
#
# @router.message(F.voice)
# async def handle_voice(message: Message):
#     await message.answer(f"🎤 file_id голосового сообщения:\n`{message.voice.file_id}`")