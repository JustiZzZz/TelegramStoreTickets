import re
from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, StateFilter, Command
import keyboards as kb
from aiogram.types import Message, CallbackQuery, InputMediaPhoto, InputMediaAudio, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

import database as db

from files.config import (
    ADMIN_CHAT_ID, MEDIA_MATH, VOICE_MATH, SUCCESS_PAYMENT_MESSAGE_SINGLE,
    SUCCESS_PAYMENT_MESSAGE_BOTH, VOICE_PHYSICS, MEDIA_PHYSICS,
)

router = Router()


class AskQuestion(StatesGroup):
    waiting_for_question = State()


class Payment(StatesGroup):
    waiting_for_check = State()
    tariff_type = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    db.add_user(
        user_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name
    )
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
        "Мы с радостью ответим на любой ваш вопрос. Сформулируйте и отправьте его, пожалуйста, одним сообщением (можно прикрепить фото)")
    await callback.answer()


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
            "Перед покупкой, пожалуйста, ознакомьтесь с условиями предоставления услуг (Пользовательским соглашением»)"
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
async def physics_media(callback: CallbackQuery):
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


@router.callback_query(F.data == 'back_start_new_msg')
async def back_to_start_new_msg(callback: CallbackQuery):
    await callback.message.answer(
        'Вы вернулись в главное меню. Воспользуйтесь кнопками ниже ⬇️',
        reply_markup=kb.main_menu
    )
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer()


@router.callback_query(F.data == 'payment_trigger')
async def payment_trigger(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Payment.waiting_for_check)
    await callback.message.edit_text(
        "Замечательно! Остался последний шаг. Пожалуйста, отправьте скриншот чека об оплате в этот чат ⬇️",
        reply_markup=None
    )
    await callback.answer()


@router.message(AskQuestion.waiting_for_question, F.text | F.photo)
async def process_question(message: Message, state: FSMContext, bot: Bot):
    user_info = f"От пользователя @{message.from_user.username} (ID: `{message.from_user.id}`)"
    user_question_text = message.text or message.caption or "[Фото без подписи]"
    photo_file_id = message.photo[-1].file_id if message.photo else None

    admin_message_id = None
    if ADMIN_CHAT_ID != 0:
        admin_message_text = (f"❓ <b>Новый вопрос!</b>\n\n{user_info}\n\n"
                              f"<b>Текст вопроса:</b>\n«{user_question_text}»\n\n"
                              "<i>Чтобы ответить, используй функкцию «Ответить» (Reply) на это сообщение</i>")
        if photo_file_id:
            sent_message = await bot.send_photo(ADMIN_CHAT_ID, photo=photo_file_id, caption=admin_message_text)
        else:
            sent_message = await bot.send_message(ADMIN_CHAT_ID, text=admin_message_text)
        admin_message_id = sent_message.message_id

    question_id = db.add_question(
        user_id=message.from_user.id,
        question_text=user_question_text,
        photo_id=photo_file_id,
        user_message_id=message.message_id,
        admin_message_id=admin_message_id
    )

    if admin_message_id:
        new_caption = f"❓ <b>Новый вопрос! (ID: {question_id})</b>\n\n{user_info}\n\n<b>Текст вопроса:</b>\n«{user_question_text}»\n\n<i>Чтобы ответить, используй функкцию «Ответить» (Reply) на это сообщение</i>"
        if photo_file_id:
            await bot.edit_message_caption(chat_id=ADMIN_CHAT_ID, message_id=admin_message_id, caption=new_caption)
        else:
            await bot.edit_message_text(text=new_caption, chat_id=ADMIN_CHAT_ID, message_id=admin_message_id)

    await message.answer(
        "Спасибо! Ваш вопрос получен. Мы ответим вам в этот чат, как только сможем",
        reply_markup=kb.back_menu,
    )
    await state.clear()


