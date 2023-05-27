import os
import time
import telebot

import db
import db_pattern_search
from stt import STT
from fio import get_fio
from punctuation import get_punctuation

with open('token/token.txt', 'r') as file:
    TOKEN = file.read()

bot = telebot.TeleBot(TOKEN)

stt = STT()


# Хэндлер на команду /start
@bot.message_handler(commands=["start"])
def cmd_start(message):
    text = "Привет! Это Бот для получения голосового сообщения от руководителя и последующей отправкой нужному " \
           "сотруднику."

    db.create_database()

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["initUser"])
def cmd_init_user(message):
    chat_id = message.from_user.id
    print(db.get_user_by_chat_id(chat_id))
    if not db.get_user_by_chat_id(chat_id):
        last_name = message.from_user.last_name
        first_name = message.from_user.first_name
        username = message.from_user.username
        db.insert_query(last_name, first_name, username, chat_id)
        bot.send_message(message.chat.id, "Вы успешно добавлены в базу сотрудников!")
    else:
        bot.send_message(message.chat.id, "Вы уже есть в базе сотрудников!")


# Хэндлер на получение голосового сообщения
@bot.message_handler(content_types=["voice"])
def voice_message_handler(message):
    """
    Обработчик на получение голосового сообщения.
    """
    file_id = message.voice.file_id
    file_info = bot.get_file(file_id)
    file_path = file_info.file_path

    file_on_disk = f"{file_id}.tmp"
    downloaded_file = bot.download_file(file_path)
    bot.send_message(message.chat.id, "Аудио получено")

    time.sleep(1)

    with open(file_on_disk, "wb") as f:
        f.write(downloaded_file)

    time.sleep(1)

    text = stt.audio_to_text(f"{file_id}.tmp")

    if not text:
        text = "Формат документа не поддерживается"

    text = get_punctuation(text)
    fio = get_fio(text)

    bot.send_message(message.chat.id, text)

    if fio is None:
        bot.send_message(message.chat.id, "Что-то пошло не так")
    else:
        chat_id = db_pattern_search.find_username(fio[1], fio[0], db.get_all_users())
        bot.send_message(chat_id, "Руководитель просил вам передать следующее сообщение: \"" + text + "\"")

    os.remove(file_on_disk)  # Удаление временного файла


bot.polling(none_stop=True)