@router.message(Payment.waiting_for_check, F.photo)
async def process_check(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    tariff = user_data.get('tariff_type', 'unknown')
    user_info = f"от @{message.from_user.username} (ID: `{message.from_user.id}`)"

    caption_for_admin = (
        f"🧾 Новая оплата {user_info}\n<b>Тариф: {tariff.upper()}</b>"
    )
    if message.caption:
        caption_for_admin += f"\n\n<b>Подпись к чеку:</b> «{message.caption[:700]}»"

    try:
        sent_message = await bot.send_photo(
            chat_id=ADMIN_CHAT_ID,
            photo=message.photo[-1].file_id,
            caption=caption_for_admin
        )
        admin_message_id = sent_message.message_id

        purchase_id = db.add_purchase_check(
            user_id=message.from_user.id,
            tariff=tariff,
            photo_id=message.photo[-1].file_id,
            admin_message_id=admin_message_id
        )

        new_caption_with_id = (
            f"🧾 Новая оплата (ID: {purchase_id}) {user_info}\n<b>Тариф: {tariff.upper()}</b>"
        )
        if message.caption:
            new_caption_with_id += f"\n\n<b>Подпись к чеку:</b> «{message.caption[:700]}»"

        await bot.edit_message_caption(
            chat_id=ADMIN_CHAT_ID,
            message_id=admin_message_id,
            caption=new_caption_with_id,
            reply_markup=kb.get_admin_payment_keyboard(purchase_id=purchase_id)
        )

        await message.answer(
            "Благодарю. Ваш чек получен и передан на проверку. Обычно это занимает не больше часа. Хорошего дня! 😊")
        await state.clear()

    except Exception as e:
        print(f"Error processing check from user {message.from_user.id}: {e}")
        await message.answer(
            "К сожалению, при отправке вашего чека произошла техническая ошибка. 😔\n"
            "Пожалуйста, попробуйте отправить чек еще раз чуть позже или свяжитесь с поддержкой"
        )


@router.message(F.chat.id == ADMIN_CHAT_ID, F.reply_to_message, ~F.text.startswith('/'))
async def admin_reply_handler(message: Message, bot: Bot):
    reply = message.reply_to_message
    admin_username = message.from_user.username

    original_text = reply.text or reply.caption
    if original_text and "❓ Новый вопрос!" in original_text:
        match_question = re.search(r"\(ID: (\d+)\)", original_text)
        if match_question:
            question_id = int(match_question.group(1))
            question_details = db.get_question_details(question_id)
            if not question_details:
                await message.reply("⚠️ Не удалось найти этот вопрос в базе данных. Возможно, он уже был обработан")
                return

            user_id, user_question_preview, user_message_id = question_details

            try:
                if message.photo:
                    admin_response_caption = message.caption or ""
                    final_caption = f"✉️ <b>Ответ от администратора @{admin_username}:</b>\n\n{admin_response_caption}"
                    await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=final_caption,
                                         reply_to_message_id=user_message_id, reply_markup=kb.back_menu_new_msg)
                else:
                    admin_response_text = message.text or ""
                    final_text = f"✉️ <b>Ответ от администратора @{admin_username}:</b>\n\n{admin_response_text}"
                    await bot.send_message(user_id, final_text, reply_to_message_id=user_message_id,
                                           reply_markup=kb.back_menu_new_msg)

                await message.answer("✅ Ответ успешно отправлен пользователю")
                db.mark_question_as_answered(question_id)

                if reply.photo:
                    await bot.edit_message_caption(
                        chat_id=reply.chat.id, message_id=reply.message_id,
                        caption=f"{original_text}\n\n✅ <b>ОТВЕЧЕНО</b> администратором @{admin_username}"
                    )
                else:
                    await bot.edit_message_text(
                        chat_id=reply.chat.id, message_id=reply.message_id,
                        text=f"{original_text}\n\n✅ <b>ОТВЕЧЕНО</b> администратором @{admin_username}"
                    )

            except TelegramBadRequest as e:
                if "replied message not found" in str(e):
                    await message.reply(
                        "⚠️ Не удалось ответить на сообщение пользователя (возможно, оно удалено). Ответ будет отправлен без цитирования")
                    if message.photo:
                        admin_response_caption = message.caption or ""
                        final_caption = f"✉️ <b>Ответ от администратора @{admin_username}:</b>\n\n{admin_response_caption}"
                        await bot.send_photo(chat_id=user_id, photo=message.photo[-1].file_id, caption=final_caption,
                                             reply_markup=kb.back_menu_new_msg)
                    else:
                        admin_response_text = message.text or ""
                        final_text = f"✉️ <b>Ответ от администратора @{admin_username}:</b>\n\n{admin_response_text}"
                        await bot.send_message(user_id, final_text, reply_markup=kb.back_menu_new_msg)
                else:
                    await message.reply(f"❌ Произошла неизвестная ошибка: {e}")
            return

    if reply.caption and "⏳ ОЖИДАНИЕ ССЫЛКИ" in reply.caption:
        match_purchase = re.search(r"\(ID: (\d+)\)", reply.caption)
        if not match_purchase:
            await message.reply("⚠️ Не удалось извлечь ID покупки из сообщения. Обработка невозможна")
            return

        purchase_id = int(match_purchase.group(1))
        purchase_details = db.get_purchase_details(purchase_id)
        if not purchase_details:
            await message.reply("⚠️ Не удалось найти эту покупку в базе данных")
            return

        user_id, tariff_code = purchase_details
        invite_link_text = message.text

        if not invite_link_text or not invite_link_text.strip():
            await message.reply(
                "⚠️ <b>Ошибка!</b> Вы отправили пустое сообщение. Пожалуйста, отправьте ссылку-приглашение")
            return

        potential_links = invite_link_text.split()
        is_valid_format = all(link.startswith('https://t.me/+') for link in potential_links)

        if not is_valid_format:
            await message.reply(
                "⚠️ <b>Ошибка!</b> Пожалуйста, отправьте корректную(-ые) ссылку(-и)-приглашение (типа https://t.me/+)")
            return

        if tariff_code == 'both' and len(potential_links) < 2:
            await message.reply(
                "⚠️ <b>Внимание!</b>\nЭтот тариф требует <b>две</b> ссылки. Отправьте обе в одном сообщении")
            return

        success_message_template = SUCCESS_PAYMENT_MESSAGE_BOTH if tariff_code == 'both' else SUCCESS_PAYMENT_MESSAGE_SINGLE
        await bot.send_message(user_id, success_message_template.format(link=invite_link_text))

        db.update_purchase_status(purchase_id, 'approved')

        original_caption = reply.caption.split('\n\n⏳ ОЖИДАНИЕ ССЫЛКИ(-ОК)')[0]
        await bot.edit_message_caption(
            chat_id=reply.chat.id,
            message_id=reply.message_id,
            caption=f"{original_caption}\n\n✅ <b>ОПЛАТА ПОДТВЕРЖДЕНА</b> администратором @{admin_username}",
            reply_markup=None
        )
        await message.answer("✅ Ссылка(-и)-приглашение успешно отправлена")
        return


@router.callback_query(F.data.startswith('decline_'))
async def decline_payment(callback: CallbackQuery, bot: Bot):
    purchase_id = int(callback.data.split('_')[1])
    admin_username = callback.from_user.username

    purchase_details = db.get_purchase_details(purchase_id)
    if not purchase_details:
        await callback.answer("❌ Ошибка: покупка не найдена в базе", show_alert=True)
        return

    user_id, _ = purchase_details
    db.update_purchase_status(purchase_id, 'declined')

    await bot.send_message(
        user_id,
        "❌ К сожалению, ваша оплата была отклонена. Пожалуйста, свяжитесь с администратором для уточнения деталей, если считаете, что это ошибка",
        reply_markup=kb.decline_menu
    )

    base_caption = callback.message.caption or ""
    await callback.message.edit_caption(
        caption=f"{base_caption}\n\n❌ <b>ОПЛАТА ОТКЛОНЕНА</b> администратором @{admin_username}",
        reply_markup=None
    )
    await callback.answer("Платеж отклонен. Пользователь уведомлен")


@router.callback_query(F.data.startswith('approve_'))
async def approve_payment_start(callback: CallbackQuery):
    purchase_id = int(callback.data.split('_')[1])
    admin_username = callback.from_user.username
    base_caption = callback.message.caption or ""

    db.update_purchase_status(purchase_id, 'waiting_for_link')

    new_caption = (
        f"{base_caption}\n\n"
        f"⏳ <b>ОЖИДАНИЕ ССЫЛКИ(-ОК)</b> от администратора @{admin_username}\n\n"
        f"<i>Чтобы отправить ссылку(-и), ответьте (Reply) на это сообщение</i>"
    )
    try:
        await callback.message.edit_caption(
            caption=new_caption,
            reply_markup=None
        )
        await callback.answer("Теперь ответьте на это сообщение ссылкой(-ами)", show_alert=True)
    except Exception as e:
        print(f"Error in approve_payment_start callback: {e}")
        await callback.answer(f"❌ Ошибка при обновлении сообщения:\n{e}", show_alert=True)


@router.message(Command("pending_checks"), F.chat.id == ADMIN_CHAT_ID)
async def list_pending_checks(message: Message):
    pending_checks = db.get_pending_checks()
    if not pending_checks:
        await message.answer("✅ Все чеки обработаны. Очередь пуста")
        return

    response_text = "<b>🧾 Чеки, ожидающие обработки:</b>\n\n"
    builder = InlineKeyboardBuilder()
    chat_id_short = str(message.chat.id).replace("-100", "")

    for purchase_id, user_id, tariff, admin_message_id in pending_checks:
        msg_link = f"https://t.me/c/{chat_id_short}/{admin_message_id}"
        response_text += f"🔹 ID Покупки: `{purchase_id}` от юзера `{user_id}`. Тариф: `{tariff}`\n"
        builder.row(InlineKeyboardButton(text=f"Перейти к чеку ID {purchase_id}", url=msg_link))

    await message.answer(response_text, reply_markup=builder.as_markup())


@router.message(Command("pending_questions"), F.chat.id == ADMIN_CHAT_ID)
async def list_pending_questions(message: Message):
    pending_questions = db.get_pending_questions()
    if not pending_questions:
        await message.answer("✅ Все вопросы обработаны. Очередь пуста")
        return

    response_text = "<b>❓ Неотвеченные вопросы:</b>\n\n"
    builder = InlineKeyboardBuilder()
    chat_id_short = str(message.chat.id).replace("-100", "")

    for question_id, user_id, question_text, admin_message_id in pending_questions:
        msg_link = f"https://t.me/c/{chat_id_short}/{admin_message_id}"
        preview = (question_text[:50]).replace('\n', ' ') + '...'
        response_text += f"🔹 ID Вопроса: `{question_id}` от юзера `{user_id}`\nВопрос: <i>{preview}</i>\n"
        builder.row(InlineKeyboardButton(text=f"Перейти к вопросу ID {question_id}", url=msg_link))

    await message.answer(response_text, reply_markup=builder.as_markup())


@router.message(Command("stats"), F.chat.id == ADMIN_CHAT_ID)
async def get_stats(message: Message):
    purchase_stats = db.get_purchase_stats()
    total_purchases = sum(purchase_stats.values())

    stats_text = (
        "<b>📊 Статистика продаж:</b>\n\n"
        f"⚡️ Математика: <b>{purchase_stats.get('math', 0)}</b>\n"
        f"🚀 Физика: <b>{purchase_stats.get('physics', 0)}</b>\n"
        f"💎 Математика + Физика: <b>{purchase_stats.get('both', 0)}</b>\n\n"
        f"📈 <b>Всего покупок: {total_purchases}</b>\n\n"
        "<i>(Данные из базы данных)</i>"
    )
    await message.answer(stats_text)


@router.message(Command("advstats"), F.chat.id == ADMIN_CHAT_ID)
async def get_advanced_stats(message: Message):
    stats = db.get_advanced_stats()

    stats_text = f"""
📊 <b>Расширенная статистика</b>

<b>💰 Финансы (BYN)</b>
- За сегодня: <code>{stats['revenue']['today']}</code>
- За неделю: <code>{stats['revenue']['week']}</code>
- За месяц: <code>{stats['revenue']['month']}</code>
- <b>Всего:</b> <code>{stats['revenue']['total']}</code>

<b>📈 Продажи (шт)</b>
- За сегодня: <code>{stats['sales']['today']}</code>
- За неделю: <code>{stats['sales']['week']}</code>
- За месяц: <code>{stats['sales']['month']}</code>
- <b>Всего:</b> <code>{stats['sales']['total']}</code>

<b>👥 Новые пользователи</b>
- За сегодня: <code>{stats['users']['today']}</code>
- За неделю: <code>{stats['users']['week']}</code>
- За месяц: <code>{stats['users']['month']}</code>
- <b>Всего:</b> <code>{stats['users']['total']}</code>

<b>⏳ Ожидают обработки</b>
- Чеков на проверку: <code>{stats['pending']['checks']}</code>
- Вопросов без ответа: <code>{stats['pending']['questions']}</code>
"""
    await message.answer(stats_text)


@router.message(Command("userstats"), F.chat.id == ADMIN_CHAT_ID)
async def get_user_stats(message: Message):
    history = db.get_user_purchase_history()
    if not history:
        await message.answer("Пока не было ни одной подтвержденной покупки")
        return

    user_purchases = {}
    for user_id, username, first_name, tariff in history:
        if user_id not in user_purchases:
            user_purchases[user_id] = {
                'info': f"@{username}" if username else f"{first_name}",
                'tariffs': []
            }
        user_purchases[user_id]['tariffs'].append(f"<code>{tariff}</code>")

    response_text = "<b>История покупок пользователей:</b>\n\n"
    for user_id, data in user_purchases.items():
        tariffs_str = ", ".join(data['tariffs'])
        response_text += f"👤 <b>{data['info']}</b> (ID: <code>{user_id}</code>)\n"
        response_text += f"   - Тарифы: {tariffs_str}\n"
        response_text += "--------------------\n"

    if len(response_text) > 4096:
        for i in range(0, len(response_text), 4096):
            await message.answer(response_text[i:i + 4096])
    else:
        await message.answer(response_text)


@router.message(Command("reset_database"), F.chat.id == ADMIN_CHAT_ID)
async def reset_database_warning(message: Message):
    await message.answer(
        text=(
            "<b>🔴🔴 ВНИМАНИЕ! КРИТИЧЕСКОЕ ДЕЙСТВИЕ! 🔴🔴</b>\n\n"
            "Вы собираетесь <b>ПОЛНОСТЬЮ ОЧИСТИТЬ ВСЮ БАЗУ ДАННЫХ</b>. "
            "Это действие <u>необратимо</u> и приведет к удалению:\n\n"
            "- <b>Всех пользователей</b>\n"
            "- <b>Всех вопросов</b> от пользователей\n"
            "- <b>Всей истории покупок</b> и финансовой статистики\n\n"
            "Бот вернется в состояние, будто его только что запустили в первый раз. "
            "Вы абсолютно уверены, что хотите продолжить?"
        ),
        reply_markup=kb.confirm_full_reset_keyboard
    )


@router.callback_query(F.data == 'confirm_full_reset_yes', F.message.chat.id == ADMIN_CHAT_ID)
async def confirm_full_reset_action(callback: CallbackQuery):
    db.wipe_all_data()
    await callback.message.edit_text(
        "✅✅✅ <b>База данных полностью очищена</b> ✅✅✅\n\n"
        "Все пользователи, покупки и вопросы были удалены"
    )
    await callback.answer("Критическая операция выполнена: ВСЕ ДАННЫЕ УДАЛЕНЫ", show_alert=True)


@router.callback_query(F.data == 'confirm_full_reset_no', F.message.chat.id == ADMIN_CHAT_ID)
async def cancel_full_reset_action(callback: CallbackQuery):
    await callback.message.edit_text("👍 Действие отменено. Все данные в безопасности")
    await callback.answer("Отмена")